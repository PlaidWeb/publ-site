Title: Templating Guide
Path-Alias: /template-format
Path-Alias: /template-api
Date: 2018-04-02 18:03:58-07:00
Entry-ID: 324
UUID: cbb977df-7902-4621-af9b-36ab44401748

A guide to building templates for Publ.

.....

Publ templates use the [Jinja2](http://jinja.pocoo.org) templating system; please
see its references for the general syntax of template files.

There are three kinds of page in Publ: entry, category, and error.

## How templates work

### Short version

When someone requests a page, Publ finds the most-specific template
that matches, and uses that to render the page.

### Long version

When someone requests a page, Publ looks up whether it's a category view or an
entry. Category views look something like
`http://mysite.com/art/photos/seattle/` or `http://mysite.com/blog/minimal`.
Entry views look something like `http://mysite.com/art/photos/1529-unwelcome-visitor`.

Every view has a category associated with it; for example,
`http://mysite.com/art/photos/1529-unwelcome-visitor` is in the `art/photos`
category (i.e. all the stuff between the website address and the entry ID, not
including the `/`s at either end), and `http://mysite.com/blog/minimal` is in
the `blog` category; the category is basically everything between the server
name and the last `/` (in this case, `minimal` is the view).

When you see an entry, there is only one possible template that it chooses,
`entry`. When you see a category, if there's a view indicated, it uses that view
name; otherwise it uses the `index` view.

(The category can be blank, incidentally; `http://mysite.com/` shows you the
(`index` view on the empty category.)

<span id="template-mapping"></span>Anyway, given the category and view name, Publ looks
for the closest matching template, by starting out in the template directory
that matches the category name, and then going up one level until it finds a
matching template. And a template will match based on either the exact name, or
the name with `.html`, `.htm`, `.xml`, or `.json` added to the end.

So for example, if you ask for `http://mysite.com/music/classical/baroque/feed`,
it will look for a template file named `feed`, `feed.html`, `feed.htm`,
`feed.xml`, or `feed.json`, in the directories
`templates/music/classical/baroque`, `templates/music/classical`,
`templates/music`, and `templates`, in that order, returning the first one that
matches. (If no templates match, it shows an error page.)

Note that the default names of `entry` and `index` can be overridden on a [per-entry](/entry-format#template-override) or
[per-category](/category-format#template-override) basis.

#### Error templates

A note on error templates: Error pages *generally* get handled by whatever
matches the `error` template; however, in the case of a specific status code, it
will also look for a template named based on that code and its category. For example, a 404 error
will try to render the `404` template first, then try `400`, then finally `error`.
(And of course this can be `404.html`, `404.xml`, `404.json`, and so on,
although in most cases you'll probably be doing it as HTML.)

#### Login/logout template

Unlike most templates, `login.html` and `logout.html` do not support per-category overrides.

#### Generating CSS files

You can also use the template system to generate CSS, which is useful for having
your CSS files reference other assets via `static()` or `image()`. This also
makes it quite simple to create CSS templates that inherit from and override
other CSS templates; for example, if you have the file `templates/style.css`,
you can have `templates/blog/style.css` that looks like:

```css
@import url('../style.css');

body { background: red; }
```

and then your HTML templates need only refer to the stylesheet using, for
example:

```html
<link rel="stylesheet" href="style.css" />
```

## Special templates

*Technically* no template is actually required, but in order to have a
functioning site, you should have, at the very least, the following top-level
templates:

* `index.html`: the default category view
* `entry.html`: the default entry view

The following templates are optional but recommended; if they are not provided, Publ will use a built-in default:

* `error.html`: the error handler
* `login.html`: the login page
* `logout.html`: the interstitial logout page, if someone visits the logout page via link or manual URL entry (rather than a form submission)
* `unauthorized.html`: the error page for attempting to access an entry that the logged-in user doesn't have access to

### Template naming and overrides

Publicly-visible templates' names must start with a letter, and should only
consist of URL-friendly characters (alphanumerics, periods, dashes, and
underscores).

Numeric error templates are not considered publicly-visible.

If a template's name begins with `_` the template will be considered "private;"
it will be available internally (such as to `Entry-Template`,`Index-
Template`, or [`get_template()`](#get-template)) but it will not be available to the world at large. So, for example,
if you want to override your site's main page you can create a file like
`/content/mainpage.cat`:

```
Name: My website
Index-Template: _main_page
```

which will cause it to render with the template `templates/_main_page.html`, but
will not allow other URLs e.g. `/blog/_main_page` to use this template.

Simiarly, it is highly recommended that `Entry-Template` overrides use this
convention, as it usually does not make sense to render an entry template in a
category context.

## Custom filters

Publ provides the following custom filters for use in templates.

### <span id="strip_html">`strip_html(text, allowed_tags=None, allowed_attrs=None, remove_elements=None)`</span>

This filter allows conditional stripping of HTML elements, similar to the built-in [`striptags`](https://jinja.palletsprojects.com/en/2.11.x/templates/#striptags)
filter except with a bit more flexibility:

* `allowed_tags`: a string or list of strings for tags to preserve in the output
* `allowed_attrs`: a string or list of strings for attributes to preserve in preserved tags
* `remove_elements`: a string or list of strings for tags to completely remove, including their children and text content

For example, with the following template:

```jinja2
{{ entry.body | strip_html(allowed_tags='a', allowed_attrs=['href', 'src'], remove_elements='del') }}
```

and the following entry body:

```markdown
[This *is* a ~~text~~ test](http://example.com/ "hello")
```

the template output will be similar to:

```html
<a href="http://example.com/">This is a test</a>
```

Note that it preserves the `<a>` and its `href` attribute, but it strips the `<em>` tag and completely removes the `<del>` and its contents.

This provides greater flexibility than passing `markup=False` to various template elements such as `entry.title` or `entry.body`.


## Template API

As mentioned before, templates are rendered using
[Jinja2](http://jinja.pocoo.org), and get standard template parameters for both
Jinja2 and Flask. Additionally, there will be other things available to you,
depending on the template type.

Also, note that the templating system uses Python syntax for passing parameters
to functions. So, for example, `some_function(1,dingle=True,berry="none")`
passes a number, a boolean (true/false) named `dingle`, and a string named
`berry` with the value of `"none"`. When passing strings, quotes are required.
When passing anything else, the quotes should be left off; `False` and `"False"`
mean very different things in Python. (For starters, `"False"` is equivalent to
`True` in many contexts.)

### All templates

All template types get the default Flask objects; there is more information
about these on the [Flask templating
reference](http://flask.pocoo.org/docs/0.12/templating/).

The following additional things are provided to all templates:

* **`arrow`**: The [Arrow](https://arrow.readthedocs.io/en/latest/) time and date library

* **`get_view`**: Requests a [view](/api/view) of entries; see the [view documentation](/api/view#subviews) for the supported arguments.

* **`static`**: Build a link to a static resource. The first argument is the path within the static
    resources directory; it also takes the following optional named arguments:

    * **`absolute`**: Whether to force this link to be absolute
        * `False`: Use a relative link if possible (default)
        * `True`: Use an absolute link

* <span id="get-template">**`get_template`**</span>: A function that finds a template file for a given category or entry. The first argument is the
    name of the template to find or a list of template names; the second argument is what to find the template relative to (entry, category, or a file path).

    Example usage:

    ```jinja
    {% for entry in view(recurse=True).entries %}
        {% include get_template('_entry', entry) %}
    {% endfor %}
    ```

    This fragment will find all of the entries below the current category, and then
    render the closest matching `_entry` template for that category, with the filenames
    mapped as described [above](#template-mapping). This is useful
    for having content where its appearance within the template changes based on the
    category it's in; for example, if you want your Atom feed to show full content
    for only some parts of your site, or if you want image thumbnails to generate
    differently.

    ==Note:== The included template will only see the variables that are visible
    at that point in the template. If you need to set a variable that would normally
    be visible to the template, use the Jinja `{% set %}` command; for example, if
    the template fragment expects to get a variable named `subcat` and you want it
    to refer to the category, you'd do something like:

    ```jinja
    {% for cat in category.subcats(recurse=True) %}
        {% set subcat = cat %}
        {% include get_template('_my_fragment', cat) %}
    {% endfor %}
    ```

* **`template`**: Information about the current [template](/api/template)

* **`user`**: Information about the current user; this object has the following properties:

    * **`name`**: The login identity of the user
    * **`groups`**: A list of the groups they belong to
    * **`is_admin`**: `True` if the user is a member of the administrative group

* **`image`**: Load an image

    The resulting image works as a URL directly, or you can pass in arguments in
    the format `(output_scale, [arguments])`, which gets a URL rendered with the
    specified output scaling and [image rendition arguments](/image-renditions).
    The default is to use an `output_scale` of 1.

    It also has the following functions on it:

    * **`get_img_tag([arguments])`**: Makes an `<img>` tag with the provided
        [image rendition arguments](/image-renditions), with the following
        additions:

        * **`alt_text`**: Provides text for the `img`'s `alt` attribute
        * **`title`**: Provides text for the `img`'s `title` attribute

    * **`get_css_background([arguments])`**: Makes the appropriate `background-image`
        CSS attributes with the provided [image rendition arguments](/image-renditions),
        with the following additions:

        * **`uncomment`**: Whether the CSS declaration will be wrapped inside a comment;
            this is useful if your code editor would otherwise get confused by Jinja
            declarations inside of CSS.

    * **`get_image_attrs([arguments])`**: Generates the raw attributes that would
        be applied to the `<img>` tag produced by `get_img_tag`. This is probably
        not useful for templating, however.


    Example usage in HTML templates:

    ```jinja
    <div style="{{ image('/layout/bg.png').get_css_background(width=320) }}"> ... </div>

    {{ image('http://example.com/external-image.jpg').get_img_tag(link='http://example.com') }}
    ```

    and in a CSS template:

    ```jinja
    body {
        /* {{image("/background.jpg").get_css_background(width=320,height=320,uncomment=True)}} */
        background-color: white;
    }
    ```

    Like the [entry Markdown tags](/entry-format#image-renditions), you can use
    a `@` prefix to indicate that the image comes from the static files (rather
    than from the template's search path), and external URLs work as well.

    Unlike the entry Markdown tags, you have to specify width and height by
    name.

    If the image path is absolute (i.e. starts with a `/`), it will be treated
    as based on the site's content directory. If it is relative, it will look in
    the following locations, in the following order:

    1. Relative to the current entry's file (on entry templates)
    2. Relative to the current entry's category within the content directory
        (on entry templates)
    3. Relative to the current category within the content directory
    4. Relative to the template file, mapped to the content directory
        (for example, the template `templates/blog/feed.xml` will search in
        `content/blog`)

* **`login`**: Provide a login link

    This can be used directly, i.e. `{{login}}`, or it can be given a redirection path
    for where to redirect on successful login; for example, if you want to redirect back to the
    category rather than the current page, you can use:

    ```
    <a href="{{login(category.link)}}">Log in and return to {{category.name}}</a>
    ```

    You can also pass in additional parameters to the login handler; for example, it will take a
    named `me` parameter to provide an identity to start logging in as, although this isn't
    generally useful except for test purposes (such as providing quick `test:whatever` links).

* <span id="logout_link">**`logout`**: Provide a logout link</span>

    This can be used directly, i.e. `{{logout}}`, or it can be given a redirection path as with `login`.

    If this is used as a link target, the user will be given a logout confirmation dialog (this is to
    prevent certain issues with browsers prefetching pages). If you would like the user to not need to
    confirm the logout, use it in a `<form method="POST">`. For example:

    ```
    <a href="{{logout}}">Log out</a>
    ```

    will show a logout confirmation dialog (using the `logout.html` template), whereas

    ```
    <form method="POST" method="{{logout}}"><input type="submit" name="Log out"></form>
    ```

    will not.

A note to advanced Flask users: while `url_for()` is available, it shouldn't
ever be necessary, as all its useful functionality is exposed via the available
objects. If you need to use the endpoints from the Python side, please see the
[Python Flask endpoints](publ-python.md#endpoints).

### Entry pages

Specific entries are always rendered with its category's `entry` template.
The template gets the following additional objects:

* **`entry`**: Information about the [entry](/api/entry)
* **`category`**: Information about the [category](/api/category)

### Category pages

Categories are rendered with whatever template is specified, defaulting to
`index` if none was specified. The template gets the following additional
objects:

* **`category`**: Information about the [category](/api/category)
* **`view`**: The default [view](/api/view) for this category. It is equivalent
    to calling `get_view()` with the following arguments:

    * `category`: This category
    * `recurse`: `False`
    * `date`, `first`, `last`, `before`, `after`: set by the URL query parameters

    Note that unless any limiting parameters are set, this `view` object will
    not have any pagination on it. The intention is that `view` will be used as
    a basis for another more specific view; for example, this example will show
    10 entries at a time and get `previous` and `next` as appropriate:

    ```jinja
    {% set paged_view = view(count=10) %}
    {% for entry in paged_view.entries %}
        <!-- render entry -->
    {% endfor %}
    {% if paged_view.previous %}
        <a href="{{paged_view.previous.link}}">Previous page</a>
    {% endif %}
    {% if paged_view.next %}
        <a href="{{paged_view.next.link}}">Next page</a>
    {% endif %}
    ```

### Error pages

Error templates receive an `error` object to indicate which error occurred;
otherwise it only gets the default stuff. This object has the following
properties:

* **`code`**: The associated HTTP error code
* **`message`**: An explanation of what went wrong
* **`category`**: Information about the [category](/api/category)
* **`exception`**: In the case of an internal error, this will be an object
    with the following properties:

    * **`type`**: The human-readable type of exception (`IOError`, `ValueError`, etc.)
    * **`str`**: The human-readable exception string
    * **`args`**: Further information passed to the exception constructor

### Login page

The login template receives the following:

* **`login_url`**: A URL for the login form's `ACTION` parameter
* **`auth`**: The authentication handler object, which in turn has the following useful things:
    * **`handlers`**: A list of configured handlers

Each of the configured handlers has the following that is useful in a template:

* **`service_name`**: A human-readable name for the service
* **`description`**: A human-readable description of the service (may contain HTML)
* **`url_schemes`**: A list of example URL schemes; this is provided as a tuple of `(template,placeholder)`. For example, a Twitter handler might provide `("https://twitter.com/%","username")` as a scheme.

A simple `login.html` might look like this:

```jinja
<!DOCTYPE html>
<html>
<head>
<title>Login required</title>
</head>
<body>
<form method="GET" action="{{login_url}}" novalidate>
<input type="url" name="me" value="{{request.args['me']}}" placeholder="Your URL here" autofocus>
</form>

{% with messages = get_flashed_messages() %}
{% if messages %}
<ul class="flashes">
    {% for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
{% endwith %}

<p>Configured handlers:</p>
<ul>
    {% for handler in auth.handlers %}
    <li>{{handler.service_name}}: {{handler.description}}
        {% if handler.url_schemes %}
        <ul>
            {% for tmpl, val in handler.url_schemes %}
            <li><code>{{tmpl.replace('%', val)}}</code></li>
            {% endfor %}
        </ul>
        {% endif %}
    </li>
    {% endfor %}
</ul>
```

Note that the login template uses Flask message flashing to provide error feedback for a failed login.

### Unauthorized page

The unauthorized template receives the same data as the entry template. The `entry` object will be sanitized and only provide limited information, and the `category` object will be based on the URL used to access the entry, rather than the actual category of the entry.

You can access the default login stylesheet with `{{url_for('login',asset='css')}}`, if so desired.

### Logout page

The logout template does not receive any special variables, and should only provide a logout form with `<form method="POST">` which will confirm the logout on submission.

