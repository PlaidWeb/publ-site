Title: Frequently Asked Questions
Path-Canonical: /faq
Entry-Type: sidebar
Date: 2018-04-30 17:01:50-07:00
Entry-ID: 374
UUID: db73553b-e046-47f4-9ee3-8749b7daab2c
Last-Modified: 2019-02-21 05:24:49+00:00

.....

## General

### What is Publ, anyway?

Publ is a website **publ**ishing system, with a focus on heterogenous content
and flexibility, and with simple content management principles.

For [my own personal site](http://beesbuzz.biz/) I need to be able to manage
comics, music, art, photography, a blog, and who knows what else as in a simple,
uniform manner, while also supporting [IndieWeb](http://indieweb.org)
principles.

### How is it pronounced?

Like "puddle," but with a B instead of a D. Or, "publish" without the "ish."

### Is Publ a CMS?

That depends on how you define "CMS." At the most basic, it is one --- it
manages and renders content to be published to a website, after all --- but the
term "CMS" has a history of implying something more complicated, with an
integrated end-to-end asset management pipeline and database-driven post editor.

I do sometimes refer to Publ as a CMS but for the above reason I prefer to think
of it as a "publishing system" or "like a static site generator, but dynamic."

#### How is it "like a static site generator?"

Most static site generators allow you to organize your content in the form of
HTML or Markdown files organized loosely in a filesystem, and have those files
appear as pages on the website. These files are the "ground truth" of what
constitutes the authoritative data; content can be managed with whatever tools
you like, and versioning and collaboration can take place using any number of
systems such as git or cloud-based file storage like Dropbox or NextCloud.

Static site generators also generally allow you to provide your original,
full-resolution images, and then use template configuration or the like to cut
renditions for view on the public webpage.

#### But it's dynamic?

Static site generators are great for performance --- they're just generating
their files once and then being served statically, after all --- but they lack a
lot of flexibility. You have to go out of your way to support things like
scheduled posts, for example, and there's no safe way to share content with a
restricted audience. Support for archive pages is generally limited to only
date-based archives, or if there are paginated archives, the archive pages tend
to change over time, so a snapshot of one page of the website's content archive
might not necessarily show the same content as it would at present. It also
becomes unwieldy to have rich support for tag filtering; generally you only
allow browsing a single tag at a time.

Publ, on the other hand, supports all of the above, and also allows for a few
additional things that are difficult or unwieldy to support in a static site.
For example, if you move content around on the site, accesses to an old URL will
automatically get redirected to the current one, and you can also set up URL
mappings for imported content, or provide easy-to-remember aliases. You can even
completely override the way that entry URLs are generated --- such as on this
very FAQ!

Publ does have a database, but it serves only as an index to content on the
filesystem, rather than being actual content storage. Since the filesystem is
the ground truth of the website, there is no need to migrate or maintain the
database. You can change hosts, revert to old versions, or heck, outright delete
the database if something goes wrong, and it'll just get rebuilt by Publ.

Basically, Publ gives you the best of both worlds, with very few drawbacks.

#### What are some of the drawbacks?

The big one is that you need to be able to host Python applications, which
normally requires somewhat better web hosting than your typical shared hosting
plan (although there are shared hosting providers which support Python
applications).

On that note, it does take a bit more technical know-how to set this up compared
to a typical PHP or static site. However, there are [deployment
guides](/manual/deploying/) to provide that information for a number of known
hosting scenarios.

Finally, you'll probably need at least a basic understanding of HTML and CSS to
set up your own site, and be willing to learn
[Jinja](https://jinja.palletsprojects.com/) templating. Hopefully there will
eventually be a rich ecosystem of existing templates you can draw from, though!

### Why not just use one of the many existing publishing systems?

Oh, gosh, yes, there *are* [a lot of publishing
systems](https://en.wikipedia.org/wiki/List_of_content_management_systems) out
there! Movable Type, Wordpress, Pelican, Jekyll/Octopress, Drupal, GetSimple,
Hugo, not to mention proprietary hosted ones like Tumblr, Facebook, SquareSpace,
Wix, Remixer, as well as the old-school hand-written HTML or
PHP-with-minor-templating...

I actually have played around with a lot of them, and have historically mostly
used [Movable Type](http://movabletype.org) for running my own sites. Don't get
me wrong, a lot of these platforms have a lot going for them, and work very well
for a lot of people! But none of them really fit into the niche I was looking
for, with this particular combination of features:

* Allowing multiple templates for different parts of a single site
* Ensuring the ability to reorganize content (or import content from other systems) and have permalinks remain valid
* Having flexible routing rules that allow for future expansion
* Keeping pages and their content together
* Providing dynamic image renditions which are:
    * CDN-friendly
    * Template-driven
    * Multi-resolution/high-DPI-aware
    * Not prone to denial-of-service attacks
* Stable pagination (i.e. an archive page's link should always point to the same content regardless of when a search engine indexed it)
* Support for protected/private/restricted entries using existing authentication systems

It certainly is *possible* to add all of this to some of the existing publishing systems, but building something from the ground up with these features in mind allowed for a much cleaner design and more flexibility.

### What does the UI look like?

It actually doesn't have one! And this is by design. I don't want to force people
into a specific content management mindset. The software primarily indexes separate
content files, and uses that to present them in a way appropriate to the content
in question.

When I write a post for this I'm writing it using Markdown or HTML in [my text editor of
choice](http://sublimetext.com) and checking it into [the website's GitHub
repository](/github-site) and pushing it
to the server. But someone else might want to upload the files manually via FTP,
and someone else might want to use an online file editor like
[codeanywhere](https://codeanywhere.com) or map their server's content directory
with [sshfs](https://en.wikipedia.org/wiki/SSHFS) or any other number of things
that suit their particular needs best. And of course a single mechanism might
not even be useful for a single site — republishing content would be best
handled by other tools, like a [cron job](https://en.wikipedia.org/wiki/Cron)
that pulls an external RSS feed, for example.

My *intention* is that there will eventually be an online content editor that integrates with Publ, but this doesn't necessarily have to be written by me or work in any particular way. My vision for one is a web-based file manager and a Publ-oriented Markdown editor, but maybe someone else would have a different (possibly better) idea.

### How do I use it?

Right now there's a [getting started guide](328) which covers the basics of
running it locally and setting up a basic site, and [this site's
files](/github-site) should be fairly straightforward to get running on any
compatible hosting platform.

There are also some [deployment guides](/manual/deploying/) that cover a few common usage scenarios.

Documenting more deployment methods is an area that I would definitely appreciate
contributions on!

## Design

### What is it written in?

Publ is written in Python, using the [Flask](https://flask.palletsprojects.com/)
framework, and [PonyORM](https://ponyorm.com) for its content indexing. For
Markdown processing it's using [Misaka](http://misaka.61924.nl), and for time
and date handling it uses [Arrow](https://arrow.readthedocs.io). It also uses
[watchdog](https://github.com/gorakhargosh/watchdog) to watch the file-based
content store for changes.

#### Why Flask (and not web.py/pyramids/...)?

Because it's easy to get started with and it's what I know, and provides some
pretty decent flexibility while also having a nice ecosystem of modules that I
might be using in the future.

#### And why PonyORM (and not SQLAlchemy/raw SQL/MongoDB/...)?

Because it's easy to get started with and handles the actual use cases for the
site pretty well. The database itself is just a disposable content index (in
fact, the way Publ currently does a schema "upgrade" is by dropping all its
tables and re-scanning the content files). I didn't see any need for anything
more "proper" when the only requirements are a glorified key-value store with
some basic ordered indexing; Publ treats the filesystem itself as the source of
ground truth.

#### And Misaka?

Misaka is a pretty good Python binding to the
[Hoedown](https://github.com/hoedown/hoedown) Markdown parser, with enough
flexibility for the extensions I want to add. It supports (most) GitHub-flavor
markdown and [MathJax](https://mathjax.org/)/[KaTeX](https://katex.org/) out of the box, and its design allows
adding further syntax hooks for the supported tokens. The downside is that it's
not feasible to extend it with custom tokens but so far I haven't really found
any need for that anyway.

That said, Misaka needs to be replaced, but that's an [enormous task](https://github.com/PlaidWeb/Publ/issues/261).

### Why didn't you use PHP/Haskell/Go/Ruby/Rust/...?

I tend to dislike PHP for many reasons, both with the language itself and with
its ecosystem. While I wouldn't go so far as to say that PHP-the-language is
irredeemably bad, there are some [pretty fundamental problems with its security
model](246) that make it somewhat undesirable. Also, setting up a flexible
request routing mechanism is way too varied and error-prone with the PHP
ecosystem (`.htaccess` on Apache, fiddly admin-managed `location` rules on
nginx, etc.), and I haven't found any routing or templating systems I'm happy
with.

As far as other languages go, one of my primary concerns was making it
deployable in as many places as possible, including various forms of shared
hosting, which imposes pretty strict limitations on choices of language and
runtime memory requirements. At one point I was specifically targeting
Dreamhost, which only allows PHP, Python, and Ruby apps, and while Dreamhost
is [no longer a primary target](358) it still informed my decisions.

Also, while I'm far from a Python expert, I know it way better than any of the
other languages people suggest for this purpose!

All that said, I'd love to see other people design similar systems using
whatever choice of platform they prefer — at the very least, it amuses me to
think that someone might make something that is "Publ-ish."

(I *may* have had that pun in mind when I chose the name...)

### Why Markdown and not reStructuredText?

I haven't yet investigated what it will take to support RST. It is certainly
within the realm of possibility, although at a glance I am not sure its concept
of image handling quite fits in with Publ's design.

### What about AsciiDoc?

It is also on my radar, but like reStructuredText I haven't investigated its
suitability for use in Publ.

## Performance

### How are you handling scaling issues?

Publ's scaling story is basically:

* Limit the complexity of request routing
* Make everything cache-friendly

Request routing is limited to just a handful of routes which can do all of their
decisions based on what's in the index database, and the index database is kept
pretty much to the minimum (aside from small amounts of data that are useful for
presentation, like entry titles).

Cache-friendliness goes hand-in-hand with stable pagination and template-driven
image renditions (which in turn rely on the content hashes of the images to
determine if a rendition needs to be regenerated).

And, the content indexer uses a decoupled background worker to do the heavy lifting.

### What if caching just isn't enough?

If a site gets to the point that throwing a fronting cache isn't enough to get
good performance, it should be fairly simple to scale it horizontally by
deploying the same site to multiple servers and load-balance between them.

If this situation comes up, it will be pretty important that at least one of the
following is true:

* The load balancer has strong connection affinity, so that the image rendition
retrieval goes to the same server that handled the page render

* The site is configured with an external CDN which is able to retrieve from all
of the backing servers as an origin, and can try them all until one handles the
request properly

In the future, if any sites actually get to the point that horizontal scaling is
necessary, it will be fairly straightforward to implement a third option:

* Configure the rendition cache to write to a shared storage bucket (via NFS,
sshfs, S3, etc.) which acts as the CDN origin

If you are running a site which gets to this point then clearly you're making
more money than me at this and I'd humbly suggest you consider [showing your
support](https://github.com/sponsors/fluffy-critter).

## Interoperability

### Do you support ActivityPub?

Not at present. While I do want to support it natively (particularly for better
interoperability with Mastodon and the like), ActivityPub's design makes for
some pretty major challenges when it comes to supporting it.

My future plans for ActivityPub support involve making a separate actor that
Publ can interoperate with, rather than making it built-in functionality.

At present, it's fairly straightforward to use [Bridgy Fed](https://fed.brid.gy)
together with [Pushl](1295) as such an actor, although that comes with several
limitations (such as no support for private posts, no content relocation/update
support, and only a single global outbox for the entire site).

### What about Webmention, WebSub, ...?

Publ is only one piece of a puzzle for a rich [IndieWeb](http://indieweb.org)
experience. It is intended to provide the publishing and content management
aspects of a site, and allow the use of other, simple tools for other parts of
the ecosystem.

To that end, the intention is that things like outgoing Webmention and WebSub
are left to external tools. One such tool is [Pushl](1295) to provide the
notification conduit between Publ (or any other publishing system, static or
dynamic!) and the various push infrastructure that is emerging around the
IndieWeb.

As far as incoming Webmentions are concerned, most of that comes down to
selecting whatever endpoint you want. There is already a rich ecosystem of
Webmention endpoints that are available for use now (such as
[webmention.io](https://webmention.io)), and there are a number of ways that you
can display incoming mentions on a Publ site, such as using
[webmention.js](https://github.com/PlaidWeb/webmention.js) or configuring your
webmention endpoint to convert incoming webmentions into an [entry
attachment](322#attach) or the like.

As with ActivityPub, my long-term plans involve building native IndieWeb support
as an additional module that's designed to interoperate with Publ, as opposed to
making it native built-in functionality (most likely making it part of the
ActivityPub actor, since there is so much common functionality between them).

### What about adding other functionality?

Being built in Flask, it is generally a simple matter to add additional routes
to any Publ instance, by simply registering them with Publ's routing rules. Any
Flask-specific plugin or blueprint should Just Work out of the box, and building
API endpoints that wrap existing libraries is quite straightforward.

This is of course not anything special to Publ.

Custom Flask endpoints can also make use of the [internal Python API](865) for
querying and formatting entries.

### What about having multuple Publ instances within a single running site?

Unfortunately, running multiple Publ instances within a single app server
is not so straightforward. I haven't found a good use case for
multiple Publ sites conmingled in a single app server anyway; if you can think
of one, feel free to [open an issue](/newissue) and make your case for it!

That said, it's straightforward to have different Publ instances for different
subdomains or mount points (configured at the HTTP server level).

### Do you have any importers from other blogging platforms?

If you want to convert a Movable Type blog's content over, see [mt2publ](1083).

There currently aren't any converters for other blogging systems, but since the
[entry file format](/entry-format) is so simple, it shouldn't be too difficult
to write converters from other systems.

## Deployment

### Can this be used with Docker?

In principle, yes, although I haven't personally investigated how to do that.
Publ, like most Python apps, is intended to run in a Python virtual environment
which already provides a decent level of deployment abstraction and portability,
and if used with SQLite, it's already pretty much self-contained. It also goes
to great lengths to behave nicely in a shared cache, which scales far better
(from a resource-utilization standpoint) than having a per-VM cache. As such,
Docker support hasn't been a priority for me.

However, I do understand the appeal to Docker for configuration and deployment
management purposes, and I would not turn away an appropriate [deployment
guide](/manual/deploying/), ideally with a sample `Dockerfile`.

(If you do write one, please have a version where the `content/` directory is
external and not a part of the build!)

## How can I help out?

Glad you asked!

Where I could use the most help right now:

* Building example templates/themes for people to use

* Improving the documentation for everything (in particular there needs to be
some sort of "quick start" guide to get people going with writing/using
templates, and explaining how the heck to use Publ in the first place!)

* Improving the code quality, especially where automated testing is concerned

* Making the Publ site itself prettier and more informative, both in terms of
feature demonstration and documentation quality

* Writing more converters for other blog platforms

I also have a [rather large list of to-do items](/issues), most of which are low
priority for me. But if there's something you want to help on, please, by all
means, do so!

