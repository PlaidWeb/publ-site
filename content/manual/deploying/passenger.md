Title: Passenger
Date: 2018-04-03 02:22:07-07:00
Entry-ID: 326
UUID: 45e36baf-9c9a-40bf-9af7-1cbacefda9bd
Sort-Title: 300 Passenger

How to run Publ on a Passenger environment (including Dreamhost)

.....

Deployment using [Phusion Passenger](https://www.phusionpassenger.com/library/walkthroughs/start/python.html) (also known as Passenger WSGI) is fairly straightforward, once you have a python3
environment working. However, on some web hosts, setting up python3 isn't quite obvious.

### Building Python 3

First you need a Python 3 environment. If your hosting provider doesn't provide one (you can check by running `python3` from the command line), there are a few ways to install it yourself.

The easiest way is to use [pyenv](https://github.com/pyenv/pyenv):

```bash
curl https://pyenv.run | bash
exec $SHELL
pyenv update
pyenv install 3.7.6
```

After a while you should be able to verify that you have a working Python 3 installation with e.g.

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
mkdir -p tmp && touch tmp/restart.txt
```
