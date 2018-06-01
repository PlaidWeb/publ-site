Title: Publ Python API
Path-Alias: /api/publ

The Python-side API when creating a Publ application.

.....

## Library calls

The `publ` library provides the following functions:

* **`publ(name, cfg)`**: Creates a Publ application object.

    `name` is the internal name for the application; this is more or less
    arbitrary although it's useful if you're setting up multiple Publ
    applications for some reason. (Note: multiple Publ applications are [not
    currently supported](https://github.com/fluffy-critter/Publ/issues/113).)
    Generally you just pass in `__name__` for this.

    `cfg` is the configuration options for Publ; it is a dictionary which holds
    the following values:

    * **`database`**: The database connection string for the content index; see the [Peewee documentation](http://peewee.readthedocs.io/en/latest/peewee/playhouse.html#database-url) for its format. You will probably want this to be `'sqlite:///index.db'` or the like. Default: `'sqlite:///:memory:'`.

    * **`content_folder`**: The directory which contains the root of your site's content files. Defaults to `content`

    * **`template_folder`**: The directory which contains the root of your site's template files. Defaults to `templates`

    * **`static_folder`**: The directory which contains the root of your site's static files. Defaults to `static`

    * **`static_url_path`**: The root path that browsers will be directed to for static content files. Defaults to `/static`. If you want to use a separate CDN/image server/etc., you would configure this to be the URL that would correspond to your static asset directory for the public.

        Note that your image server will need a separate route into your static
        content files, be it through network file storage of some sort or
        through a separate webserver that maps this content directory or the
        like.

    * **`image_output_subdir`**: The subdirectory of `static_folder` that will be used to store the image rendition cache. Defaults to `_img`.

    * **`index_rescan_interval`**: How frequently Publ should do a maintenance rescan of the content files. Defaults to 7200 (2 hours); set to 0  or None to disable.

    * **`timezone`**: The timezone to use for dates with no specified time zone. Defaults to the server's local timezone.

    * **`cache`**: A dictionary with the caching configuration; see the [Flask-Caching documentation](https://pythonhosted.org/Flask-Caching/#configuring-flask-caching) for more information. Defaults to `{}` (i.e. no caching).

    Returns an application object.

## Application object

A `Publ` application object is an extension of a [Flask application object](http://flask.pocoo.org/docs/1.0/api/#application-object);
you can do all the same things to it as you could to a Flask object, although it's a good idea to not modify any of the configuration
values that Publ expects to see.

This mostly exists to provide the `@path_alias_regex` decorator and its related `add_path_regex` function; here is an example from [my site](https://beesbuzz.biz), used to remap legacy URLs (like `/d/20060606.php`) to newer URLs (like `/comics/?date=20060606`):

```python
app = publ.publ(__main__, {})

@app.path_alias_regex(r'/d/([0-9]{8}(_w)?)\.php')
def redirect_date(match):
    return flask.url_for('category', category='comics', date=match.group(1)), True
```

The path alias function takes a [`re.match` object](https://docs.python.org/3.5/library/re.html#match-objects) and returns a tuple of `(url, is_permanent)`. This function can also make use of the various Flask request context things (e.g. `request.args`) and if it doesn't want to redirect after all it can return `(None,None)`.
