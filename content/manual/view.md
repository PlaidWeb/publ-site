Title: View object
Path-Alias: /api/view
Date: 2018-04-25 15:03:55-07:00
Entry-ID: 150
UUID: d506b63c-dd77-4c7a-b06e-c381696c3cc2

The template API for view objects.

.....

The `view` object has the following things on it:

* **`entries`**: A list of all of the entries that are visible in this view

* **`last_modified`**: A last-modified time for this view (useful for feeds)

* **`spec`**: The view's specification (category, count, date, etc.)

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
as [`get_view()`](/api#fn-get-view); for example, this will print the titles of
the first 10 entries in the view, including subcategories:

```jinja
{% for entry in view(count=10,recurse=True) %}
    {{entry.title}}
{% endfor %}
```

Note that if you specify a category this will override the current view's category.

See the [explanation on category pagination](/api#pagination) to see how to use `next` and `previous`.
