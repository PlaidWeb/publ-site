Title: Self-hosting Publ
Date: 2018-12-16 22:41:45-08:00
Entry-ID: 1278
UUID: 6b0d8b5d-08d2-5ad5-8cf0-13a1c5720586
Sort-Title: 300 Self-hosting

How to host Publ on your own webserver

.....

This assumes that you have your own webserver where you can run your site.  There are two parts to this: <a href="#service">running the Publ service</a>, and <a href="#routing">routing public traffic</a> from the fronting webserver (Apache, nginx, fhttpd, etc.) to it.

This list is not exhaustive; if there is a mechanism that you'd like to see supported, feel free to open an [issue](/issue-site/) or, better yet, [pull request](https://github.com/PlaidWeb/Publ-site/pulls) with details!

## <span id="service">Running the Publ service</span>

### Prerequisites

You will need Python 3. The most reliable way to install this is via [`pyenv`](https://github.com/pyenv/pyenv), but any system-provided Python 3 will do, as long as it meets the minimum system requirements.

The easiest way to manage your package dependencies is with [`poetry`](https://python-poetry.org); you can see [their installation instructions](https://python-poetry.org/docs/#installation) for more information. `pipenv` and `virtualenv` also work but these instructions will focus on the use of `poetry`.

Your Publ environment needs to have a WSGI server available. [gunicorn](http://gunicorn.org) is a good choice for this. The ideal means of installing gunicorn is directly into your site's environment. If you're using `poetry` then that's done with:

```bash
poetry add gunicorn
```

It will also be helpful to know the full path to the `poetry` command. You can usually find this with

```bash
which poetry
```

It will typically be `$HOME/.poetry/bin/poetry`.

### Basic approach

Anything that runs the application server should change into the site's working directory, and then start the gunicorn process with

```bash
/path/to/poetry run gunicorn -b unix:gunicorn.sock app:app
```

which will use the `app` object declared in `app.py` (per the [getting started guide](328)) and listen on a socket file named `gunicorn.sock`. The presence of that socket file will also indicate whether the site is up and running.

Note that you don't have to put `gunicorn.sock` in the same directory as the application -- it can go anywhere that the web server has access. For example, it's nice to make a `$HOME/.vhosts` directory to keep your socket files, named with the site name:

```bash
/path/to/poetry run gunicorn -b unix:/home/USERNAME/.vhosts/example.com app:app
```

This way you can also set the directory permissions on your site files with `chmod 700` which prevents other users of the server from peeking into them.

### <span id="systemd">systemd</span>

If you're on a UNIX that uses `systemd` (for example, recent versions of Ubuntu or CentOS), the preferred approach is to run the site as a user service. Here is an example service file:

```systemd
! example.com.service
[Unit]
Description=Publ instance for example.com

[Service]
Restart=always
WorkingDirectory=/home/USERNAME/example.com
ExecStart=/path/to/poetry run gunicorn -b unix:/path/to/socket app:app
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=default.target
```

Install this file as e.g. `$HOME/.config/systemd/user/example.com.service` and then you should be able to start the server with:

```bash
systemctl --user enable example.com
systemctl --user start example.com
```

and the site should now be up and running on the local port; as long as it's up there should be a socket file named `gunicorn.sock` in the site's directory.

However, this service will only run while the user is logged in; in order to make it run persistently, have an admin set your user to "linger" with e.g.:

```bash
sudo loginctl enable-linger USERNAME
```

Anyway, once you have this service set up, you can use `systemctl` to do a number of useful things; some example commands:

```bash
# Start the website if it isn't running
systemctl --user start example.com

# Shut off the website temporarily
systemctl --user stop example.com

# Reload the website (if e.g. templates changed)
systemctl --user reload-or-restart example.com

# Restart the website (if e.g. Publ or gunicorn gets updated)
systemctl --user restart example.com

# Disable the website from starting up automatically
systemctl --user disable example.com

# Enable the website to start up automatically
systemctl --user enable example.com

# Look at the status of the website (and see the logs)
systemctl --user status example.com
```

See the [`systemctl` manual page](https://www.freedesktop.org/software/systemd/man/systemctl.html) for more infromation.

### Other watchdog services

Some Linux distributions provide other mechanisms for running persistent services under a watchdog, such as [daemontools](https://cr.yp.to/daemontools.html) or [upstart](https://upstart.ubuntu.com/). These mechanisms are not highly recommended.

### cron

In a pinch, you can use a [cron job](https://en.wikipedia.org/wiki/Cron) as a makeshift supervisor; create a file named `cron-launcher.sh` in your site directory:

```bash
! cron-launcher.sh
#!/bin/sh

cd $(dirname "$0")
flock -n .lockfile /path/to/poetry run gunicorn -b unix:gunicorn.sock app:app
```

and then run `crontab -e` and add a line like:

```crontab
* * * * * /home/USERNAME/example.com/cron-launcher.sh
```

### Next steps

You can verify that the site is working with `curl`; for example:

```bash
curl --unix-socket gunicorn.sock https://example.com/
```

By default, `gunicorn` only runs with a small number of render threads. You might want to increase this with the `--threads` parameter, e.g.:

```bash
/path/to/poetry run gunicorn --threads 8 -b unix:/path/to/socket app:app
```

The number of threads to use varies greatly. You almost certainly want more than 1 thread (especially if you're planning on using authentication), but overallocating on threads can cause other problems to happen in some circumstances. I find that even for larger sites, a thread count of 8-12 is more than sufficient.

## <span id="routing">Routing traffic</span>

Configuring Publ to work with your web server is a matter of configuring the fronting httpd as a proxy to your Publ instance's socket. The two most common are [Apache](https://apache.org/) and [nginx](https://nginx.com/), but there are others as well.

### Apache

To use this with Apache, you'll need `mod_proxy` installed and enabled.

Next, you'll need to configure a vhost to forward your domain's traffic to the gunicorn socket. Here is a basic Apache configuration (e.g. `/etc/apache2/sites-enabled/100-example.com.conf`), showing how to configure both `http` and `https`:

```apache
# http
<VirtualHost *:80>
    ServerName example.com

    AcceptPathInfo On
    ErrorLog /path/to/error.log
    CustomLog /path/to/access.log combined

    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>

    ProxyPreserveHost On
    ProxyPass / unix:/user/USERNAME/example.com/gunicorn.sock|http://localhost/
</VirtualHost>

# https
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName example.com

    AcceptPathInfo On
    ErrorLog /path/to/ssl-error.log
    CustomLog /path/to/ssl-access.log combined

    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>

    ProxyPreserveHost On
    ProxyPass / unix:/user/USERNAME/example.com/gunicorn.sock|http://localhost/

    # tell gunicorn that this is https instead of http
    RequestHeader set X-Forwarded-Proto https
    SSLCertificateFile /path/to/fullchain.pem
    SSLCertificateKeyFile /path/to/privkey.pem
</VirtualHost>
</IfModule>
```

Note that both connections go over the same socket; you can have arbitrarily many fronting configurations to the same Publ instance, even with different domain names! Publ doesn't mind at all.

If you use [Let's Encrypt](http://letsencrypt.org/) to manage your SSL certificate, the configuration change made by `certbot --apache` *should* "just work" although you will want to make sure that it sets `X-Forwarded-Protocol` or else Publ will still generate `http://` URLs for things, which is probably not what you want.

### nginx

Here is an example nginx configuration, e.g. `/etc/nginx/sites-available/example.com`:

```nginx
# http
server {
    listen 80;
    server_name example.com;
    access_log  /var/log/nginx/example.log;

    location / {
        proxy_pass http://unix:/path/to/gunicorn.sock:/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

#https
server {
    listen 443;
    server_name example.com;
    access_log  /var/log/nginx/example.log;
    ssl_certificate     /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    location / {
        proxy_pass http://unix:/path/to/gunicorn.sock:/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Others

The basic premise to configuring any arbitrary httpd to work with Publ:

* Reverse proxy from your vhost to the UNIX socket (or `localhost` port, if UNIX sockets aren't supported)
* On SSL, add `X-Forwarded-Proto $scheme`
* Try to preserve the incoming `Host` and set `X-Forwarded-For` if at all possible

If these are not options, you could see if there is direct support for WSGI from the server instead. However, this usually has security implications, especially with regards to how the image rendition cache works; running as a reverse proxy is almost always the preferred approach.

## Alternatives to gunicorn

### [hypercorn](https://hypercorn.readthedocs.io/)

In some situations, hypercorn has better scaling characteristics than gunicorn. However, it isn't quite as turnkey as gunicorn, as it defaults to tighter security regarding proxies. So, in order to use it with hypercorn, the following changes must be made to your deployment:

1. In order to set the correct socket permissions, either launch it with `-m 0` (giving it the same wide permissions as gunicorn), or ensure that your user shares a group with the webserver process and set that as the parameter to `-g`. My recommendation is to just use `-m 0`, e.g.

    ```
    poetry run gunicorn -b unix:/path/to/socket -m 0 app:app
    ```

2. In order to correctly handle the `X-Forwarded-*` headers, add these lines to the bottom of your `app.py`:

    ```
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    ```

    This should *only* be done if Publ is running behind a fronting proxy; while this is the most common deployment scenario, it is not universal, so Publ does not ship with this enabled by default.

    Additionally, the numbers may need to be adjusted if Publ is running behind multiple forwarding proxies; see [the Flask documentation](https://flask.palletsprojects.com/en/stable/deploying/proxy_fix/) for more information.
