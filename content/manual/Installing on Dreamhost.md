Title: Installing on Dreamhost
Date: 2018-04-03 02:22:07-07:00
Entry-ID: 326
UUID: 45e36baf-9c9a-40bf-9af7-1cbacefda9bd
Path-Alias: /dreamhost

A quick guide to getting Publ running on Dreamhost's Passenger WSGI environment.

.....


Deployment to Dreamhost is fairly straightforward, once you have a python3
environment working. However, setting up python3 isn't quite obvious, and
[Dreamhost's own instructions](https://help.dreamhost.com/hc/en-
us/articles/115000702772-Installing-a-custom-version-of-Python-3) are incomplete
and don't include [`pipenv`](https://docs.pipenv.org) (which, to be fair, is a
fairly recent addition to the ecosystem).

These instructions should be easy to adapt to any other shared-hosting provider
that provides WSGI. If you have successfully gotten a site running on another
WSGI-based hosting provider, please feel free to [clone and modify this
site](https://github.com/fluffy-critter/publ.beesbuzz.biz) and submit a pull
request.

## Building Python 3

First you need a Python 3 environment. On Dreamhost you can create one by using
`ssh` to your Dreamhost shell account and then downloaded the [Python source
distribution](https://www.python.org/downloads/source/):

```bash
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
tar xzvf Python-3.6.5.tgz
```

Then building it is fairly straightforward:

```bash
cd Python-3.6.5
./configure --prefix=$HOME/opt/python-3.6.5 --enable-optimizations
nice -19 make build_all
make install
```

The `nice -19` is to reduce the chances that Dreamhost's process killer kicks in
for the build, and `build_all` builds Python without building unit tests (which
Dreamhost's process killer severely dislikes).

At this point you'll want to add Python 3 to the environment, by adding the
following lines to your `~/.bash_profile`:

```bash
# python3
export PATH=$HOME/opt/python-3.6.5/bin:$HOME/.local/bin:$PATH
```

Log out and back in (or run the `export` line directly) and you should now have Python 3.6 on your path, you can verify this by typing

```bash
python3 --version
pip3 --version
```

If all worked well, you can now install `pipenv`:

```bash
pip3 install --user pipenv
```

and, optionally, add this line to your `~/.bash_profile` to get better shell
tab completion:

```bash
eval "$(pipenv --completion)"
```

## Running Publ on Dreamhost

This guide simply assumes that you are deploying the files for this site using
its Git repository. For your own site you will probably be uploading your own
content directory in some other way.

First, clone this site's files into your home directory and deploy its virtual environment:

```bash
git clone https://github.com/fluffy-critter/publ.beesbuzz.biz
cd publ.beesbuzz.biz
./setup.sh
```

Next, open up the [Dreamhost panel](https://panel.dreamhost.com) and
create a new domain, with the following configuration:

* Remove WWW from URL
* Web directory: `/home/username/publ.beesbuzz.biz/public`
* HTTPS (via LetsEncrypt): Yes
* Passenger (Ruby/NodeJS/Python apps only): Yes

After Dreamhost's configuration robot does its thing, you should now have a copy of this website running on whatever
domain you've configured.

If you would like to make your own site (which you probably do!) I recommend borrowing this site file's `passenger_wsgi.py` and `setup.sh`, which provide the WSGI configuration and environment setup for running Publ on Dreamhost.

## Migrating a legacy site

If you have an older site that you want to move over to Publ, you don't have to do it all at once.
Dreamhost's Passenger configuration puts an "overlay" of the `public/` directory on top of the
Passenger application; so, you can change your site configuration to enable Passenger, and then move your
existing content into the `public/` directory under the domain name, and it will continue to be served up.

Then, as you add content into Publ, you can [add `Path-Alias` headers to your entries](/entry-format#path-alias)
to map legacy URLs to your new URL scheme. (You can also put such redirections into your `.htaccess` in the form
of `RewriteRule` but this is a lot easier to manage and gives better performance.)

If you would like to map legacy URLs programmatically you can add such mappings into the `.htaccess` file, or you can
use the [Python API](/api/python) to add regular expression mapping rules (with `path_alias_regex`) in your `main.py`. Using `path_alias_regex` is recommended as it will work anywhere Publ does and also provides slightly better performance.

### Using Path-Alias to redirect old PHP URLs

Dreamhost has (as of 2018/04/06) a [misconfiguration in Passenger](https://github.com/fluffy-critter/Publ/issues/19) which prevents `Path-Alias` from working correctly on legacy PHP URLs out of the box. However, there is a simple workaround;
create a `public/.htaccess` file which contains the following lines:

```htaccess
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*\.php)$ /$1.PUBL_PATHALIAS [L]
```

This will redirect any request to a non-existent PHP script to a special URL routing rule that
tells Publ to treat it as a path-alias immediately.

## Upgrading the code

To get the latest versions of all library dependencies you can run the following from your site directory:

```bash
pipenv update
./setup.sh
```

