Title: Apache+`mod_proxy` or nginx
Date: 2018-12-16 22:41:45-08:00
Entry-ID: 1278
UUID: 6b0d8b5d-08d2-5ad5-8cf0-13a1c5720586

How to run Publ on an Apache with `mod_proxy` or an nginx server

.....

Configuring Publ to work with Apache or nginx is largely the same either way, the difference being in how you point the server to your Publ instance.

## Running the Publ instance

Your Publ environment needs to have a WSGI server installed. This guide assumes you're using [gunicorn](http://gunicorn.org) although any WSGI server should work. On that note, you'll probably need to install gunicorn into your Publ environment; if you're using pipenv that'll be

```bash
pipenv install gunicorn
```

Next, you need something to launch your site; here are a few options. These all assume that you're declaring your Publ app as `app` from the file `app.py`, per the [getting started guide](328), that `pipenv` was installed using `pip install --user pipenv`, and the Publ site's directory is `/home/USERNAME/example.com`.

### <span id="systemd">systemd</span>

If you're on a UNIX that uses `systemd`, the preferred approach is to run the site as a user service. Here is an example systemd launcher:

```systemd
[Unit]
Description=example.com website

[Service]
Restart=always
WorkingDirectory=/home/USERNAME/example.com
ExecStart=/home/USERNAME/.local/bin/pipenv run gunicorn -b unix:gunicorn.sock app:app
ExecReload=/bin/kill -HUP $MAINPID
StandardOutput=file:/home/USERNAME/logs/example.com/service.log

[Install]
WantedBy=default.target
```

Install this file as e.g. `~/.config/systemd/user/example.com.service` and then you should be able to start the server with:

```bash
systemctl --user enable example.com.service
systemctl --user start example.com
```

and the site should now be up and running on the local port; as long as it's up there should be a socket file named `gunicorn.sock` in the site's directory.

However, this service will only run as long as the user is logged in; in order to make it run persistently, have an admin set your user to "linger" with e.g.:

```bash
loginctl enable-linger USERNAME
```

### cron

If you don't have systemd, or you don't have administrator access, you can use `cron` as a service launcher; first, make a file like `cron-launcher.sh` in your site's
directory:

```bash
#!/bin/sh

cd $(dirname "$0")
flock -n .lockfile $HOME/.local/bin/pipenv run gunicorn -b unix:gunicorn.sock app:app
```

and then run `crontab -e` and add a line like:

```crontab
* * * * * /home/USERNAME/example.com/cron-launcher.sh
```

## Apache

To use this with Apache, you'll need `mod_proxy` installed and enabled.

Here is a basic Apache configuration (e.g. `/etc/apache2/sites-enabled/100-example.com.conf`):

```apache
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
```

You will of course need to edit `ServerName`, `ErrorLog`, and `CustomLog` accordingly, and make sure that the address and port in `ProxyPass` matches your running service as configured in the service launcher, and the `/path/to/gunicorn.sock` must be wherever the socket file is kept (e.g. `/home/USERNAME/example.com/gunicorn.sock`)

### SSL

Here is an example SSL Apache configuration; it can go in the same file as the non-SSL configuration.

```apache
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName example.com

    AcceptPathInfo On
    ErrorLog /path/to/error.log
    CustomLog /path/to/access.log combined

    <Proxy *>
    Order deny,allow
    Allow from all
    </Proxy>

    ProxyPreserveHost On
    RequestHeader set X-Forwarded-Protocol ssl

    ProxyPass / unix:/user/USERNAME/example.com/gunicorn.sock|http://localhost/

    SSLCertificateFile /path/to/fullchain.pem
    SSLCertificateKeyFile /path/to/privkey.pem
</VirtualHost>
</IfModule>
```

Note that this uses the same local connection as the non-SSL version; in fact, you can have arbitrarily many fronting configurations to the same Publ instance, even with different domain names! Publ doesn't mind at all.

If you use [Let's Encrypt](http://letsencrypt.org) to get your certificate, the configuration change made by `certbot --apache` *should* "just work" although you will want to make sure that it sets `X-Forwarded-Protocol` or else Publ will still generate `http://` URLs for things, which is probably not what you want.

## nginx

Here is an example nginx configuration, e.g. `/etc/nginx/sites-available/example.com`:

```nginx
  server {
    listen 80;
    server_name example.com;
    access_log  /var/log/nginx/example.log;

    location / {
        proxy_pass http://unix:/path/to/gunicorn.sock:/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }
```
