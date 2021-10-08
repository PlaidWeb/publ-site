Title: Getting started
Sort-Title: 001 Getting Started
UUID: 4dea4c3b-c6ec-4dc0-9f40-b27a91128a60
Entry-ID: 328
Path-Alias: /getting-started
Date: 2018-10-13 15:59:50-07:00

A guide to starting with Publ

.....

This guide will walk you through setting up Publ on your local computer so that
you can build and run a site that runs locally. To learn how to run this website
on a webserver, see the [deployment guides](deploying/).

## Installing system requirements

You'll need [Python](https://python.org) (at least version 3.6), and it's a good
idea to use a virtual environment manager as well. Any such manager
(`virtualenv`, `pipenv`, `poetry`) is fine; the following instructions all
assume [`poetry`](https://python-poetry.org).

### macOS

On macOS this is pretty straightforward; after installing
[Homebrew](https://brew.sh) you can install Python with:

```bash
brew install python
```

As an alternative to homebrew you can install Python from the [Python
website](http://python.org), using your package manager of choice, or using
[pyenv](https://github.com/pyenv/pyenv-installer).

Afterwards, install [Poetry](https://python-poetry.org) per the [documentation](https://python-poetry.org/docs/).


### Linux/FreeBSD/etc.

Your distribution probably provides packages for python3; make sure to get
python 3.6 or later, and to also install `pip3`.

Afterwards, install [Poetry](https://python-poetry.org) per the [documentation](https://python-poetry.org/docs/).

### Windows

1. Install [Python](http://python.org)

    When you install, make sure to check the option for "add python to your
    PATH" and if you customize the installation, make sure it installs pip as
    well

2. Install [Visual Studio](https://visualstudio.microsoft.com/downloads/),
making sure to select "Visual C++ build tools" at the very least.

    This is unfortunately necessary for some of the libraries Publ depends on.
    You can either install the Visual Studio Community Edition, or you can
    install just the build tools (under the "Tools for Visual Studio" section).

3. (Optional, but recommended) Install some sort of `bash` environment, such as
MinGW.

    The "git bash" that comes with [Git for Windows](http://git-scm.com) is a
    pretty good choice.

4. Install [Poetry](https://python-poetry.org) per the [documentation](https://python-poetry.org/docs/)

## Making a website

### Copying this one (recommended)

1. Clone a local copy of [this website repository](https://github.com/PlaidWeb/Publ-site).

    You can use the command line (e.g. `git clone https://github.com/PlaidWeb/Publ-site`) or you can use your favorite git frontend for this (such as GitHub Desktop).

2. Launch the website locally

    On macOS and Linux, or on Windows using git bash, run `./run.sh` (also from the same directory).

    On Windows, double-click the `winrun.cmd` file (which may appear as just `winrun`)

After the site reindex completes, connecting to
[`http://localhost:5000`](http://localhost:5000) should show you this website.

If you need to run the site on a different port (for example, you get an error
like `OSError: [Errno 48] Address already in use`), you can change this by
setting the `FLASK_RUN_PORT` environment variable; for example:

```bash
FLASK_RUN_PORT=12345 ./run.sh
```

will run the site at [`http://localhost:12345`](http://localhost:12345) instead.

### Setting one up from scratch

#### Creating the environment

To make your own Publ-based site, you'll want to create a new virtual
environment to hold Publ in. As above, the following instructions assume
`poetry`, although any other manager is fine.


```bash
mkdir example.site
cd example.site
poetry init -n
poetry add publ
```

Next, you'll need an `app.py` file. Here is a pretty minimal one:

```python
!app.py
import os
import publ

config = {
    'database_config': {
        'provider': 'sqlite',
        'filename': 'index.db'
    },
}
app = publ.publ(__name__, config)
```

Now, you'll need directories for your site content; create folders named
`content`, `templates`, and `static` in the same directory as `app.py`. From the
command line you can type:

```bash
mkdir -p content templates static
```

Then you can launch your (not yet very functional) site with

```bash
poetry run flask run
```

Now you should have a site running at
[`http://localhost:5000`](http://localhost:5000) that does absolutely nothing!
Congratulations!

Also, feel free to copy the `run.sh` and/or `winrun.cmd` from [this
website](/github-site) which will better automate subsequent setup steps.

#### Basic templates

For a fairly minimal site, create the file `templates/index.html`:

```html
!templates/index.html
<!DOCTYPE html>
<html>
<head>
<title>{{ category.name or 'My simple site' }}</title>
</head>

<body>
<h1>{{ category.name or 'My simple site'}}</h1>
{% for entry in view.entries %}
<article>
<h2><a href="{{entry.permalink}}">{{ entry.title }}</a></h2>
{{ entry.body }}

{% if entry.more %}
<a rel="more" href="{{entry.permalink}}">More...</a>
{% endif %}
</article>
{% endfor %}

</body>
</html>
```

and `templates/entry.html`:

```html
!templates/entry.html
<!DOCTYPE html>
<html>
<head>
<title>{{ entry.title }}</title>
</head>

<body>
<h1><a href="{{category.link}}">{{ category.name or 'My simple site' }}</a></h1>
<article>
<h2>{{ entry.title }}</h2>

{{ entry.body }}
{{ entry.more }}
</article>

</body>
</html>
```

Now you can finally create a content file; for example, create a file called
`first-entry.md` in the `content` directory:

```
!content/first-entry.md
Title: My first entry!

This is my first entry on this website.

.....

This is the extended text.
```

After Publ sees the content file, it should now get some extra stuff in the
headers, namely a `Date`, an `Entry-ID`, and a `UUID`. These are how Publ tracks
the publishing information for the entry itself. It's a good idea to leave them
alone unless you know what you're doing.

Anyway, read on for more information about how to build a bigger site!

### What does what

Looking at [the files for this site](/github-site), here are some key things to
look at:

* `pyproject.toml` and `poetry.lock`: Package dependencies
* `app.py`: Main "application" that runs the site
* `Procfile`: Configures the site to run on [Heroku](http://heroku.com)
* `templates/`: The site layout files (i.e. how to lay your content out). Some you can look at:
    * `index.html`: What renders when you view a category (e.g. [`/manual/`](/manual/))
    * `entry.html`: What renders when you look at an individual page (like this one)
    * `feed.xml`: The Atom feed
    * `error.html`: The error page ([for example](/_broken_link_))
    * `sitemap.xml`: Produces a sitemap for search engines
* `content/`: The content on this site (for example, this page's content is stored in `content/manual/Getting started.md`)
* `static/`: Things that never change; for example, stylesheets and Javascript libraries. For example, this site has:
    * `style.css`: the global stylesheet
    * `lightbox`: A library used for presenting images in a gallery ([example page](/yay-cats-wooooo))
    * `pygments.default.css`: A stylesheet used by the Markdown engine when formatting code

For more information about templates, see [the manual on template
formats](/template-format). The only absolutely required template is
`index.html`, but it's a good idea to also provide an `entry.html`.

For more information about content, see [that manual page](/entry-format).

I also have made [some of my own website
templates](https://github.com/PlaidWeb/Publ-templates-beesbuzz.biz) available.

### Putting it on the web

Getting a Publ site online depends a lot on how you're going to be hosting it.
If you're savvy with Flask apps you probably know what to do; otherwise, check
out the [deployment guides](deploying/) to see if there's anything that covers
your usage.

