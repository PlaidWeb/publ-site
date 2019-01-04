Title: Getting started
Sort-Title: 000 Getting Started
UUID: 4dea4c3b-c6ec-4dc0-9f40-b27a91128a60
Entry-ID: 328
Path-Alias: /getting-started
Date: 2018-10-13 15:59:50-07:00

A guide to starting with Publ.

.....

## Installing system requirements

You'll need Python 3 (at least version 3.6) and
[`pipenv`](https://pipenv.org) to be installed.

### macOS

On macOS this is pretty straightforward; after installing
[Homebrew](https://brew.sh) you can install these things with:

```bash
brew install python
pip3 install --user pipenv
```

and then add the following line to your login script (usually
`~/.bash_profile`):

```bash
export PATH=$HOME/Library/Python/3.7/bin:$PATH
```

As an alternative to homebrew you can install Python 3.6 or later from the [Python website](http://python.org) or using your package manager of choice.

### Linux/FreeBSD/etc.

Your distribution probably provides packages for python3; make sure to get
python 3.6 or later, and to also install `pip3` (Ubuntu
keeps this in the `python3-pip` package; other distributions will vary).

Afterwards, you can install `pipenv` with either:

```bash
sudo pip3 install pipenv
```

or

```bash
pip3 install --user pipenv
```

If you do the latter, make sure your pip user directory is on your `PATH`; this
will probably be `$HOME/.local/bin` but it might vary based on your
distribution.

Also, if `pip3` doesn't work, try running just `pip` instead; not all
distributions differentiate between Python 2 and 3 anymore.

### Windows

1. Install [Python](http://python.org)

    When you install, make sure to check the option for "add python to your
    PATH" and if you customize the installation, make sure it installs pip as
    well

2. Install the [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017), making sure to select "Visual C++ build tools" at the very least.

    This is necessary for some of the libraries Publ depends on. (If you already
    have Visual Studio installed with C++ support you can skip this step.)

3. (Optional, but recommended) Install some sort of `bash` environment, such as MinGW. The "git bash" that comes with [Git for Windows](http://git-scm.com) is a pretty good choice.

4. From a command prompt, run `pip install pipenv`


## Making a website

### Copying this one (recommended)

Run the following commands inside a UNIX shell environment (e.g. Terminal on macOS or Linux, or git bash on Windows):

```bash
# Copy the website files
git clone https://github.com/PlaidWeb/Publ-site
cd Publ-site

# Run the setup steps
./setup.sh

# Start the website locally
./run.sh
```

at which point connecting to [`http://localhost:5000`](http://localhost:5000) should show you this website. Note that on the first page load it will take a little while before all of the content is visible -- but you can watch the site build in your terminal window to see it finish.

If you need to run the site on a different port (for example, you get an error like `OSError: [Errno 48] Address already in use
`), you can change this by setting the `PORT` environment variable; for example:

```bash
PORT=12345 ./run.sh
```

will run the site at [`http://localhost:12345`](http://localhost:12345) instead.

On Windows you can also avoid the use of `bash` and can simply double-click the `winsetup.cmd` and `winrun.cmd` files in order. If you want to change the port, edit `run.cmd` with your text editor of choice.

### Setting one up from scratch

#### Creating the environment

To make your own Publ-based site, you'll need to use `virtualenv`+`pip` or
`pipenv` to set up a sandbox and install the `Publ` package to it; I recommend
`pipenv` for a number of reasons but if you're familiar with `virtualenv` or are
using a hosting provider that requires it, feel free to do that instead.

You can copy the `setup.sh` and `run.sh` from the [main site](/github-site), and also `winsetup.cmd` and `winrun.cmd` if you would like to run it on Windows.

If you're using `pipenv` the command would be:

```bash
pipenv --three install Publ
```

and if you're doing the `virtualenv` approach it would be:

```bash
virtualenv env
env/bin/pip3 install Publ
```

Next, you'll need a `main.py` file. Here is a pretty minimal one:

```python
import os
import publ

APP_PATH = os.path.dirname(os.path.abspath(__file__))

config = {
    # Leave this off to do an in-memory database
    'database_config': {
        'provider': 'sqlite',
        'filename': os.path.join(APP_PATH, 'index.db')
    },
}
app = publ.publ(__name__, config)
if __name__ == "__main__":
    app.run(port=os.environ.get('PORT', 5000))
```

Now, you'll need directories for your site content:

```bash
mkdir -p content templates static
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

Now you should have a site running at [`http://localhost:5000`](http://localhost:5000) that does absolutely nothing! Congratulations!

#### Basic templates

The following template files are available from the [publ site repository](https://github.com/PlaidWeb/publ-site/sample-site).

For a fairly minimal site, create the file `templates/index.html`:

```html
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

Now you can finally create a content file; for example, create a file called `first-entry.md` in the `content` directory:

```
Title: My first entry!

This is my first entry on this website.

.....

This is the extended text.
```

After Publ sees the content file, it should now get some extra stuff in the headers, namely a `Date`, an `Entry-ID`, and a `UUID`. These are how Publ tracks the publishing information for the entry itself. It's a good idea to leave them alone unless you know what you're doing.

Anyway, read on for more information about how to build a bigger site!

### What does what

Looking at [the files for this site](/github-site), here are some key things to look at:

* `Pipfile` and `Pipfile.lock`: Configures `pipenv`
* `main.py`: Main "application" that runs the site
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

For more information about templates, see [the manual on template formats](/template-format). The only required templates are `index.html`, `entry.html`, and `error.html`.

For more information about content, see [that manual page](/entry-format).

I also have made [some of my own website templates](https://github.com/PlaidWeb/Publ-templates-beesbuzz.biz) available.

### Putting it on the web

Getting a Publ site online depends a lot on how you're going to be hosting it. If you're savvy with Flask apps you probably know what to do; otherwise, check out the [deployment guides](/deployment) to see if there's anything that covers your usage.

### Next steps

If you do end up using Publ, please let me know so that I can check it out — and maybe add it to a list of featured sites!
