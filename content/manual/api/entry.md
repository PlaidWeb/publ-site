Title: Entry objects
Path-Alias: /api/entry
Date: 2018-04-25 14:50:21-07:00
Entry-ID: 115
UUID: ceece984-9cde-4323-9bd9-14e9a68044cd

The template API for `entry` objects.

.....

The `entry` object has the following methods/properties:

* **`id`**: The numerical entry ID
* **`title`**: The title of the entry

    This property can be used directly, or it can take [HTML processing arguments](/html-processing), as well as the following:

    * **`always_show`**: Whether to always show the title, even if the entry isn't authorized; use with caution. (default: `False`)

    ==Note:== v0.5.12 has a bug where the `no_smartquotes` HTML argument doesn't work. This will be [fixed in v0.5.13](https://github.com/PlaidWeb/Publ/commit/004fb47a3c53830081579e6ae5c1133f1ca2581e).

* **`entry_type`**: The value of the entry's `Entry-Type` header, if any.

* **`private`**: Indicates whether this entry is only visible to logged-in users.
* <span id="authorized">**`authorized`**: Indicates whether this entry is visible to the current user.</span>

* **`body`**, **`more`**, and <span id="footnotes">**`footnotes`**</span>: The different content sections of an entry.

    `body` is the section above the fold.

    `more` is the section below the fold.

    `footnotes` are the footnotes for the entire entry.

    These properties can be used directly, or they can take any of the following
    parameters:

    * The standard [HTML processing arguments](/html-processing)
    * **`footnotes_link`**: Specifies the base URL for footnote links; defaults to the entry's link.

        From `body` and `more` this refers to the URL the footnotes will display on.

        From `footnotes` this refers to a URL where the entry text will be visible.

        You can make these different if you want to do something fancy like keeping your footnotes on a separate page (using an archive template or the like); for example,
        `{{entry.more(footnotes_link=entry.link(template='footnotes'))}}`

    * **`footnotes_class`**: Specifies the CSS class for the `<sup>` that contains the footnote reference link. Defaults to none.

        If you would like to style the `<a>` element, you can use CSS selectors `[rel="footnote"]` and `[rev="footnote"]` for the reference and return links, respectively.

    * **`footnotes_return`**: Specifies the text to put inside the return link; defaults to `'↩'`.

* **`card`**: `<meta>` tags for an OpenGraph card

    Like `body` and `more`, this takes arguments that affect the image renditions;
    you will almost certainly want to set `width`, `height`, and `count`.

    This will generate an appropriate `og:title`, `og:url`, `og:image`, and `og:description`
    tags based on the entry's permalink and text. `og:description` contains the [entry summary](322#summary), and there will be `og:image` tags for up to the first `count` images.

    If you use this, you should also provide your own `og:type` tag, e.g.

    ```html
    {{ entry.card(width=640,height=350,resize="fill",count=4) }}
    <meta property="og:type" content="website" />
    ```

    Please see the [OpenGraph documentation](http://ogp.me/) for more information.

    This also accepts the `markdown_extensions` argument.

* <span id="summary">**`summary`**</span>: The [entry summary](322#summary). This is always treated as plain text (i.e. no HTML or Markdown).

* **`category`**: The category that this entry belongs to; this is provided as a
    [category object](/api/category).

* **`date`**: The publication date and time of the entry, as an [Arrow](https://arrow.readthedocs.io/en/latest/#arrow.arrow.Arrow) object.

    This is taken from the entry's [`Date` header](322#date).

    Since it's an Arrow object you can use it directly to get an incredibly
    precise time, but you'll probably want to call a method on it such as
    [`format()`](http://arrow.readthedocs.io/en/latest/#format) or
    [`humanize()`](http://arrow.readthedocs.io/en/latest/#humanize).

* <span id="date_grouper">**`date_year`**, **`date_month`**, **`date_day`**: Three pre-defined formats of `date` for the purpose of making it easier to use Jinja's [`groupby`](http://jinja.pocoo.org/docs/2.10/templates/#groupby) functionality.</span>

    For example, this snippet will collate the visible entries by month:

    ```jinja
    <ul>{% for month,entries in view.entries|groupby('date_month') %}
        <li>{{month}}
            <ul>{% for entry in entries %}
            <li>{{entry.date.format()}}: <a href="{{entry.link}}">{{entry.title}}</a></li>
            {% endfor %}</ul>
        </li>
    {% endfor %}</ul>
    ```

* **`permalink`**: A permanent link to the entry

    Takes the following arguments:

    * **`absolute`**: Whether to format this as an absolute or relative URL
        * **`False`**: Use a relative link (default)
        * **`True`**: Use an absolute link
    * **`expand`**: Whether to expand the URL to include the category and slug text
        * **`False`**: Use a condensed link
        * **`True`**: Expand the link to the full entry path (default)

    Whether to use an expanded link or not depends on how "permanent" you want your
    permalink to be; a condensed link will always cause a redirect to the current
    canonical URL, but an expanded link may go obsolete and still cause a redirection.
    The expanded link is generally better for SEO, however, and thus it is the default
    even if it isn't truly "permanent." (But then again, what *is* permanent, anyway?)

* **`link`**: A destination link to the entry

    This is the same as **`permalink`** except it will also follow an entry's
    `Redirect-To` destination.

* **`tags`**: A list of tags associated with this entry.

* **`archive`**: Get an archive link for rendering this in a category view.

    This takes the following arguments:

    * <span id="archive.paging">**`paging`**: The pagination type; one of:</span>
        * **`"day"`**: Entries for that day
        * **`"month"`**: Entries for that month
        * **`"year"`**: Entries for that year
        * **`"week"`**: Entries for that week
        * **`"offset"`**: Goes to the page starting with this entry (default)
    * **`template`**: Which template to use for the link (defaults to `''`, i.e. the default/index category template)
    * **`category`**: Which category to link to; defaults to the entry's own category
    * **`absolute`**: Whether to use an absolute link (defaults to `False`)
    * **`tag`**: Limit the view to the specified tag(s)

* **`last_modified`**: A last-modified time for this entry.

    This is taken from the entry's [`Last-Modified` header](322#last-modified).

* **`next`**: The next entry (ordered by date)

    This can also take the same arguments as [`get_view()`](/api#fn-get-view), with the following differences:

    * `count` has no effect
    * If `category` is unspecified, it defaults to the entry's category
    * If `category` is specified, `recurse` defaults to `True`

    Examples:

    ```jinja
    <!-- link to the next entry in its category -->
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

* **`get`**: Get a header from the [entry file](/entry-format)

    Note that if there's more than one of a header, it's undefined which one this will retrieve.
    If you want to get more than one, use `get_all` instead.

    Header names are not case-sensitive (i.e. `'fooBar'`, `'Foobar'`, and `'FOOBAR'` are all equivalent).

    Also, if the header name is a valid variable name (i.e. consists of only letters, numbers, and underscores, and starts with a letter or underscore), and doesn't conflict with an API function, you can also retrieve it directly, e.g. `entry.Foobar` is equivalent to `entry.get('Foobar')`. It is recommended that if you do this, always start the name with a capital letter, to avoid conflicts with any future API functions (e.g. `entry.Next` will always be equivalent to `entry.get('Next')`).

* **`get_all`**: Get all of a header type from an entry, as a list.

    For example, this template fragment
    will print out all of the `Tag` headers in an unordered list, but only
    if there are any `Tag` headers:

    ```jinja
    {% if entry.get('Tag') %}
    <ul class="tags">
        {% for tag in entry.get_all('Tag') %}
        <li>{{ tag }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    ```

    Header names are not case-sensitive (i.e. `'fooBar'`, `'Foobar'`, and `'FOOBAR'` are all equivalent).

* The following properties are also available but probably aren't of use to template authors, and are only listed for the sake of completion. You should not rely on them for anything as they might change without warning.

    * `file_path`: The file path of the entry's content file

    * `status`: The publish status of the entry

        Note that as of Publ 0.3.14 this is a numerical value; in future versions this may change to a string or internal data representation. You should not actually rely on this for anything public.

    * `slug_text`: The URL slug text for the entry

    * `redirect_url`: The value of the `Redirect-To` header, if any

    * `sort_title`: The value of the `Sort-Title` header, if any

    * `entry_template`: The value of the `Entry-Template` header, if any

    * `display_date`, `utc_date`, `local_date`: Various forms of the entry's `date` used for internal purposes

    * `aliases`: The various registered path aliases for this entry. A list of items, each providing the following properties:
        * `path`: The incoming path
        * `url`
        * `entry`
        * `category`
        * `template`
