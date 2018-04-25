Title: Entry objects
Path-Alias: /api/entry
Date: 2018-04-25 14:50:21-07:00
Entry-ID: 115
UUID: ceece984-9cde-4323-9bd9-14e9a68044cd

The template API for `entry` objects.

.....

The `entry` object has the following methods/properties:

* **`id`**: The numerical entry ID
* **`body`** and **`more`**: The text above and below the fold, respectively

    These properties can be used directly, or they can take parameters,
    for example for [image renditions](/image-renditions).

* **`date`**: The creation date and time of the entry

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

* **`last_modified`**: A last-modified time for this entry

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

    Note that if there's more than one of a header, it's undefined which one you retrieve.
    If you want to get more than one, use `get_all` instead.

* **`get_all`**: Get all of a header type from an entry, as a list.

    For example, this template fragment
    will print out all of the `Tag` headers in an unordered list, but only
    if there are any `Tag` headers:

    ```jinja
    {% if entry.get('Tag') %}
    <ul>
        {% for tag in entry.get_all('Tag') %}
        <li>{{ tag }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    ```
