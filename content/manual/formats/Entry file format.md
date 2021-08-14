Title: Entry files
Date: 2018-04-02 14:04:32-07:00
Entry-ID: 322
UUID: 9b03da44-da6a-46a7-893a-d4ecbe813681
Path-Alias: /entry-format
Last-Modified: 2019-05-08 07:39:26+00:00

A guide to writing page content for Publ.

.....

## Overall format

Publ entries are files saved as `.md` or `.html` in your content directory. An
entry consists of three parts: Headers, above-the-fold, and below-the-fold (also
known as a "cut").

Here is what an entry might look like:

```publ
Title: My first blog entry
Date: 2018/01/04 12:34PM
Category: /blog/random

Hi, this is my first blog entry. I guess I don't have a lot to say.

.....

Well, maybe a *little* more.
```

## Headers

Headers are, more or less, a series of lines like:

```publ
Header-Name: Header-Value
Another-Header-Name: Header-Value
```

followed by a blank line. (At present, Publ actually uses Python's [RFC 2822](https://tools.ietf.org/html/rfc2822) parser, so in theory you should be able
to do line continuations if that's necessary for some reason.)

You can define whatever headers you want for your
templates; the following headers are what Publ itself uses:

* **`Title`**: The display title of the entry

    **Default value**: None

* <span id="sort-title">**`Sort-Title`**: The sorting title of the entry</span>

    This affects the title for the purpose of [sorting](150#order), but is otherwise unused.
    If none is given it defaults to the entry's display title.

* **`Entry-ID`**: The numerical ID of the entry

    This must be unique across all
    entries and will be automatically assigned if missing. It must also be just
    a number.

    Entry IDs also provide a convenient linking mechanism; this entry has ID of 322 so
    [a link to /322](/322) or [322](322) works fine regardless of where the
    entry gets moved to in the future.

* <span id="date">**`Date`**: The publication date and time</span>

    This can be in any format that [Arrow](http://arrow.readthedocs.io)
    understands. If no timezone is specified it will use the timezone indicated
    in `config.py`.

    **Default value**: the modification time of the entry file (which will be added to the
    file for later).

    If you set this to a non-date value (e.g. `now`) then it will be replaced with the
    file modification time when the file is scanned, as if the header were omitted.

* **`Category`**: Which category to put this entry in

    **Default value:** the entry file's directory

* **`Status`**: The publish status of the entry

    Allowed values:

    * `DRAFT`: This entry is not visible at all
    * `HIDDEN`: This entry is visible when accessed directly, but will not be included in entry listings or in previous/next links
    * `UNLISTED`: A synonym for `HIDDEN`
    * `PUBLISHED`: This entry is visible at all times
    * `SCHEDULED`: Until the publication date, this acts as `HIDDEN`; afterwards, it acts as `PUBLISHED`
    * `GONE`: The entry has been deleted and will not be coming back; attempts to access this entry will result in an HTTP 410 GONE error.
    * `DELETED`: A synonym for `GONE`

    **Default value:** `SCHEDULED`

* **`Slug-Text`**: The human-readable part of the URL

    In some circles this is known as "SEO text."

    **Default value:** the entry title

* <span id="redirect-to">**`Redirect-To`**: A URL to redirect this entry to</span>

    This is useful if you want to remove an entry and redirect to another entry, or if
    you want an entry to be a placeholder for some external content (e.g. when the entry
    was syndicated from an external source).

* <span id="path-alias">**`Path-Alias`**: An alternate path to this entry</span>

    This is useful for providing easy-to-remember short names for an entry, and
    for redirecting old, non-Publ URLs to this entry. For example, if you're
    migrating from a legacy site and you have a URL like
    `http://example.com/blog/0012345.php` you can set a header like:

    ```publ
    Path-Alias: /blog/0012345.php
    ```

    Any number of these may be added to any given URL.

    For example, this entry has a `Path-Alias` of [`/entry-format`](/entry-format),
    and the template format page can be similarly reached at [`/template-format`](/template-format).

    **Note:** A path-alias will never override another entry at its canonical URL;
    however, it can potentially override any other kind of URL, including URLs for
    category views and non-canonical entry URLs.

    You can also optionally specify a category template to use, by writing it after the aliased path:

    ```publ
    Path-Alias: /blog/0012345.php archive
    ```

    which will cause the legacy URL to remap to showing this view within the category using the `archive` template.
    If you would like to just go to the category without any specific template, use `index`.

    The path portion is URL-encoded; for example:

    ```publ
    Path-Alias: /entry%20with%20spaces
    Path-Alias: %28parentheses%29
    ```

    Typically, only whitespace and percent signs must be URL-encoded.

* <span id="path-mount">**`Path-Mount`**: An alternate path to this entry</span>

    This is similar to [`Path-Alias`](#path-alias), except that the browser will not be redirected to the canonical location; for example, if you have an entry like:

    ```publ
    Title: Test
    Category: blog
    Entry-ID: 12345
    Path-Mount: /faq
    ```

    then both `/blog/12345-test` and `/faq` will render as the entry directly.

    Also, unlike `Path-Alias`, if a template is specified, this will be treated as an *entry* template (i.e. there will be an `entry` object and no `view` object).

* <span id="path-canonical">**`Path-Canonical`**: Specify the canonical path to this entry</span>

    **Default value:** `/{category}/{entry id}-{slug text}` (for example, `/articles/general/1924-this-is-a-test`)

    For example, if there's an entry with:

    ```publ
    Title: Test
    Category: blog
    Entry-ID: 12345
    Path-Alias: /faq.html
    Path-Canonical: /faq
    Path-Mount: /faque
    ```

    then any access to `/blog/12345-test`, `/blog/12345`, `/12345`, `/faq.html`, etc. will be redirected to `/faq`.  However, `Path-Mount` paths (`/faque` in the above example) will still be a non-redirecting alias.

    As with `Path-Mount`, if a template is specified then this will be treated as an entry template.

    If you specify more than one `Path-Canonical` header, all but one of them will be treated as `Path-Mount` instead; it is undefined as to which one becomes the canonical path.

* **`UUID`**: A globally-unique identifier for the entry

    While Publ doesn't use this internally, having this sort of generated ID is
    useful for Atom feeds and the like. As such, a UUID will be automatically
    generated if not present.

    It is *highly recommended* (but not technically required) that this be
    unique to every entry, including between different websites.

* <span id="entry-type">**`Entry-Type`**: An arbitrary string which you can use
    to define an entry type</span>

    This allows you to differentiate entry types however you want; with this you
    can, for example, set up something similar to what WordPress and Tumblr call
    "page"-type content, or use this to manage entries within a navigation
    sidebar or a linkroll or the like.

    Note that this is intended for affecting the layout/structure of the site,
    and each entry only has a single type. If you set more than one, only one of
    them will be used (and which one is undefined). For making content that can
    be filtered on multiple criteria, use [tags](#tag) instead.

* <span id="template-override">**`Entry-Template`**</span>: Use the specified
    template instead of `entry` when rendering this entry

* <span id="last-modified">**`Last-Modified`**: The date to use for the
    last-modified time for this entry.</span>

    Like with `Date`, if you set this to a non-date value (e.g. `now`) then it
    will be replaced with the file modification time when the file is scanned.

    **Default value:** the entry's `Date`

* <span id="tag">**`Tag`**: Add the specified tag to the entry. To add more than
    one tag, use separate `Tag:` headers.</span>
* <span id="hiddentag">**`Hidden-Tag`**: Like `Tag`, but the tag will not appear
    in the entry's tag list. This lets you filter an entry without making its
    filter criteria visible.</span>

* <span id="summary">**`Summary`**</span>: A plain-text summary/description of
    the entry. Markdown is supported.

    **Default value:** The first paragraph of text in the entry body.

* <span id="auth">**`Auth`**: A list of permissions for who can and cannot see
    the entry.</span>

    This is a list of identities or groups, separated by spaces.
    Identities/groups which start with a `!` means that they *cannot* access the
    entry. For example, this line:

    ```publ
    Auth: friends !mailto:erik@example.com
    ```

    means that members of `friends` can access the entry, but not
    `erik@example.com` (even if they are a member of `friends`).

    This list can grow arbitrarily long, and the rightmost rule wins.

    There is also a special access group, `*`, which just refers to anyone who
    is logged in; for example:

    ```publ
    Auth: *
    ```

    will be visible to anyone who is logged in, and

    ```publ
    Auth: !*
    ```

    will only be visible to anyone who is *not* logged in. These rules can also
    stack; for example:

    ```publ
    Auth: * !enemies mailto:bob@example.com
    ```

    will be visible to anyone who's logged in except for members of the
    `enemies` group, but `mailto:bob@example.com` will be allowed even if they
    are in `enemies`. This is one way that you can make an entry which is open
    to everyone *except* people who have been blocked, for example.

    Note that identities won't necessarily be an email address; they are only
    listed as such here for illustrative purposes. For example, a Mastodon user
    will appear as e.g. `https://queer.party/@fluffy`. See the [user
    configuration file](1341) and [admin guide](732) for more information.

    ==Note:== Only a single `Auth:` header is supported. If more than one is
    present, only one will be used, and it is undefined as to which one that is.

* <span id="attach">**`Attach`**: Another entry to "attach" to this one, useful for defining arbitrary content sections or the like. This can be by file path or by entry ID.

    This is to be used with the [`entry.attachments`](115#attachments) and [`entry.attached`](115#attached) template functions, as well as the related [view parameters](150#attachments)

## <span id="markdown-extensions">Entry content</span>

After the headers, you can have entry content; if the file has a `.htm` or `.html`
extension it will just render directly as HTML (with internal `href` and `src` links rewritten to local files and entries), but with a `.md` extension it will
render as [Markdown](https://en.wikipedia.org/wiki/Markdown).

Publ supports a number of extensions to Markdown, specifically via [Misaka](http://misaka.61924.nl) (which in turn uses [Hoedown](https://github.com/hoedown/hoedown "My, Earth certainly is full of things!")). The extensions are [configurable](865#markdown_extensions); by default it is configured to resemble [GitHub-flavored markdown](https://guides.github.com/features/mastering-markdown/) with the addition of [Kramdown-style math](https://kramdown.gettalong.org/syntax.html#math-blocks) (which in turn works with [MathJax or KaTeX](https://kramdown.gettalong.org/math_engine/mathjax.html)).

Markdown entries can use code fences, which support syntax highlighting via [Pygments](http://pygments.org); see its [rather large list of syntaxes](http://pygments.org/docs/lexers/). There are [Publ-specific extensions](#fenced-code) to this.

There are also some Publ-specific extensions for things like cuts, image renditions, and galleries.

### Custom tags

* **`.....`**: Indicates the cut from above-the-fold to below-the-fold content (must be on a line by itself)

### <span name="image-renditions">Images</span>

Publ extends the standard Markdown image tag (`![](imageFile)`) syntax with some added features for
generating display-resolution-independent renditions and [Lightbox](http://lokeshdhakar.com/projects/lightbox2/) galleries. The syntax is based on the standard Markdown for an image, which is:

```markdown

![alt text](image-path.jpg "title text")
```

(where `alt text` and `"title text"` are optional), but it adds a few features:

* Multiple images can be specified in the image list, separated by `|` characters; for example:

    ```markdown

    ![](image1.jpg "title text" | image2.jpg | image3.jpg "also title text")
    ```

* Images can be configured by adding `{arguments}` to the filename portion or to the alt text; for example:

    ```markdown
    <!-- A single image being configured -->
    ![](image.jpg{width=320,height=200})

    <!-- Three images configured to a width of 640, with one of them further overridden -->
    ![{width=640}](image1.jpg | image2.jpg{width=320} "this one is narrower" | image3.jpg)
    ```

You can also specify the width and height as the first one or two unnamed arguments to an argument list;
for example, these two invocations are equivalent:

```markdown

![{320,240}](image1.jpg | image2.jpg | image3.jpg)

![{width=320,height=240}](image1.jpg | image2.jpg | image3.jpg)
```

For the shorthand notation, if you want to specify only height you can use `None` for the width, e.g.:

```markdown

![{None,240}](image1.jpg | image2.jpg | image3.jpg)
```

For a full list of the configurations available, please see the manual entry on [image renditions](/image-renditions#arguments).

If the image path is absolute (i.e. starts with a `/`) it will search for the image within the content directory. Otherwise it will search in the following order:

1. Relative to the entry file
2. Relative to the entry category in the content directory

So, for example, if content directory is `content/entries` and your entry is in
`content/entries/photos/my vacation/vacation.md` but indicates a category of `photos`,
and you have your static directory set to `content/static`,
an image called `DSC_12345.jpg` will be looked up in the following order:

1. `content/entries/photos/my vacation/DSC_12345.jpg`
2. `content/entries/photos/DSC_12345.jpg`

Relative paths will also be interpreted, including `../` parent directory paths.

This approach allows for greater flexibility in how you manage your images; the simple
case is that the files simply live in the same directory as the entry file, and in more complex cases
things work in a hopefully-intuitive manner.

Of course, external absolute URLs (e.g. `http://example.com/image.jpg` or `//example.com/protocol-relative.gif`) are still allowed, although they are
more limited in what you can do with them (for example, scaling will be done client-side and cropping
options will not work). Also, keep in mind that URLs that are not under your control may change without notice.

This functionality is also available for links to images; for example:

```markdown
Here is [a graph I made](my-graph.png).
```

In this variant you can also specify the image attributes:

```markdown
Here is [the same graph at smaller size](my-graph.png{320,240}),
and here it is [as a JPEG](my-graph.png{format='jpg'}).
```

Note that these links to images do *not* inherit the default image arguments from the page template (this is by design). And, of course, only a single image is supported.

#### Image sets

To support image sets, the following options can be added to the `alt text` section to wrap the image(s) in a `<div>`:

* **`div_class`**: Sets the `class` attribute on the containing `<div>`
* **`div_style`**: A string or list of strings which are added to the containing `<div>`'s `<style>` element

For example, this Markdown fragment:

```markdown

![{div_class="foo"}](test.jpg | test2.jpg)
```

will produce the equivalent of the following HTML:

```html
<div class="foo"><img src="test.jpg"><img src="test2.jpg"></div>
```

#### HTML tags

HTML `<img>` tags will use their `width` and `height` attributes to determine the image rendition size. For example:

```html
<img src="foo.jpg" width="320" height="200" title="Custom title">
```

is equivalent to:

```markdown

![](foo.jpg{320,200} "Custom title")
```

You can also use most of the Markdown image rendition flags, for example:

```html
<img src="foo.jpg{200,format='png'}" title="Converted to PNG at 200 pixels across">
```

This `<img>` functionality is available on both HTML and Markdown entries.

### <span id="link-targets"></span>Linking to things

Both Markdown and HTML entries support a number of enhancements to how link targets are handled; this allows the transparent use of local file paths in your entries.

In HTML tags, this applies to all `href` and `src` attributes (e.g. `<a href="example.md">link</a>` and `<audio src="example.mp3" controls>`).

In Markdown entries, this also applies to images (e.g. `![](example.jpg)`) and hyperlinks (e.g. `[example link](example.md)`) in addition to applying to embedded HTML content.

<span id="rendition-attrs">In HTML tags, you can also force this to apply to other attributes by prefixing them with a $, which is useful for supporting various JavaScript libraries and the like.</span> For example:

```html
<img $data-ondemand="image.jpg{320,320}">  <!-- becomes <img data-ondemand="/path/to/image_320x320.jpg"> -->

<iframe src="other-entry.md">  <!-- becomes <iframe src="/category/1234-other-entry"> -->

<a href="@some-asset.txt">  <!-- becomes <a href="/static/some-asset.txt"> -->
```


#### Local files

Entries can link to files that are stored within the content directory, using the same relative path rules as images. For example, if you have
a file `term paper.pdf` in the same directory as `my entry.md`, then from the entry you can link to it with:

```markdown
You want to read [my paper](term paper.pdf)? Well here you go!
```

This also works in HTML links; for example:

```html
You want to read <a href="term paper.pdf">my paper</a>? I'm flattered!
```

Any file type is supported; however, keep in mind that an HTML or Markdown file will be interpreted as an [entry](#entry-links). If you would like to
serve one up as just their plain content, you can give it headers like:

```publ
Status: HIDDEN
Entry-Template: _plain
```

and create a `templates/_plain.html` file that is simply:

```jinja
{{entry.body}}
{%- if entry.more -%}
.....
{{entry.more}}
{%- endif -%}
```

#### Static assets

Starting a link target with `@` acts as a shorthand for linking to a file in the static assets directory. For example,

```markdown
[here is a file](@files/file.txt)
```

will link to the file `files/file.txt` within the static files for the site. This is more portable than linking
to the static files directly, e.g. `/static/files/file.txt`.

This also applies to images (e.g. `![](@foo.jpg)` will display the image `/static/foo.jpg`), although it will be
treated the same way as an external image; if you want the image to be scaled to save bandwidth, it is better to
put it into your content tree instead.

When writing HTML, the following is equivalent to the above two examples:

```html
<a href="@files/file.txt">here is a file</a>
<img src="@foo.jpg">
```

#### <span id="entry-links"></span>Entries

You can also link to an entry by its entry ID or by an absolute or relative file path to the source file. This also
supports anchors (`#`). Some examples:

* `[link to entry 322](322)` &rarr; [link to entry 322](322)
* ``[link to `Template format.md`](Template format.md)`` &rarr; [link to `Template format.md`](./Template format.md)
* ``[link to `/faq.md`](/faq.md)`` &rarr; [link to `/faq.md`](/faq.md)
* ``[link to `../api/view.md#order`](../api/view.md#order)`` &rarr; [link to `../api/view.md#order`](../api/view.md#order)

And the HTML equivalents to the above:

```html
<a href="322">link to entry 322</a>
<a href="Template format.md">Link to <code>Template format.md</code></a>
<a href="/faq.md">Link to <code>/faq.md</code></a>
<a href="../api/view.md#order">Link to <code>../api/view.md#order</code></a>
```

As above, you can also use these in any HTML element with the `src`, `href`, or arbitrary attributes annotated with `$`; for example:

```html
<iframe src="some entry.md"></iframe> <!-- by filename -->
<div $data-popup="12345#anchor"></div> <!-- by entry ID -->
```

### <span id="fenced-code">Fenced code blocks</span>

As is typical for Markdown, Publ supports fenced code blocks, with a syntax like:

````markdown
```language
Text goes here
More text
More text
```
````

#### Syntax extensions

Publ allows you to add a title to a fenced code block, by putting it on the first line and prefixed with `!`:

````markdown
```python
! example.py
def foo():
    return None
```
````

This will render as:

```python
! example.py
def foo():
    return None
```

Note: If you need the first line of code to start with a literal `!` character, put a blank line before it, or prefix it with a `\`. For example,

````markdown
```markdown
\![alt text](image.jpg "This is an image")
```
````

renders as:

```markdown
\![alt text](image.jpg "This is an image")
```

You can also provide template override arguments to the code block by putting parameters after the language declaration; for example:

````markdown

```{code_number_links=False}
This block has had its line number links suppressed.
```

```bash{code_highlight=False}
cat << EOF
This code has had highlighting disabled.

Test 1
Test 2
EOF
```
````

These render as:

```{code_number_links=False}
This block has had its line number links suppressed.
```

```bash{code_highlight=False}
cat << EOF
This code has had highlighting disabled.

Test 1
Test 2
EOF
```


#### HTML output

The overall code block structure is:

```html
<figure class="blockcode">
    <figcaption>
        Block caption
    </figcaption>
    <pre>
        /* code goes in here */
    </pre>
</figure>
```

If a language is specified, the `<pre>` also gets `class="highlight"` and a `data-language` attribute that is set to the language.

If code highlighting is enabled, the code is also run through [Pygments](https://pygments.org/).

If line number links are enabled, the `<pre>` gets an empty attribute of `data-line-numbers`.

Each line is wrapped in a `<span class="line">` and a `<span class="line-content">`, to allow for additional CSS formatting. If both `code_highlight` and `code_number_links` are enabled, there will also be a `<a class="line-number"></a>` inserted before the `line-content` span, and the `line` span will have an ID that this links to. This allows for code-line permalinks:

```html
<pre>
    <span class="line" id="xxxL1">
        <a class="line-number" href="#xxxL1"></a>
        <span class="line-content">first line</span>
    </span>
    <span class="line" id="xxxL2">
        <a class="line-number" href="#xxxL2"></a>
        <span class="line-content">second line</span>
    </span>
    <span class="line" id="xxxL3">
        <a class="line-number" href="#xxxL3"></a>
        <span class="line-content">third line</span>
    </span>
   ...
</pre>
```

This markup is intended to be used with [CSS counters](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Lists_and_Counters/Using_CSS_counters) to actually add the line numbering, which allows copy-and-paste to still function correctly. For a minimal example:

```css
.highlight {
    counter-reset: codeline;
}

.highlight .line-number::before {
    content: counter(codeline);
    display: inline-block;
    min-width: 3em;
}

```

For a more thorough example of how to format fancy code, look at the [code block CSS file](@fancy-code.css) for this website.
