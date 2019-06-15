Title: Python API
Sort-Title: 200 Python API
Path-Alias: /api/python
Date: 2018-06-01 15:48:09-07:00
Entry-ID: 865
UUID: 1ce6bed6-df7a-487a-85a8-8270c35f65cd

The Python-side API when creating a Publ application.

.....

## Library calls

The `publ` library provides the following functions:

* **`publ(name, cfg)`**: Creates a Publ application object.

    `name` is the internal name for the application; this is more or less
    arbitrary although it's useful if you're setting up multiple Publ
    applications for some reason (Note: multiple Publ apps are not currently
    supported). Generally you just pass in `__name__` for this.

    `cfg` is the configuration options for Publ; it is a dictionary which holds
    the following values:

    * **`database_config`**: The parameters sent to PonyORM's [`db.bind()`](https://docs.ponyorm.com/api_reference.html#Database.bind) method. Defaults to an in-memory sqlite database.

    * **`content_folder`**: The directory which contains the root of your site's content files. Defaults to `content`

    * **`template_folder`**: The directory which contains the root of your site's template files. Defaults to `templates`

    * **`static_folder`**: The directory which contains the root of your site's static files. Defaults to `static`

    * **`static_url_path`**: The root path that browsers will be directed to for static content files. Defaults to `/static`. If you want to use a separate CDN/image server/etc., you would configure this to be the URL that would correspond to your static asset directory for the public.

        Note that your image server will need a separate route into your static
        content files, be it through network file storage of some sort or
        through a separate webserver that maps this content directory or the
        like.

    * **`image_output_subdir`**: The subdirectory of `static_folder` that will be used to store the image rendition cache. Defaults to `_img`.

        Be careful not to set this to a directory you want to store static files in, as they risk being deleted.

    * **`index_rescan_interval`**: How frequently Publ should do a maintenance rescan of the content files. Defaults to 7200 (2 hours); set to 0 or `None` to disable.

    * **`timezone`**: The timezone to use for dates with no specified time zone. Defaults to the server's local timezone.

    * **`cache`**: A dictionary with the caching configuration; see the [Flask-Caching documentation](https://pythonhosted.org/Flask-Caching/#configuring-flask-caching) for more information. Defaults to `{}` (i.e. no caching).

    * <span id="markdown_extensions"></span>**`markdown_extensions`**: A list of extensions to use with the Markdown processor; see the [misaka documentation](https://misaka.61924.nl/#extensions) for a list of accepted values. Defaults to `('tables', 'fenced-code', 'footnotes', 'strikethrough', 'highlight', 'superscript', 'math')`.

        Generally you will only want to configure this globally, but you can also override these settings at the template level by passing `markdown_extensions` in as configuration to the [entry properties](115) (`entry.body`, `entry.text`, `entry.title`, etc.).

    Returns an application object.

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
