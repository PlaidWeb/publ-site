Title: Getting started
Date: 2018-04-03 16:24:37-07:00
Entry-ID: 328
UUID: 4dea4c3b-c6ec-4dc0-9f40-b27a91128a60

A guide to starting with Publ.

.....

## Installing system requirements

You'll need Python 3 (at least version 3.6) and [`pipenv`](https://docs.pipenv.org) to be installed.

### macOS

On macOS this is pretty straightforward; after installing [Homebrew](https://brew.sh) you can install these things with:

```bash
brew install python pipenv
```

and then add the following line to your login script (usually `~/.bash_profile`):

```bash
export PATH=$HOME/Library/Python/3.6/bin:$PATH
```

### Other platforms

This should also be possible to do on Linux and Windows; if anyone would like to share how to do it, please [open an issue](http://github.com/fluffy-critter/Publ/issues/new)!

## Obtaining Publ

Now when you open a new terminal you should have pipenv and python3 on your path:

```bash
# which pipenv
/Users/fluffy/Library/Python/3.6/bin/pipenv
# which python3
/usr/local/bin/python3
# python3 --version
Python 3.6.5
```


## Copying this website

The files for this website are in a [separate repository](http://github.com/fluffy-critter/publ.beesbuzz.biz).
You should be able to clone or fork that repository in order to have your own instance of it, and then
you can start a local server for experimenting with:

```bash
./setup.sh    # Install Publ and do various setup steps
./run.sh      # Start running the server locally
```

at which point connecting to `http://localhost:5000` should do what you want. If you
want to run on a different port you can set the `PORT` environment variable, e.g.:

```bash
PORT=12345 ./run.sh
```

## What does what

Looking at the example site, here's the key things to look at:

* `main.py`: Configures the Publ site
* `passenger_wsgi.py`: A Passenger wrapper, used for running the site on Dreamhost
* `templates/`: The site layout files (i.e. how to lay your content out). Some you can look at:
    * `index.html`: What renders when you view a "directory" (e.g. [`/manual`](/manual))
    * `entry.html`: What renders when you look at an individual page (like this one)
    * `feed.xml`: The Atom feed
    * `error.html`: The error page ([for example](/12345))
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

If you do end up using Publ, please let me know so that I can check it out — and maybe add it to a list of featured sites!
