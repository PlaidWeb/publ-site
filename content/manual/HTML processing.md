Title: HTML processing
Path-alias: /html-processing

How to configure HTML processing in templates

.....

## HTML and Markdown options

Anywhere that Markdown or HTML is processed from a content file, the following parameters apply:

* The standard [image rendition arguments](/image-renditions#arguments)
* **`absolute`**: Set to True to force all links to be absolute (rather than relative); for HTML, this applies to all `href`, `src`, and [rendition](322#rendition-attrs) attributes.
* **`markup`**: Whether to include any markup in the title; defaults to `True`, but should be set to `False` where HTML markup isn't valid.

    For example, markup isn't allowed in the HTML `<title>` tag:

    ```html
    <html>
    <head><title>{{ entry.title(markup=False) }}</title></head>
    <body><h1>{{ entry.title }}</h1></body>
    </html>
    ```

    Nor is it valid in HTML attributes:

    ```html
    <a href="{{category.link}}" title="{{category.description(markup=False)}}">{{category.name}}</a>
    <a href="{{entry.link}}" title="{{entry.title(markup=False)}}">{{entry.title}}</a>
    ```

## Markdown-only options

The following options only apply to Markdown content:

* **`smartquotes`**: Set to `True` to enable automatic smartquote substitution, or `False` to disable it (necessary in e.g. Atom feeds). Defaults to `True`.
* **`no_smartquotes`**: The opposite of `smartquotes`, provided for backwards compatibility; if `smartquotes` is set then this is ignored.
* **`markdown_extensions`**: A list of extensions to configure the Markdown formatter with; defaults to the global configuration.
* **`xhtml`**: Set to `True` to render as XHTML instead of HTML (default: `False`)

Note that an entry's title is always treated as Markdown, even if the entry itself is HTML.