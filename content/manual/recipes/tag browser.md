Title: Tag browser
Tag: tags
Tag: browsing
Date: 2026-03-13 11:44:02-07:00
UUID: 3ba836df-d547-42df-a2f2-b918cfc8b60f
Entry-ID: 577

Allow users to narrow in on content based on multiple tags at a time.

.....

Here is an implementation of a basic tag browser that allows users to filter content based on multiple criteria.

Note that you'll also want to implement the [crawler mitigations](210).

First, you'll need to modify your content view with `tag_filter='ALL'`; for example, at the top of your template, have a line like:

```html+jinja
!index.html
{%- set view = view(tag_filter='ALL') -%}
```

Next, this block will give you a tag filter that shows the top 10 tags present in the current view in addition to any tags that are currently selected, with a toggle to show all tags that have more than one entry:

```html+jinja
{%- if not user.is_bot and category.tags(recurse=view.spec.recurse) -%}
<div id="tags"><h3>Topic Tags</h3>

    {% macro tag_link(view) -%}
    {{view.link(template=template,all_tags=1 if request.args.all_tags else None)}}
    {%- endmacro %}

    <ul>
        {%- if view.tags -%}
        <li class="clear"><a href="{{tag_link(view(tag=None))}}">Clear filter</a></li>
        {% endif %}

        {% set tags = category.tags(tag=view.spec.tag if view.spec.tag else None,
            tag_filter='ALL',recurse=view.spec.recurse)
            | sort(attribute='count',reverse=True) %}
        {% for name,count in (tags if request.args.all_tags else tags[:10+view.tags|length]) %}
            {%- if count > 1 and
                (request.args.all_tags or loop.index < 10 or name in view.tags) -%}
                <li class="{{name in view.tags and 'selected' or ''}}"><a rel="nofollow" href="{{tag_link(view.tag_toggle(name))}}">{{name}}</a> ({{count}})</li>
            {%- endif -%}
        {% endfor %}

    {% if request.args.all_tags %}
        <li class="top-only"><a rel="nofollow" href="{{view.link(template=template)}}">Top tags only</a></li>
    {% elif tags|length > 10 %}
        <li class="all"><a rel="nofollow" href="{{view.link(template=template,all_tags=1)}}">Show all tags</a></li>
    {% endif %}
    </ul>
</div>
{% endif %}
```

This stylesheet snippet will add useful styling to the tag list, as well:

```css
#tags ul {
    list-style-type: none;
}
#tags li {
    text-indent: 1em hanging;
}
#tags li:before {
    content: '☐\00a0';
}

#tags li.clear:before {
    content: '☒\00a0';
    font-weight: bold;
}

#tags li.selected:before {
    content: '☑︎\00a0';
}

#tags li.all, #tags li.top-only {
    font-style: italic;
}
#tags li.all:before, #tags li.top-only:before {
    content: '';
}
```
