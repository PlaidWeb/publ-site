Title: Calendar display
Date: 2026-02-26 10:58:13-08:00
UUID: 981db6de-d22f-432c-8775-7deb98ca334b
Entry-ID: 1101

How to render a calendar widget

.....

Here is a template snippet for rendering out a calendar for a particular view.

```jinja
{%- macro render_calendar(view, week_start=7) -%}

{%- if not view.is_current and view.newest -%}
{%- set month = view.newest.date.floor('month') -%}
{%- else -%}
{%- set month = arrow.now().floor('month') -%}
{%- endif -%}

{%- set content = view(date=month.format('YYYY-MM')) -%}
{%- set firstday,_ = month.span('week',week_start=week_start) -%}
{%- set _,lastday = month.ceil('month').span('week',week_start=week_start) -%}

<table class="calendar">
    <thead>
        <tr>{%- for day in arrow.Arrow.range('day',firstday,firstday.shift(days=6)) -%}
            <th>{{day.format('ddd')}}</th>
        {%- endfor -%}</tr>
    </thead>
    <tbody>

        {%- for week in arrow.Arrow.range('week',firstday,lastday) -%}
        <tr>
            {%- for day in arrow.Arrow.range('day',week,week.shift(days=6)) -%}
            {%- set items = content(date=day.format('YYYYMMDD')) -%}
            <td class="{{['entries' if items.entries else 'empty',
            'thismonth' if day.month==month.month else 'othermonth',
            'today' if day.date() == arrow.get().date() else 'future' if day.date() > arrow.get().date() else 'past']|join(' ')}}"><time datetime="{{day.format('YYYY-MM-DD')}}">{{day.format('D')}}</time>
                {%- if items.entries -%}
                <ul>
                    {%- for entry in items.entries -%}
                    <li class="{{entry.type}}"><a href="{{entry.link}}">{{entry.title}}</a></li>
                    {%- endfor -%}
                </ul>
                {%- endif -%}
            </td>
            {%- endfor -%}
        </tr>
        {%- endfor -%}
    </tbody>
</table>

{%- endmacro -%}
```

You can now use `render_calendar` to display a calendar that shows days with items on it, where the month will be based on the most recent visible item in the view.

The `week_start` parameter indicates which day of the week the week starts on (1 = Monday, 7 = Sunday).

Each cell in the table will have the following CSS classes:

* `entries` if there are items on that day
* `empty` for days with no items
* `thismonth` for days which are on the current month
* `othermonth` for days which come from neighboring months
* `today` for the current date
* `future` for days in the future
* `past` for days in the past
