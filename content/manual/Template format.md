Title: Template API
Path-Alias: /template-format
Path-Alias: /template-api
Path-Alias: /api
Date: 2018-04-02 18:03:58-07:00
Entry-ID: 324
UUID: cbb977df-7902-4621-af9b-36ab44401748

A guide to building templates for Publ

.....

Publ templates use the [Jinja2](http://jinja.pocoo.org) templating system; please
see its references for the general syntax of template files.

There are three kinds of page in Publ: entry, category, and error.

## How templates work

### Short version

When someone requests a page, Publ finds the most-specific template
that matches, and uses that to render the page.

### Long version

When someone requests a page, Publ looks up whether it's a category view or an entry.
Category views look something like `http://mysite.com/art/photos/seattle/` or `http://mysite.com/blog/minimal`.
Entry views look something like `http://mysite.com/art/photos/1529-unwelcome-visitor`.

Every view has a category associated with it; for example, `http://mysite.com/art/photos/1529-unwelcome-visitor`
is in the `art/photos` category (i.e. all the stuff between the website address and the entry ID, not including
the `/`s at either end), and `http://mysite.com/blog/minimal` is in the `blog` category; the category is basically everything between the server name and the last `/` (in this case, `minimal` is the view).

When you see an entry, there is only one possible template that it chooses, `entry`. When you see a category,
if there's a view indicated, it uses that view name; otherwise it uses the `index` view.

(The category can be blank, incidentally; `http://mysite.com/` shows you the `index` view on the empty category.)

Anyway, given the category and view name, Publ looks for the closest matching template, by starting out in the
template directory that matches the category name, and then going up one level until it finds a matching
template. And a template will match based on either the exact name, or the name with `.html`, `.htm`, `.xml`, or `.json` added to the end.

So for example, if you ask for `http://mysite.com/music/classical/baroque/feed`, it will look for a template
file named `feed`, `feed.html`, `feed.htm`, `feed.xml`, or `feed.json`,
in the directories `templates/music/classical/baroque`, `templates/music/classical`, `templates/music`, and `templates`, in that order, returning the first one
that matches. (If no templates match, it shows an error page.)

#### Error templates

A note on error templates: Error pages *generally* get handled by whatever matches the `error` template; however, in the case of a specific
status code, it will also look for a template named based on that code. For example, a 404 error will try to
render the `404` template first, before falling back to `error`. (And of course this can be `404.html`, `404.xml`, `404.json`, and so on, although in most cases you'll probably be doing it as HTML.)

Also, if no error template is found (i.e. there's no top-level `error.html`), Publ will provide a built-in template
instead.

#### Generating CSS files

You can also use the template system to generate CSS, which is useful for having your
CSS files reference other assets via `static()` or `image()`. This also makes it
quite simple to create CSS templates that inherit from and override other CSS templates;
for example, if you have the file `templates/style.css`, you can have `templates/blog/style.css`
that looks like:

```css
@import url('../style.css');

body { background: red; }
```

and then your HTML templates need only refer to the stylesheet using, for example:

```html
<link rel="stylesheet" href="style.css" />
```

## Required templates

*Technically* no template is actually required, but in order to have a functioning site,
you should have, at the very least, the following top-level templates:

* `index.html`: the default category view
* `entry.html`: the entry view
* `error.html`: Some sort of error page (but this is entirely optional)

## Template API

As mentioned before, templates are rendered using [Jinja2](http://jinja.pocoo.org), and get standard template parameters for both Jinja2 and Flask. Additionally, there will be other things available to you, depending on
the template type.

Also, note that the templating system uses Python syntax for passing parameters to functions.
So, for example, `some_function(1,dingle=True,berry="none")` passes a number, a boolean (true/false) named `dingle`,
and a string named `berry` with the value of `"none"`. When passing strings, quotes are required. When passing
anything else, the quotes should be left off; `False` and `"False"` mean very different things in Python. (For starters,
`"False"` is equivalent to `True` in many contexts.)

### All templates

All template types get the default Flask objects; there is more information about
these on the [Flask templating reference](http://flask.pocoo.org/docs/0.12/templating/).

The following additional things are provided to all templates:

* **`arrow`**: The [Arrow](https://arrow.readthedocs.io/en/latest/) time and date library

* <a name="get-view"></a>**`get_view`**: Requests a [view](/api/view) of entries; it takes the following arguments:

    * **`category`**: The top-level category to consider

        **Note:** If this is left unspecified, it will always include entries from the entire site.

    * **`recurse`**: Whether to include subcategories

        * `True`: Include subcategories
        * `False`: Do not include subcategories (default)

    * **`future`**: Whether to include entries from the future

        * `True`: Include future entries
        * `False`: Do not include future entries (default)

    * **`date`**: Limit to entries based on a specified date; this can be of the format `YYYY`, `YYYY-MM`, or `YYYY-MM-DD`.
    * **`count`**: Limit to a maximum number of entries.

        If `date` is set, `count` has no effect.

    * **`entry_type`**: Limit to entries with a specific [`Entry-Type`](/entry-format#entry-type) header
    * **`entry_type_not`**: Limit to entries which do NOT match a specific entry type

        These can be a single string, or it can be an array of strings. Note that
        these are case-sensitive (i.e. `"PaGe"` and `"pAgE"` are two different types).

        * `get_view(entry_type='page')` - only get entries of type "page"
        * `get_view(entry_type_not='page')` - only get entries which AREN'T of type "page"
        * `get_view(entry_type=['news','comic'])` - get entries which are of type 'news' or 'comic'
        * `get_view(entry_type_not=['news','comic'])` - get entries of all types except 'news' or 'comic'

        Mixing `entry_type` and `entry_type_not` results in undefined behavior, not that it makes
        any sense to do that anyway.

    * **`last`**: Limit the view such to none newer than the specified entry (by id or object)
    * **`first`**: Limit the view such to none older than the specified entry
    * **`before`**: Limit the view to only entries which came before the specified entry
    * **`after`**: Limit the view to only entries which came after the specified entry

    * **`order`**: What order to provide the entries in; one of:
        * **`oldest`**: Oldest-first
        * **`newest`**: Newest-first (default)
        * **`title`**: Sorted alphabetically by title

* **`static`**: Build a link to a static resource. The first argument is the path within the static
    resources directory; it also takes the following optional named arguments:

    * **`absolute`**: Whether to force this link to be absolute
        * `False`: Use a relative link if possible (default)
        * `True`: Use an absolute link

* **`template`**: Information about the current [template](/api/template)

* **`image`**: A function to generate an image rendition.

    In addition to the [standard image rendition arguments](/image-renditions), it also
    takes the following arguments:

    * **`filename`**: The name of the image to render; this can also be passed as the
        first positional parameter
    * **`output_scale`**: The scaling factor for the image rendition (defaults to 1)


    Example usage (in a CSS template):

    ```css
    body {
        background-image: url('{{image("/background.jpg")}}');
    }
    ```

    If the image path is absolute (i.e. starts with a `/`), it will be treated as based on the
    site's content directory. If it is relative, it will look in the following locations, in the
    following order:

    1. Relative to the current entry's file (on entry templates)
    2. Relative to the current entry's category within the content directory (on entry templates)
    3. Relative to the current category within the content directory
    4. Relative to the template file, mapped to the content directory (for example, the template
        `templates/blog/feed.xml` will search in `content/blog`)

As a note: while `url_for()` is available, it shouldn't ever be necessary, as all
the other endpoints are accessible via higher-level wrappers (namely **`static`**, **`category`**, and **`entry`**).

### Entry pages

Specific entries are always rendered with its category's `entry` template.
The template gets the following additional objects:

* **`entry`**: Information about the [entry](/api/entry)
* **`category`**: Information about the [category](/api/category)

### Category pages

Categories are rendered with whatever template is specified, defaulting to `index`
if none was specified. The template gets the following additional objects:

* **`category`**: Information about the [category](/api/category)
* **`view`**: The default [view](/api/view) for this category. It is equivalent to calling [`get_view`](#get-view)
    with the following arguments:

    * `category`: This category
    * `recurse`: `False`
    * `date`, `first`, `last`, `before`, `after`: set by the URL query parameters

    Note that unless any limiting parameters are set, this `view` object will not have any
    pagination on it. The intention is that `view` will be used as a basis
    for another more specific view; for example, this example will show 10 entries at a time and
    get `previous` and `next` as appropriate:

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
* **`exception`**: In the case of an internal error, this will be an object with the following properties:
    * **`type`**: The human-readable type of exception (`IOError`, `ValueError`, etc.)
    * **`str`**: The human-readable exception string
    * **`args`**: Further information passed to the exception constructor

