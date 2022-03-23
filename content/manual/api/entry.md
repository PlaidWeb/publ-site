Title: Entry objects
Path-Alias: /api/entry
Date: 2018-04-25 14:50:21-07:00
Entry-ID: 115
UUID: ceece984-9cde-4323-9bd9-14e9a68044cd

The template API for `entry` objects.

.....

## Default properties

The `entry` object has the following methods/properties:

* **`id`**: The numerical entry ID
* **`title`**: The title of the entry

    This property can be used directly, or it can take [HTML processing arguments](/html-processing), as well as the following:

    * **`always_show`**: Whether to always show the title, even if the entry isn't authorized; use with caution. (default: `False`)

* <span id="summary">**`summary`**</span>: The entry's [summary text](322#summary)

    This property can be used directly, or it can take [HTML processing arguments](/html-processing), as well as the following:

    * **`always_show`**: Whether to always show the summary text, even if the entry isn't authorized; use with caution. (default: `False`)

* **`entry_type`**: The value of the entry's `Entry-Type` header, if any.

* **`private`**: Indicates whether this entry is only visible to logged-in users.
* <span id="authorized">**`authorized`**: Indicates whether this entry is visible to the current user.</span>

* <span id="body">**`body`**</span>, <span id="more">**`more`**</span>, and <span id="footnotes">**`footnotes`**</span>: The different content sections of an entry.

    `body` is the section above the fold.

    `more` is the section below the fold.

    `footnotes` are the footnotes for the entire entry.

    These properties can be used directly, or they can take any of the following
    parameters:

    * The standard [HTML processing arguments](/html-processing)
    * **`footnotes_link`**: Specifies the base URL for footnote links; defaults to the entry's URL.

        From `body` and `more` this refers to the URL the footnotes will display on.

        From `footnotes` this refers to a URL where the entry text will be visible.

        You can make these different if you want to do something fancy like keeping your footnotes on a separate page (using an archive template or the like); for example,
        `{{entry.more(footnotes_link=entry.link(template='footnotes'))}}`

    * **`footnotes_class`**: Specifies the CSS class for the `<sup>` that contains the footnote reference link. Defaults to none.

        If you would like to style the `<a>` element, you can use CSS selectors `[rel="footnote"]` and `[rev="footnote"]` for the reference and return links, respectively.

    * **`footnotes_return`**: Specifies the text to put inside the return link; defaults to `'↩'`.

    * **`toc_link`**: The base URL for the heading's anchor link (for use from table of contents or generic permalinks); defaults to the entry's URL.

    * **`heading_link_class`**: The HTML `class` attribute to add to the self-link from within headings; defaults to none.

        This is useful for e.g. displaying a fancy permalink marker; for example, you can render the entry with:

        ```html
        {{ entry.more(heading_link_class='toc')}}
        ```

        and use a stylesheet rule like e.g.

        ```css
        .toc:before {
            position: absolute;
            margin-left: -1ex;
            content: '#';
            color: #777;
        }
        ```

    * **`heading_link_config`**: Additional attributes to add to the self-link from within headings (for e.g. `title` or `data-*` or the like); defaults to nothing.

    * **`heading_template`**: A template string for how to format headings; takes the following format fragments:
        * **`link`**: The open link tag (e.g. `<a href="entry#anchor" class="linkClass">`)
        * **`text`**: The formatted text of the heading itself

        This defaults to `{link}</a>{text}` (the `<a>` is contained within `{link}`).

        Note that this template will always be rendered inside the heading tags (e.g. `<h2 id="foo"><a class="toc" href="entry#foo"></a>Foo</h2>`).

        If you would not like any self-link to be produced for some reason, set `heading_template` to `{text}`.

    * **`code_highlight`**: Whether to apply syntax highlighting to code blocks with a declared language (default: `True`)
    * **`code_number_links`**: Whether to generate line-numbering links within code blocks; see the [fenced code extensions](322#fenced-code) for more information. (default: `True`)

        Set this to a string value to override the base URL for the line number links.

* <span id="toc">**`toc`**</span>: The table of contents for an entry.

    Renders a table of contents based on the headings of the entry; only applies to Markdown entries.

    In addition to the standard [HTML processing arguments](/html-processing), it takes the following arguments:

    * **`toc_link`**: The base URL for links to the entry; defaults to the entry's link.

    * **`max_depth`**: How many levels deep to render



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

* <span id="get">**`get`**</span>: Get a header from the [entry file](/entry-format)

    This takes the following arguments:

    * **`name`**: The name of the header to retrieve
    * **`always_allow`**: Whether to always retrieve it, even if the entry is unauthorized (default: `False`)

    Note that if there's more than one of a header, it's undefined which one this will retrieve.
    If you want to get more than one, use `get_all` instead.

    Header names are not case-sensitive (i.e. `'fooBar'`, `'Foobar'`, and `'FOOBAR'` are all equivalent).

    Note that this will get the *raw* header values, rather than anything interpreted by Publ. So, for example, `entry.get('date')` will return the `Date:` header string, rather than the display date of the entry.

    See the section on [header retrieval](#header-retrieval) for more information.

* <span id="get_all">**`get_all`**</span>: Get all of a header type from an entry, as a list.

    This takes the following arguments:

    * **`name`**: The name of the header to retrieve
    * **`always_allow`**: Whether to always retrieve it, even if the entry is unauthorized (default: `False`)

    For example, this template fragment
    will print out all of the `Author` headers in an unordered list, but only
    if there are any `Author` headers:

    ```jinja
    {% if entry.Author %}{# equivalent to entry.get('Author') #}
    <ul class="authors">
        {% for author in entry.get_all('Author') %}
        <li>{{ author }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    ```

    Header names are not case-sensitive (i.e. `'fooBar'`, `'Foobar'`, and `'FOOBAR'` are all equivalent).

    Note that this will get the *raw* header values, rather than anything interpreted by Publ. So, for example, `entry.get_all('category')` will retrieve the raw text of the `Category:` header, rather than the entry's [`category` object](170).

* <span id="attachments">**`attachments`**</span>: Other entries which are attached to this one, using the `Attach:` header.

    This takes the standard [view arguments](150#subviews). Note that the default ordering is undefined, and if order matters you should specify it. For example:

    ```jinja
    {% for attachment in entry.attachments(order='oldest') %}
    ```

    will order by date, and

    ```jinja
    {% for attachment in entry.attachments(order='title') %}
    ```

    will order them by title (honoring the `Sort-Title` attribute). You can also sort by arbitrary metadata headers; for example:

    ```jinja
    {% for attachment in entry.attachments|sort(attribute='My-Custom-Header')} %}
    ```

* **`attached`**: Like `attachments`, but it shows the entries that this entry is attached to.

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

## <span id="header-retrieval">Header retrieval</span>

If you have defined [custom headers](322#headers), you can do several different things with them:

* You can always use `entry.get('header-name')`, or `entry['header-name']` which is equivalent. If there are multiple headers of the same name, it is undefined which one this will get.

* `entry.get_all('header-name')` will get all of the raw values of a header, as an array. For example, with an entry like:

    ```publ
    Title: My weird day
    Noun: first noun
    Noun: second noun
    Noun: third noun
    ```

    then `entry.get_all('noun')` will return an array like `['first noun', 'second noun', 'third noun']` (although the order isn't guaranteed).

* If the header name is a valid variable name (i.e. starts with a letter or
    underscore, and only contains letters, numbers, and underscores), and
    doesn't conflict with one of the [built-in properties](#builtins), you can
    also get it using the `.` operator; for example, in an entry like:

    ```publ
    Title: This is a test
    Verb: embiggen
    ```

    `entry.verb` will be `'embiggen'`.

    However, there's always the possibility that a future Publ update might end
    up using your custom header name as a built-in property, so you can't be
    100% sure that this will continue to work forever.

* The `in` keyword will let you know if a header exists on an entry; for
    example, this template fragment:

    ```jinja2

    <h1>{{entry.title}}</h1>
    {{entry.body}}

    {% if 'cut' in entry %}
    <details class="cut"><summary>{{entry.cut}}</summary>
    {{entry.more}}
    </details>
    {% endif %}
    ```

    lets you make an entry like this:

    ```publ
    Title: An entry with a cut
    Cut: Extreme nerdery

    Want to hear a secret?

    .....

    I'm a gigantic nerd.
    ```

    which will render like:

    ```
    <h1>An entry with a cut</h1>

    <p>Want to hear a secret?</p>

    <details class="cut"><summary>Extreme nerdery</summary>
    <p>I'm a gigantic nerd.</p>
    </details>
    ```

    Note that this is *generally* the same as simply doing e.g.

    ```jinja2
    {% if entry.cut %}
    ```

    but it's slightly more efficient and also can simplify some template logic,
    probably.

* If the header name is a valid variable name (i.e. consists of only letters, numbers, and underscores, and starts with a letter or underscore), and doesn't conflict with an API function, you can also retrieve it directly, e.g. `entry.Foobar` is equivalent to `entry.get('Foobar')`. It is recommended that if you do this, always start the name with a capital letter, to avoid conflicts with any future API functions (e.g. `entry.Next` will always be equivalent to `entry.get('Next')`).

    You can also check to see if the entry has a header

