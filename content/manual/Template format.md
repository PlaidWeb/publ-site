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
file named `feed`, `feed.html`, `feed.htm`, `feed.xml`, or `feed.json`, in the directories `templates/music/classical/baroque`, `templates/music/classical`, `templates/music`, and `templates`, in that order, returning the first one
that matches. (If no templates match, it shows an error page.)

> Note that because an exact filename can match, you can also use the template system to generate CSS or
> whatever other format you like! However, this usage isn't recommended.

#### Error templates

A note on error templates: Error pages *generally* get handled by whatever matches the `error` template; however, in the case of a specific
status code, it will also look for a template named based on that code. For example, a 404 error will try to
render the `404` template first, before falling back to `error`. (And of course this can be `404.html`, `404.xml`, `404.json`, and so on, although in most cases you'll probably be doing it as HTML.)

Also, if no error template is found (i.e. there's no top-level `error.html`), Publ will provide a built-in template
instead.

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
anything else, the quotes should be left off; `False` and `"False"` mean very different things in Python. (For starters, `"False"` is equivalent to `True` in many contexts. You'll get used to it.)

### All templates

All template types get the default Flask objects; there is more information about
these on the [Flask templating reference](http://flask.pocoo.org/docs/0.12/templating/).

The following additional things are provided to the request context:

* **`arrow`**: The [Arrow](https://arrow.readthedocs.io/en/latest/) time and date library

* <a name="fn-get-view"></a>**`get_view`**: Requests a view of entries; it takes the following arguments:

    * **`category`**: The top-level category to consider

        **Note:** If this is left unspecified, it will always include entries from the entire site.

    * **`recurse`**: Whether to include subcategories

        * `True`: Include subcategories
        * `False`: Do not include subcategories (default)

    * **`future`**: Whether to include entries from the future

        * `True`: Include future entries
        * `False`: Do not include future entries (default)

    * **`limit`**: Limit to a maximum number of entries. This is overridden by `date` (below).

    * **`entry_type`**: Limit to entries with a specific [`Entry-Type`](/entry-format#entry-type) header
    * **`entry_type_not`**: Limit to entries which do NOT match a specific entry type

        These can be a single string, or it can be an array of strings. Note that
        these are case-sensitive (i.e. `"PaGe"` and `"pAgE"` are two different types).

        * `get_view(entry_type='page')` - only get entries of type "page"
        * `get_view(entry_type_not='page')` - only get entries which AREN'T of type "page"
        * `get_view(entry_type=['news','comic'])` - get entries which are of type 'news' or 'comic'
        * `get_view(entry_type_not=['news','comic'])` - get entries of all types except 'news' or 'comic'

        Mixing `entry_type` and `entry_type_not` results in undefined behavior, not that it makes
        any sense anyway.

    * **`date`**: Limit to entries on a specified date; this can be of the format `YYYY`, `YYYY-MM`, or `YYYY-MM-DD`.

        If this is set, this overrides the `limit` parameter.

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

As a note: while `url_for()` is available, it shouldn't ever be necessary, as all
the other endpoints are accessible via higher-level wrappers (namely **`static`**, **`category`**, and **`entry`**).

### Entry pages

Specific entries are always rendered with its category's `entry` template.
The template gets the following additional objects:

* **`entry`**: Information about the [entry](#entry-object)
* **`category`**: Information about the [category](#category-object)

### Category pages

Categories are rendered with whatever template is specified, defaulting to `index`
if none was specified. The template gets the following additional objects:

* **`category`**: Information about the [category](#category-object)
* **`view`**: The default [view](#view object) for this category. It is equivalent to calling `get_view`
    with the following arguments:

    * `category`: This category
    * `recurse`: `False`
    * `date`, `first`, `last`, `before`, `after`: set by the URL query parameters

    <a name="pagination"></a>The intention is that `view` will be used as a basis
    for another more specific view; for example,
    the following will give you 10 entries at a time, with appropriate previous/next links:

    ```jinja
    {% set paged_view = view(limit=10) %}
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

## Object interface

### <a name="entry-object"></a>Entry object

The `entry` object has the following methods/properties:

* **`id`**: The numerical entry ID
* **`body`** and **`more`**: The text above and below the fold, respectively

    These properties can be used directly, or they can take parameters,
    for example for [image renditions](/image-renditions).

* **`date`**: The creation date and time of the entry

* All headers on the [entry file](/entry-format) are available

    These can be accessed either with `entry.header` or `entry.get('header')`. If
    there is a `-` character in the header name you have to use the second
    format, e.g. `entry.get('some-header')`.

    If there is more than one header of that name, this will only retrieve
    one of them (and which one isn't defined); if you want to get all of them
    use `entry.get_all('header')`. For example, this template fragment
    will print out all of the `Tag` headers in an unordered list, but only
    if there are any `Tag` headers:

    ```jinja
    {% if entry.Tag %}
    <ul>
        {% for tag in entry.get_all('Tag') %}
        <li>{{ tag }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    ```

* **`link`**: A link to the entry's individual page

    This can take arguments for different kinds of links; for example:

    * **`absolute`**: Whether to format this as an absolute or relative URL
        * **`False`**: Use a relative link (default)
        * **`True`**: Use an absolute link
    * **`expand`**: Whether to expand the URL to include the category and slug text
        * **`False`**: Use a condensed link
        * **`True`**: Expand the link to the full entry path (default)

    **Note:** If this entry is a redirection, this link refers to the redirect
    target.

* **`permalink`**: A permanent link to the entry

    This is similar to **`link`** but subtly different; it only accepts the
    **`absolute`** and **`expand`** arguments, and it never follows a redirection.

    Whether to use an expanded link or not depends on how "permanent" you want your
    permalink to be; a condensed link will always cause a redirect to the current
    canonical URL, but an expanded link may go obsolete and still cause a redirection.
    The expanded link is generally better for SEO, however, and thus it is the default
    even if it isn't truly "permanent." (But then again, what *is* permanent, anyway?)

    Unlike **`link`** this will never follow a redirection.

* **`last_modified`**: A last-modified time for this entry (useful for feeds)

* **`next`**: The next entry (ordered by date)

    This can also take the same arguments as [`get_view()`](#fn-get-view), with the following differences:

    * `limit` has no effect
    * If `category` is unspecified, it defaults to the entry's category
    * If `category` is specified, `recurse` defaults to `True`

    Examples:

    ```jinja
    <!-- link to the next entry in the category -->
    {% if entry.next %}
    <a href="{{ entry.next.link }}">{{ entry.next.title }}</a>
    {% endif %}

    <!-- link to the next entry in the entire 'comics' section where the type isn't 'news' or 'recap' -->
    {% set next_comic = entry.next(category='comics',entry_type_not=['news','recap']) %}
    {% if next_comic %}
    <a href="{{ next_comic.link }}">{{ next_comic.title }}</a>
    {% endif %}
    ```


* **`previous`**: The previous entry (ordered by date)

    This takes the same arguments as `next`.

### <a name="category-object"></a>Category object

The `category` object provides the following:

* **`path`**: The full path to the category

* **`basename`**: Just the last part of the category name

* **`subcats`**: The subcategories of this category. Takes the following argument:

    * **`recurse`**: Whether to include the subcategories of the subcategories, and their subcategories
        and so on. Possible values:

        * **`False`**: Only include direct subcategories (default)
        * **`True`**: Include all subcategories

* **`parent`**: The parent category, if any

* **`link`**: The link to the category; optionally takes the
    following arguments:

    * **`template`**: Which template to use when rendering the category
    * **`absolute`**: Whether to format this as an absolute or relative URL
        * **`False`**: Use a relative link (default)
        * **`True`**: Use an absolute link

Example template code for printing out an entire directory structure (flattened):

```jinja
<ul>
{% for subcat in category.subcats(recurse=True) %}
<li>subcat.path</li>
{% endfor %}
</ul>
```

Example template code for printing out the directory structure in a nice recursive manner:

```jinja
<ul>
{% for subcat in category.subcats recursive %}
    <li>{{ subcat.basename }}
    {% if subcat.subcats %}
    <ul>{{ loop(subcat.subcats)}}</ul>
    {% endif %}</li>
{% endfor %}
</ul>
```

### <a name="view-object"></a>View object

The `view` object has the following things on it:

* **`entries`**: A list of all of the entries that are visible in this view

* **`last_modified`**: A last-modified time for this view (useful for feeds)

* **`spec`**: The view's specification (category, limits, date, etc.)

    This is in the form of the arguments that would be passed to `get_view` to
    obtain this view.

* **`previous`**: The previous page's view

* **`next`**: The next page's view

* **`link`**: The link to this view; optionally takes the following arguments:

    * **`template`**: Which template to use (defaults to the index template)
    * **`absolute`**: Whether the URL should be absolute or relative
        * **`False`**: Use a relative URL (default)
        * **`True`**: Use an absolute URL

* **`first`**: The first entry in the view
* **`last`**: The last entry in the view
* **`newest`**: The newest entry in the view
* **`oldest`**: The oldest entry in the view

It also takes arguments to further refine the view, using the same arguments
as [`get_view()`](#fn-get-view); for example:

```jinja
{% for entry in view(limit=10) %}
    {{entry.title}}
{% endfor %}
```

Note that if you specify a category this will override the current view's category.

See the [explanation on category pagination](#pagination) to see how to use `next` and `previous`.
