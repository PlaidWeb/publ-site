Title: Python API
Sort-Title: 200 Python API
Path-Alias: /api/python
Date: 2018-06-01 15:48:09-07:00
Entry-ID: 865
UUID: 1ce6bed6-df7a-487a-85a8-8270c35f65cd

The Python-side API when creating a Publ application.

.....

## Library calls

The `publ` library provides the `publ.Publ` class. Its constructor is called as follows:

* **`Publ(name, cfg)`**: Creates a Publ application object.

    `name` is the internal name for the application; this is more or less
    arbitrary although it's useful if you're setting up multiple Publ
    applications for some reason (Note: multiple Publ apps are not currently
    supported). Generally you just pass in `__name__` for this.

    `cfg` is the configuration options for Publ; it is a dictionary which holds
    the following values:

    * **`database_config`**: The parameters sent to PonyORM's [`db.bind()`](https://docs.ponyorm.com/api_reference.html#Database.bind) method. Defaults to an in-memory sqlite database.
    * **`index_rescan_interval`**: How frequently Publ should do a maintenance rescan of the content files. Defaults to 7200 (2 hours); set to 0 or `None` to disable.

    * **`content_folder`**: The directory which contains the root of your site's content files. Defaults to `content`
    * **`template_folder`**: The directory which contains the root of your site's template files. Defaults to `templates`
    * **`static_folder`**: The directory which contains the root of your site's static files. Defaults to `static`
    * **`static_url_path`**: The root path that browsers will be directed to for static content files. Defaults to `/static`. If you want to use a separate CDN/image server/etc., you would configure this to be the URL that would correspond to your static asset directory for the public (and configure some other mechanism for that external service to actually retrieve your origin content).

    * **`image_output_subdir`**: The subdirectory of `static_folder` that will be used to store the image rendition cache. Defaults to `_img`.

        Be careful not to set this to a directory you want to store static files in, as they risk being deleted.

    * **`image_cache_interval`**: How frequently to clean the image rendition cache, in seconds. Defaults to 7200 (3 hours).
    * **`image_cache_age`**: The maximum age of image renditions to keep, in seconds. Defaults to one month.
    * **`image_render_threads`**: The maximum number of threads to use for image rendering; defaults to the number of CPUs in the system. Set this to `None` to use the [Python default for `ThreadPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor).
    * **`timezone`**: The timezone to use for dates with no specified time zone. Defaults to the server's local timezone.

    * <span id="cache">**`cache`**</span>: A dictionary with the page caching configuration; see the [deplyment guide](20) for more information. Defaults to `{}` (i.e. no caching).

    * <span id="markdown_extensions">**`markdown_extensions`**: A list of extensions to use with the Markdown processor; see the [misaka documentation](https://misaka.61924.nl/#extensions) for a list of accepted values. Defaults to `('tables', 'fenced-code', 'footnotes', 'strikethrough', 'highlight', 'superscript', 'math')`.</span>

        Generally you will only want to configure this globally, but you can also override these settings at the template level by passing `markdown_extensions` in as configuration to the [entry properties](115) (`entry.body`, `entry.text`, `entry.title`, etc.).

    * **`auth`**: The configuration values for the [authentication system](authentication.md#auth).  Defaults to no configuration.
    * **`user_list`**: The filename of the configuration file that stores the user configuration. Defaults to `users.cfg`
    * **`admin_group`**: The name of the user group that will have administrative access; defaults to `admin`
    * **`auth_log_prune_interval`**: How frequently to clean out the authentication log, in seconds. Defaults to 3600 (one hour).
    * **`auth_log_prune_age`**: The maximum age of authentication log entries to keep, in seconds. Defaults to one month.
    * **`max_token_age`**: The expiry time for [AutoAuth](https://indieweb.org/AutoAuth) tokens, in seconds. Defaults to one hour.

## Application object

A `Publ` application object is an extension of a [Flask application object](http://flask.pocoo.org/docs/1.0/api/#application-object);
you can do all the same things to it as you could to a Flask object, although it's a good idea to not modify any of the configuration
values that Publ expects to see.

This mostly exists to provide the `@path_alias_regex` decorator and its related `add_path_regex` function; here is an example from [my site](https://beesbuzz.biz), used to remap legacy URLs (like `/d/20060606.php`) to newer URLs (like `/comics/?date=20060606`):

```python
app = publ.publ(__name__, {})

@app.path_alias_regex(r'/d/([0-9]{8}(_w)?)\.php')
def redirect_date(match):
    return flask.url_for('category', category='comics', date=match.group(1)), True
```

The path alias function takes a [`re.match` object](https://docs.python.org/3.5/library/re.html#match-objects) and returns a tuple of `(url, is_permanent)`. This function can also make use of the various Flask request context things (e.g. `request.args`) and if it doesn't want to redirect after all it can return `(None,None)`.

Note that you can also use `@app.route` like any typical Flask application, but due to Flask routing rules it may not work with variadic routes. For example:

```python
@app.route('/favicon.ico')
def favicon():
    """ Static route should work """
    return flask.send_file('favicon.ico')

```python
@app.route('/foo/<path:path>')
def redirect_foo(path):
    """ Dynamic route will likely fail, as the 'category' route is a stronger match """
    return "We are invisible: {}".format(path)
```

is unlikely to work. Currently Flask doesn't provide any clean mechanism for adjusting a routing rule's priority; [this StackOverflow question](https://stackoverflow.com/questions/17135006/url-routing-conflicts-for-static-files-in-flask-dev-server) discusses the issue and some possible workarounds.

## Sample `app.py`

This is based on the `app.py` that configures [beesbuzz.biz](https://beesbuzz.biz). It
configures basic logging, sets the in-process cache to store up to 500 items for
up to 300 seconds, and only does a maintenance rescan once per day. It also maps
a bunch of legacy URLs as well as forwarding ActivityPub requests to fed.brid.gy's
handler.

```python
""" Main Publ application """

import os
import logging
import logging.handlers

import publ
import flask

if os.path.isfile('logging.conf'):
    logging.config.fileConfig('logging.conf')
else:
    if not os.path.isdir('logs'):
        os.makedirs('logs')
    logging.basicConfig(level=logging.INFO,
                        handlers=[
                            logging.handlers.TimedRotatingFileHandler(
                                'logs/publ.log', when='D'),
                            logging.StreamHandler()
                        ],
                        format="%(levelname)s:%(threadName)s:%(name)s:%(message)s")

logging.info("Setting up")

APP_PATH = os.path.dirname(os.path.abspath(__file__))

config = {
    'database_config': {
        'provider': 'sqlite',
        'filename': os.path.join(APP_PATH, 'index.db')
    },
    'timezone': 'US/Pacific',
    'cache': {
        'CACHE_TYPE': 'simple',
        'CACHE_DEFAULT_TIMEOUT': 300,
        'CACHE_THRESHOLD': 500
    } if not os.environ.get('FLASK_DEBUG') else {},
    'index_rescan_interval': 86400
}

app = publ.publ(__name__, config)


@app.route('/favicon.ico')
def favicon():
    """ Send the favicon.ico file directly from this directory """
    return flask.send_file('favicon.ico')


@app.path_alias_regex(r'/d/([0-9]{8}(_w)?)\.php')
def redirect_date(match):
    ''' legacy comic url '''
    return flask.url_for('category', category='comics', date=match.group(1)), True


@app.path_alias_regex(r'/blog/e/')
def redirect_blog_entry(match):
    ''' missing blog entry -- put up the apology page '''
    return flask.url_for('entry', entry_id=7821), False


@app.path_alias_regex(r'/\.well-known/(host-meta|webfinger).*')
def redirect_bridgy(match):
    ''' support ActivityPub via fed.brid.gy '''
    return 'https://fed.brid.gy' + flask.request.full_path, False

if __name__ == "__main__":
    app.run(port=os.environ.get('PORT', 5000))
```

## <span id="endpoints"></span>Flask endpoints

If you're writing Python code that extends Publ, you might need to use `flask.url_for`.
Here are Publ's usable endpoints:

* **`category`**: Routes to a category page; options are:
    * `category`: The category's path
    * `template`: The template to render
    * The [pagination parameters for `get_view()`](/api/view#subviews)

* **`entry`**: Routes to an entry page; options are:
    * `entry_id`: The numeric ID of the entry (this is the only one that's
        useful to specify in `url_for`)
    * `slug_text`: The SEO slug text
    * `category`: The category the entry lives in

* **`login`**: Routes to the login page; options are:
    * `redir`: The path to redirect to after login completes.

        Note that this must not start with a `/`. Typical usage will be something like:

        ```
        {# login and redirect back to this page #}
        {{ url_for('login', redir=request.full_path[1:]) }}

        {# login and redirect to a specific entry #}
        {{ url_for('login', redir=url_for('entry', entry_id=12345)[1:])}}
        ```

        The `[1:]` is to trim the initial `/` off the path.
    * `me`: An identity to initiate sign-in as. This is equivalent to submitting
        the login form with this value set, and is only really useful for testing.

* **`logout`**: Routes to the logout page; takes the `redir` option with the same
    usage as `login`.

`login` and `logout` have a helper available in `publ.utils.auth_endpoint`, which
simplifies the usage of the endpoints; it takes an endpoint name and returns a function
which routes to that endpoint with an optional redirection parameter. If no redirection
parameter is provided, it defaults to `flask.request.full_path`.

```python
import publ.utils

# get the login helper
login_helper = publ.utils.auth_endpoint('login')

# log in and redirect back to the current page
flask.redirect(login_link())

# log in and redirect to a different page
flask.redirect(login_link('/path/to/something'))

# get the logout helper
logout_helper = publ.utils.auth_endpoint('logout')

# log out and redirect to the same page
flask.redirect(logout_link())

# log out and redirect to server root
flast.redirect(logout_link('/'))
```

Also note that the redirection target *must* be a local URL; external URLs will
not work. (This prevents your site from being used as a
malicious URL redirector.)