Title: Category object
Path-Alias: /api/category
Date: 2018-04-25 15:02:41-07:00
Entry-ID: 170
UUID: 81cbd7d2-55c5-48d5-b27c-29b8b6d8a3b0

Template API for categories.

.....

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

* **`first`**: Returns the first entry in this category; optionally takes [view arguments](/api#get-view)
* **`last`**: Returns the last entry in this category; optionally takes [view arguments](/api#get-view)

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
