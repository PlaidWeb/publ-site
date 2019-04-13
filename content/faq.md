Title: Frequently Asked Questions
Path-Alias: /faq
Entry-Type: sidebar
Date: 2018-04-30 17:01:50-07:00
Entry-ID: 374
UUID: db73553b-e046-47f4-9ee3-8749b7daab2c
Last-Modified: 2019-02-21 05:24:49+00:00

.....

## General

### What is Publ, anyway?

Publ is a website **publ**ishing system, with a focus on heterogenous content and flexibility, and with simple content management principles.

For [my own personal site](http://beesbuzz.biz/) I need to be able to manage
comics, music, art, photography, a blog, and who knows what else as in a simple, uniform manner, while also supporting [IndieWeb](http://indieweb.org) principles.

### Is Publ a CMS?

That depends on how you define "CMS." At the most basic, it is one -- it manages and renders content to be published to a website, after all -- but the term "CMS" has a history of implying something more complicated, with an integrated end-to-end asset management pipeline and database-driven post editor.

I do sometimes refer to Publ as a CMS but for the above reason I prefer to think of it as a "publishing system" or "like a static site generator, but dynamic."

### Why not just use one of the many existing publishing systems?

Oh, gosh, yes, there *are* [a lot of publishing systems](https://en.wikipedia.org/wiki/List_of_content_management_systems) out there! Movable Type, Wordpress, Pelican, Jekyll/Octopress, Drupal, GetSimple, not to mention proprietary hosted ones like Tumblr, Facebook, SquareSpace, Wix, Remixer, as well as the old-school hand-written HTML or PHP-with-minor-templating...

I actually have played around with a lot of them, and have historically mostly used
[Movable Type](http://movabletype.org) for running my own sites. Don't get me wrong, a lot of these platforms have
a lot going for them, and work very well for a lot of people! But none of them really fit into the niche I was looking for,
with this particular combination of features:

* Allowing multiple templates for different parts of a single site
* Ensuring the ability to reorganize content (or import content from other systems) and have permalinks remain valid
* Having MVC-style routing rules that allow for future expansion
* Keeping pages and their content together
* Providing dynamic image renditions which are:
    * CDN-friendly
    * Template-driven
    * Multi-resolution/high-DPI-aware
    * Not prone to denial-of-service attacks
* Stable pagination (i.e. an archive page's link should always point to the same content regardless of when a search engine indexed it)

I had ended up hacking a lot of this functionality into my Movable Type templates
but as I mentioned on [the first blog entry](325), this got incredibly unwieldy and difficult!

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

My *intention* is that there will eventually be an online content editor that integrates with Publ, but this doesn't necessarily have to be written by me or work in any particular way. My vision for one is  a web-based file manager and a Publ-oriented Markdown editor, but maybe someone else would have a different (possibly better) idea.

### How do I use it?

Right now there's a [getting started guide](328) which covers the basics of running
it locally and setting up a basic site, and [this site's files](/github-site)
includes all of the necessary configuration for deploying on both Heroku and Dreamhost.
There's definitely a lot of work to be done in the documentation area, though;
I would love if someone could write up a clear and simple way for people to
deploy to their platform of choice!

## Design

### What is it written in?

Publ is written in Python (I'm specifically developing against 3.7 and targeting 3.5 as a minimum, although I am happy to accept compatibility patches to
support earlier versions), using the [Flask](http://flask.pocoo.org) framework,
and [PonyORM](https://ponyorm.com) for its content indexing. For Markdown processing
it's using [Misaka](http://misaka.61924.nl), and for time and date handling it
uses [Arrow](https://arrow.readthedocs.io). It also uses [watchdog](https://github.com/gorakhargosh/watchdog)
to watch the content store for changes.

#### Why Flask (and not web.py/pyramids/...)?

Because it's easy to get started with and it's what I know, and provides some
pretty decent flexibility while also having a nice ecosystem of modules that I
might be using in the future.

#### And why PonyORM (and not SQLAlchemy/raw SQL/MongoDB/...)?

Because it's easy to get started with and handles the actual use cases for the
site pretty well. The database itself is just a disposable content index (in fact,
the way Publ currently does a schema "upgrade" is by dropping
all its tables and re-scanning the content files). I didn't see any need for
anything more "proper" when the only requirements are a glorified key-value store
with some basic ordered indexing; Publ treats the filesystem itself as the source of ground truth.

#### And Misaka?

It's a pretty good Python binding to the
[Hoedown](https://github.com/hoedown/hoedown) Markdown parser, with enough
flexibility for the extensions I want to add. It supports (most) GitHub-flavor
markdown and [MathJax](http://mathjax.org) out of the box, and its design allows
adding further syntax hooks for the supported tokens. The downside is that it's
not feasible to extend it with custom tokens but so far I haven't really found
any need for that anyway.

### Why didn't you use PHP/Haskell/Go/Ruby/Rust/...?

I tend to dislike PHP for many reasons, both with the language itself and with
its ecosystem. While I wouldn't go so far as to say that PHP-the-language is
irredeemably bad, there are some [pretty fundamental problems with its security
model](246) that make it somewhat undesirable. Also, setting up a flexible
request routing mechanism is way too varied and error-prone with the PHP
ecosystem (`.htaccess` on Apache, fiddly `location` rules on nginx, etc.), and I
haven't found any MVC-style routing/templating systems I'm happy with.

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

I haven't yet investigated what it will take to support RST. It is certainly within the realm of possibility, although at a glance I am not sure its concept of image handling quite fits in with Publ's design.

### What about AsciiDoc?

It is also on my radar, but like reStructuredText I haven't investigated its suitability for use in Publ.

## Performance

### How are you handling scaling issues?

Publ's scaling story is basically:

* Limit the complexity of request routing
* Make everything cache-friendly
* Defer as much to background tasks as possible

Request routing is limited to just a handful of routes which can do all of their
decisions based on what's in the index database, and the index database is kept
pretty much to the minimum (aside from small amounts of data that are useful for
presentation, like entry titles).

Cache-friendliness goes hand-in-hand with stable pagination and template-driven
image renditions (which in turn rely on the content hashes of the images to
determine if a rendition needs to be regenerated).

And, the content indexer and image renditions all use decoupled background
workers to do their heavy lifting, with some simple tricks to fake asynchronous
image retrieval in the client.

### What if caching just isn't enough?

If a site gets to the point that throwing a fronting cache isn't enough to get
good performance, it should be fairly simple to scale it horizontally by deploying
the same site to multiple servers and load-balance between them.

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
more money than me at this and I'd humbly suggest you consider [showing your support](https://liberapay.com/fluffy).


## Interoperability

### Do you support ActivityPub?

At some point I will write a longer piece on why ActivityPub has an impedance mismatch with Publ's design goals, but in the meantime you can read an [off-the-cuff rant about it](http://beesbuzz.biz/blog/2535-ActivityPub-hot-take).

That said, it is fairly simple to support ActivityPub using [Bridgy Fed](https://fed.brid.gy) together with [Pushl](1295); this very site is [configured to use that](https://github.com/PlaidWeb/publ-site/blob/384e2c9bca9c25dedde3e9d68f682f2872db15be/main.py#L96), and should be followable at `@publ.beesbuzz.biz@publ.beesbuzz.biz` on your WebFinger-enabled social network of choice, although the experience isn't particularly great.

### What about Webmention, WebSub, ...?

Publ is only one piece of a puzzle for a rich [IndieWeb](http://indieweb.org) experience. It is intended to provide the publishing and content management aspects of a site, and allow the use of other, simple tools for other parts of the ecosystem.

To that end, the intention is that things like outgoing Webmention and WebSub are left to external tools. One such tool is [Pushl](1295) to provide the notification conduit between Publ (or any other publishing system, static or dynamic!) and the various push infrastructure that is emerging around the IndieWeb.

As far as incoming Webmentions are concerned, most of that comes down to selecting whatever endpoint you want. There is already a rich ecosystem of Webmention endpoints that are available for use now (I use [webmention.io](http://webmention.io), personally), and I haven't seen any compelling reason to integrate one into Publ directly.

### What about adding other functionality?

Being built in Flask, it is a simple matter to add additional routes to any Publ instance, by simply registering them with Publ's routing rules. Any Flask-specific plugin should Just Work out of the box, and building API endpoints that wrap existing libraries is quite straightforward.

This is of course not anything special to Publ.

### What about having multuple Publ instances on a single running server?

Unfortunately, that is not so straightforward. Currently, the ORM in use does not support segregating data across instances, and as such I also haven't put much effort into containerizing the Publ configuration (which is currently global). However, I haven't found a good use case for multiple Publ sites conmingled in a single app server anyway; if you can think of one, feel free to [open an issue](/newissue) and make your case for it!

### Do you have any importers from other blogging platforms?

If you want to convert a Movable Type blog's content over, see [mt2publ](https://github.com/PlaidWeb/mt2publ).

There currently aren't any converters for other blogging systems, but since the [entry file format](/entry-format) is so simple, it shouldn't be too difficult to write converters from other systems either.

## Troubleshooting

### I get `OSError: [Errno 8] Exec format error: '/path/to/main.py'` when running in debug

Flask 0.15 changed the way the automatic reload works, which makes it so that if `main.py` is set executable, this will
fail. (See [an associated GitHub issue](https://github.com/pallets/werkzeug/issues/1482) for more information.)

If you're on Linux or macOS, the easiest solution is to make sure that `main.py` is not set executable, with e.g.

```bash
chmod a-x main.py
```

A more general fix (which includes Windows) is to use the `flask run` script instead:

```bash
FLASK_ENV=development FLASK_DEBUG=1 FLASK_APP=main.py pipenv run flask run
```

The scripts bundled with the [publ-site repository](https://github.com/PlaidWeb/publ-site) have been updated accordingly.


## How can I help out?

Glad you asked!

Where I could use the most help right now:

* Building example templates/themes for people to use

* Improving the deployment mechanism and documentation thereof

* Improving the documentation for everything (in particular there needs to be
some sort of "quick start" guide to get people going with writing/using
templates, and explaining how the heck to use Publ in the first place!)

* Improving the code quality — currently all testing is via ad-hoc smoke tests,
and I'm still relatively inexperienced in Python so I'm sure a lot of places
where the code could be better/cleaner/more Pythonic

* Making the Publ site look nicer in general

* Writing more converters for other blog platforms

I also have a [rather large list of to-do items](/issues),
most of which are low priority for me. But if there's something you want to help
on, please, by all means, do so!

