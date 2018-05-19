Title: Getting started
UUID: 4dea4c3b-c6ec-4dc0-9f40-b27a91128a60
Date: 2018-04-03 16:24:37-07:00
Entry-ID: 328
Path-Alias: /getting-started

A guide to starting with Publ.

.....

## Installing system requirements

You'll need Python 3 (at least version 3.5, but 3.6 is recommended) and
[`pipenv`](https://pipenv.org) to be installed.

### macOS

On macOS this is pretty straightforward; after installing
[Homebrew](https://brew.sh) you can install these things with:

```bash
brew install python pipenv
```

and then add the following line to your login script (usually
`~/.bash_profile`):

```bash
export PATH=$HOME/Library/Python/3.6/bin:$PATH
```

### Linux/FreeBSD/etc.

Your distribution probably provides packages for python3; make sure to get
python 3.5 or later (ideally 3.6 or later), and to also install `pip3` (Ubuntu
keeps this in the `python3-pip` package; other distributions will vary).

Afterwards, you can install `pipenv` with either:

```bash
sudo pip3 install pipenv
```

or

```bash
pip3 install --user pipenv
```

If you do the latter, make sure your pip user directory is on your PATH; this
will probably be `$HOME/.local/bin` but it might vary based on your
distribution.

Also, if `pip3` doesn't work, try running just `pip` instead; not all
distributions differentiate between Python 2 or 3 anymore.

### Windows

==Note:== I haven't yet managed to get Publ working from Windows. Perhaps someone
with more Windows and Python experience could [help me out](https://github.com/fluffy-critter/Publ/issues/97)?

1. Install [Python](http://python.org)

    When you install, make sure to check the option for "add python to your
    PATH" and if you customize the installation, make sure it installs pip as
    well

2. Install the [Visual Studio Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools)

    This is necessary for some of the libraries Publ depends on. If you already
    have Visual Studio installed with C++ support you can probably skip this
    step.

3. From the command prompt, run `pip install pipenv`

## Making a website

### Copying this one (recommended)

The files for this website are in a [separate repository](/github-site). You
should be able to clone or fork that repository in order to have your own
instance of it, and then you can start a local server for experimenting with:

```bash
./setup.sh    # Install Publ and do various setup steps
./run.sh      # Start running the server locally
```

at which point connecting to `http://localhost:5000` should do what you want. If
you want to run on a different port you can set the `PORT` environment variable,
e.g.:

```bash
PORT=12345 ./run.sh
```

#### Windows users

If you don't have any sort of UNIX commandline (minGW, Linux Subsystem for
Windows, Cygwin, etc.), then instead of `setup.sh` run:

    pipenv install

and instead of `run.sh` run:

    pipenv run python3 main.py

You could also put these in `.cmd` files if you like.

### Setting one up from scratch

To make your own Publ-based site, you'll need to use `virtualenv`+`pip` or
`pipenv` to set up a sandbox and install the `Publ` package to it; I recommend
`pipenv` for a number of reasons but if you're familiar with `virtualenv` or are
using a hosting provider that requires it, feel free to do that instead.

If you're using `pipenv` the command would be:

```bash
pipenv install Publ
```

and if you're doing the `virtualenv` approach it would be:

```bash
virtualenv env
. env/bin/activate
pip install Publ
```

(Windows users would type `env\scripts\activate` instead of `. env/bin/activate`.)

Next, you'll need a `main.py` file. The absolute minimum for that is simply:

```python
import os
import publ

config = {
    # Leave this off to do an in-memory database
    'database': 'sqlite:///index.db'
}
app = publ.publ(__name__, config)
if __name__ == "__main__":
    app.run(port=os.environ.get('PORT', 5000))
```

Then you can launch your (not yet very functional) site with

```bash
pipenv run python3 main.py
```

if you're using `pipenv`, or

```bash
env/bin/python3 main.py
```

if you're using `virtualenv`.

Now you have a site running at `http://localhost:5000` that does absolutely nothing! Congratulations!

## What does what

Looking at the [example site](/github-site), here's the key things to look at:

* `Pipfile`: Configures `pipenv`
* `main.py`: Configures the Publ site
* `passenger_wsgi.py`: A Passenger wrapper, used for running the site on Dreamhost and other Passenger-WSGI hosting providers
* `Procfile`: Configures the site to run on Heroku (and possibly other providers)
* `templates/`: The site layout files (i.e. how to lay your content out). Some you can look at:
    * `index.html`: What renders when you view a "directory" (e.g. [`/manual`](/manual))
    * `entry.html`: What renders when you look at an individual page (like this one)
    * `feed.xml`: The Atom feed
    * `error.html`: The error page ([for example](/_broken_link_))
    * `sitemap.xml`: Produces a sitemap for search engines
* `content/`: The content on this site (for example, this page's content is stored in
    `content/manual/getting started.md`)
* `static/`: Things that never change; for example, stylesheets and Javascript libraries. For example, this site has:
    * `style.css`: the global stylesheet
    * `lightbox`: A library used for presenting images in a gallery ([example page](/yay-cats-wooooo))
    * `pygments.default.css`: A stylesheet used by the Markdown engine when formatting code

For more information about templates, see [the manual on template formats](/template-format).

For more information about content, see [that manual page](/entry-format).

## Putting it on the web

Publ is intended to be run on a containerized platform such as [Heroku](http://heroku.com); the free tier should
be sufficient for at least basic experimentation. Or if you have hosting with a provider that supports Passenger WSGI
you can try deploying there; I have a very basic guide for [installing on Dreamhost](/dreamhost), and information
on Heroku is coming eventually.

If you're running your own server (Apache or nginx), you should be able to configure this as a WSGI application
or using a reverse proxy. More information will come on that later, hopefully.

## Next steps

If you do end up using Publ, please let me know so that I can check it out — and maybe add it to a list of featured sites!
