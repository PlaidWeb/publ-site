Title: Frequently Asked Questions
Path-Alias: /faq
Entry-Type: sidebar
Date: 2018-04-30 17:01:50-07:00
Entry-ID: 374
UUID: db73553b-e046-47f4-9ee3-8749b7daab2c

.....

## General

### What is Publ, anyway?

It is a content management system (CMS) for publishing to the web. Think of it as filling
a similar niche as Movable Type or Wordpress, only with a focus on heterogenous
content and flexibility.  For [my own personal site](http://beesbuzz.biz/) I need to be able to manage
comics, music, art, photography, a blog, and who knows what else as uniformly
as possible, and I really want RSS/Atom feeds to be the norm again.

Pretty much I want to focus on the "C" in "CMS."

The name, incidentally, is short for "Publish."

### Why not just use Wordpress/Movable Type/Jekyll/Pelican/...?

I actually have played around with a lot of different CMSes, and have mostly used
MT for running my sites in the past. Don't get me wrong, a lot of these CMSes have
a lot going for them! But none of them really fit into the niche I'm looking for,
with this particular combination of features:

* Allowing multiple templates for different parts of the site
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

When I write a post for this I'm writing it in [my text editor of
choice](http://sublimetext.com) and checking it into [the website's GitHub
repository](http://github.com/fluffy-critter/publ.beesbuzz.biz) and pushing it
to the server. But someone else might want to upload the files manually via FTP,
and someone else might want to use an online file editor like
[codeanywhere](https://codeanywhere.com) or map their server's content directory
with [sshfs](https://en.wikipedia.org/wiki/SSHFS) or any other number of things
that suit their particular needs best. And of course a single mechanism might
not even be useful for a single site — republishing content would be best
handled by other tools, like a [cron job](https://en.wikipedia.org/wiki/Cron)
that pulls an external RSS feed, for example.

My *intention* is that there will eventually be a built-in content editor with some
sort of configurable access rules, but that's more of a long-term goal rather
than a necessity for Publ's initial release.

### Great, how do I install it?

Right now there's a [getting started guide](328) which covers the basics of running
it locally, and [this site's files](https://github.com/fluffy-critter/publ.beesbuzz.biz)
includes all of the necessary configuration for deploying on both Heroku and Dreamhost.
There's definitely a lot of work to be done in the documentation area, though;
I would love if someone could write up a clear and simple way for people to
deploy to their platform of choice!

## Design

### What is it written in?

Publ is written in Python (I'm specifically developing against 3.6 and that is
currently a requirement, although I am happy to accept compatibility patches to
support earlier versions), using the [Flask](http://flask.pocoo.org) framework,
and [PonyORM](https://ponyorm.com). For Markdown processing
it's using [Misaka](http://misaka.61924.nl), and for time and date handling it
uses [Arrow](https://arrow.readthedocs.io).

#### Why Flask (and not web.py/pyramids/...)?

Because it's easy to get started with and it's what I know, and provides some
pretty decent flexibility while also having a nice ecosystem of modules that I
might be using in the future.

#### And why PonyORM (and not SQLAlchemy/raw SQL/MongoDB/...)?

Because it's easy to get started with and handles the actual use cases for the
site pretty well. The database itself is just a disposable content index (in fact,
the way Publ currently does a schema upgrade is by dropping
all its tables and re-scanning the content files). I didn't see any need for
anything more "proper" when the only requirements are a glorified key-value store
with some basic indexing; Publ treats the filesystem itself as the source of ground truth.

#### And Misaka?

It's a pretty good Python binding to the
[Hoedown](https://github.com/hoedown/hoedown) Markdown parser, with enough
flexibility for the extensions I want to add. It supports (most) GitHub-flavor
markdown and [MathJax](http://mathjax.org) out of the box, and its design allows
adding further syntax hooks for the supported tokens. The downside is that it's
not feasible to extend it with custom tokens but so far I haven't really found
any need for that.

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

I also like the Python ecosystem for this stuff; Jinja2 templating is
particularly well-suited to the way I think about page render logic, for
example, and is also compatible with plenty of HTML authoring tools.

All that said, I'd love to see other people design similar systems using
whatever choice of platform they prefer — at the very least, it amuses me to
think that someone might make something that is "Publ-ish."

(I *may* have had that pun in mind when I chose the name...)

## Performance

### How are you handling scaling issues?

The CMS's scaling story is basically:

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
more money than me at this and I'd humbly suggest you consider [contributing to
Publ development](https://patreon.com/fluffy).


## Interoperability

### Why don't you support ActivityPub?

I do plan on that being part of the system in the long term, but it's not really
necessary for any of my current requirements. Being able to subscribe to long-
form content is already well-handled by syndication feeds like Atom and RSS, and
ActivityPub is focused more on doing instant push updates for short-form
content. For most uses of public Internet content, [Atom is fine](http://beesbuzz.biz/blog/2535-ActivityPub-hot-take) -- and this can still handle push via [WebSub](https://github.com/w3c/websub) (which Publ also doesn't yet support but adding that would be fairly simple).

I do have plans for supporting friends-only/private content, though, and I could see a future in which ActivityPub providers are used to provide federated authentication. And there's no reason it couldn't also be used to support ActivityPub for push, although it'll take some doing to make it actually work well in that ecosystem.

## Okay, so, how can I help?

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

I also have a [rather large list of to-do items](http://github.com/fluffy-critter/Publ/issues),
most of which are low priority for me. But if there's something you want to help
on, please, by all means, do so!

