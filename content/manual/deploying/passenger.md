Title: Passenger WSGI
Date: 2018-04-03 02:22:07-07:00
Entry-ID: 326
UUID: 45e36baf-9c9a-40bf-9af7-1cbacefda9bd

How to run Publ on a Passenger WSGI environment (including Dreamhost)

.....

Deployment using Passenger WSGI (as used on several shared hosting providers
such as Dreamhost) is fairly straightforward, once you have a python3
environment working. However, on some web hosts, setting up python3 isn't quite obvious.

### Building Python 3

First you need a Python 3 environment. On most shared hosting providers you can
create one by using `ssh` to log in to your shell account and then downloaded the [Python source
distribution](https://www.python.org/downloads/source/). For example, for version 3.7.0, you'd do:

```bash
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
tar xzvf Python-3.7.0.tgz
```

Then building it is fairly straightforward:

```bash
cd Python-3.7.0
./configure --prefix=$HOME/opt/python-3.7.0 --enable-optimizations
nice -19 make build_all
make install
```

The `nice -19` is to reduce the chances that Dreamhost's process killer kicks in
for the build, and `build_all` builds Python without building unit tests.

At this point you'll want to add Python 3 to the environment, by adding the
following lines to your login script (usually `~/.bash_profile`):

```bash
# python3
export PATH=$HOME/opt/python-3.7.0/bin:$HOME/.local/bin:$PATH
```

Log out and back in (or run the `export` line directly) and you should now have Python 3.7.0 on your path.
You can verify this by typing

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

### Set up the virtual environment

Now it's time to set up your virtual environment for Publ. Again, `ssh` to your webhost and do the following:

```bash
cd (website_directory)
pipenv --three
pipenv install Publ
```

This sets up the virtual environment and installs Publ and its dependencies. Now you need to write a `passenger_wsgi.py` script that tells Passenger how to run it. A fuller example is in the [files for this site](/github-site) but a minimal version is below:

```python
import sys
import os
import subprocess

# hack to keep click happy
os.environ['LANG'] = 'C.UTF-8'
os.environ['LC_ALL'] = 'C.UTF-8'

INTERP = subprocess.check_output(
    ['pipenv', 'run', 'which', 'python3']).strip().decode('utf-8')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())

from main import app as application
```

### Configure the website

Once you get your files on your server, it's generally a matter of telling Passenger where to find the files.
Generally, this involves going to your web host's configuration panel and configuring your website to use Passenger.
Different hosts may have different requirements. Known configurations are below:

#### Dreamhost

Configure your web domain as follows:

* Remove WWW from URL
* Web directory: `/home/(username)/(site file directory)/public`
* HTTPS (via LetsEncrypt): Yes
* Passenger (Ruby/NodeJS/Python apps only): Yes

You will also need to have a `public` directory, ideally with a symbolic link to your `static` directory inside of it; you can set this up by logging in and doing something like:

```bash
cd (website_directory)
mkdir -p public
cd public
ln -s ../static .
```

You will also probably want to create a `.htaccess` file under `public/` with the following contents:

```htaccess
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*\.php)$ /$1.PUBL_PATHALIAS [L]
```

### Care and feeding

Upgrading Publ should just be a matter of `ssh`ing to your host, `cd`ing into the site directory, and running:

```bash
pipenv update
```

After doing this, or after changing any site templates, you'll want to restart your website.
On Dreamhost you do this with:

```bash
cd (website_directory)
mkdir -p tmp    # only necessary the first time
touch tmp/restart.txt
```
