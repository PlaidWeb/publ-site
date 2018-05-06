Title: The Trouble with PHP
Date: 2018-05-07 00:00:00-07:00
Entry-ID: 246
UUID: bed88efa-a822-4a13-acaf-77df79bb0a12

I've had people ask me why I'm not building Publ using PHP. While [much](http://phpsadness.com)
has been [written](https://www.quaxio.com/wtf/php.html) on this [subject](http://tracks.ranea.org/post/13908062333/php-is-not-an-acceptable-cobol) from
a standpoint of what's wrong with the language (and with which I agree quite a lot!), that isn't, to me, the core of the problem with PHP on the web.

So, I want to talk a bit about some of the more fundamental issues with PHP, which actually goes back well before PHP even existed and is intractibly linked with
the way PHP applications themselves are installed and run.

(I will be glossing over a lot of details here.)

.....

### Some history

Back when the web was first created, it was all based around serving up static files. You'd have an HTML file (usually served up from a `public_html` directory
inside your user account on some server you
had access to, which was sometimes named or aliased `www` but more often was just some random machine living on your university's network), and it
acted much like a simplified version of FTP — someone would go to a URL like `http://example.com/~username/` and you'd see an ugly directory index of the
files in there (if you didn't override it with an `index.html` or, more often in those days, `index.htm`), and then someone would click on the page
they wanted to look at like `homepage3.html` and it would retrieve this file and whatever flaming skull .gif files it linked to in an `<img>` tag and the copy of `canyon.mid` you put an `<embed>` around, and that would be that. The web server was really just a file server that happened to speak HTTP.

Then one day, servers started supporting things called SSIs, short for "[server-side includes](https://en.wikipedia.org/wiki/Server_Side_Includes)." This let you do some very simple templatization of your
site; the server wouldn't just serve up the HTML file directly, but it would scan it for simple SSI tags that told the server to replace this tag
with another file, so that you could, for example, have a single navigation header that was shared between all your pages, and a common
footer or whatever.

But this mechanism was still pretty limited, and so about two minutes later someone came up with the idea of the [Common Gateway Interface](https://en.wikipedia.org/wiki/Common_Gateway_Interface), or CGI;
this would make it so the server would see a special URL like `/cgi-bin/formail.pl` and instead of serving up the content of the file, it would
run the file as a separate program and serve up its output.

At this time, HTTP generally used just a single verb, `GET`, which would get a resource. CGI needed a way of passing in parameters to the
program. Instead of just running the program like a command line (which would be very insecure), they passed in parameters through
environment variables; for example, if the user requested the "file" at `/cgi-bin/formail.pl?email=fwiffo@example.com&text=Hi+I+like+your+site!`,
the web server would set the environment variable `QUERY_STRING` to the value of everything after the `?`, which `formail.pl` would then
parse out.

If the `POST` verb were used instead, then the server would also read some additional data from the user's web browser and then send that
to the script via its standard input.

Basically, the web server was no longer just a file server, but a primitive command processor.

### Early security

Back when this first started, system administrators knew better than to let just *anyone* run just *any* program from the web server.
After all, people might do silly things like make it very easy to execute arbitrary commands on the server — and since the web server
often ran as the root/administrator user, this would be very bad indeed. Even the admins who were savvy enough to set up a special
sandbox user for the HTTP server would still need it to run everything from a common, trusted account that might have had
access to common areas of the server.

So, the usual approach was to have just a single `/cgi-bin/` directory with *trusted* programs that were vetted and installed by
the administrator, for things that they felt were important or useful for everyone to have. Usually this would be things like
standard guest books (the great-great-grandfather to comment sections) or email contact forms (since spam was starting to become
a problem and it was already dangerous to put your email address on the public web).

Back in these days people generally didn't have a database — after all, Oracle was expensive — and it didn't really matter anyway;
if you wanted to have a complex website you'd just run some sort of static site generator (which was often written in tcsh or Perl or
something) and if you needed scheduled posts you'd do it by having a `cron` job periodically update things. So, it wasn't really
that much of an impediment to have this setup.

If you were really savvy and wanted to run, say, an interactive online multiplayer game of your own design, you'd simply
run your own server (often under your desk in your dorm room) and you'd have root access and could install everything you
wanted in `/cgi-bin/`.

Because *everything* in `/cgi-bin/` was run as a program, you knew better than to let your scripts save other files into
that same directory; if it was a thing where people could upload files or post comments, it's not like it would do any
good anyway (since then the server would try to run them as programs, and you can't run a .jpg).

### Shared hosting

Then as the web really started to take off, shared hosting providers started appearing, and CGI access became a pretty
commonly-requested high-end feature. Generally the shared hosting providers didn't want to let just *anyone* upload a
script to be run by the server, but they also didn't want to have to manually vet each and every script that users
wanted to install. So, as a compromise, they set up special rules so that within your own server space you could have a `/cgi-bin/` directory
and that things run from that directory would run under your account, rather than as the web server (using a mechanism called `suexec`).

This provided a pretty good compromise; users still had to know what they were doing in order to install their scripts, but they still
ran from a little sandboxed location, and because of the way `suexec` worked it was pretty unlikely for even a very badly-written script
to cause problems, because if the script tried to save out an executable file into the `cgi-bin` directory, it wouldn't be saved out
with execute privileges, so it would just cause an error 500 to occur. After all, `/cgi-bin/picture.jpg` wasn't a program, so why should it run?

### Increased flexibility

But then things started to get a little more complicated. People wanted their main index page to be able to run as a script, without it
forwarding the page to `/cgi-bin/index.pl` or whatever.

So, another compromise happened: the CGI mechanism, which previously was set up to only run the scripts from the `/cgi-bin/` directory, got a
few new rules, such as "if the filename ends in `.cgi` (or other common extensions like `.pl` or `.py`)
run it as a script." It still needed permissions to be set correctly, though,
and by this point `suexec` was generally set up so that there were even more rigorous checks before it would run the script.
And there were so many safety checks in place that this was still *generally* okay.

Around this time it also started becoming common to have access to a database such as mySQL or Postgresql, which allowed more flexibility
and more two-way content. Forums became a thing. So did early blogs. Most of this software started out by having the database just for
storage and the software would simply write out static files, but this started to have scaling problems and the webserver got busy with
the software writing these files out *all the time*, so it became more common for the software to simply read from the database directly
as it ran. This helped somewhat, but it also shifted the load to needing to constantly establish and shut down connections to the database,
because every time the forum program ran it had to connect.

### Hello PHP

... but then PHP happened.

PHP itself was originally intended as another way of adding server-side scripting into HTML files; it was in effect a templating
system for HTML. In the earliest days it was pretty much just treated as another scripting language. The server would be configured to
consider `.php` as another name for `.cgi` or `.pl` or whatever, and the file had to be set up like a proper script; it needed to
start with `#!/usr/local/bin/php` and it needed to be set executable with the correct permissions and so on.

But this was seen as an impediment. So `mod_php` got pretty popular, and it was very similar to `mod_cgi` except it did a few
interesting things. One of the undeniable benefits was that it was now able to maintain the database connection persistently,
rather than having to re-establish a connection every time a script ran. It was also generally a bit nicer for speed because
commonly-used PHP scripts could stay in memory and not have to be re-interpreted every time a page was loaded.

But there are a couple of other implications this led to. The main ones we care about are:

* It embedded the PHP interpreter into the web server itself (rather than running it as an external program)
* Since it was already running as an interpreter, it could always run a .php file regardless of its execution permissions — and so that's what it did

There were a few different variations on this and it didn't always just run PHP from the web server (for example, some of the
better hosts figured out that they could have each user run their own separate per-user FastCGI server that would
run the PHP programs as the separate users, or whatever) but regardless of the setup, you now had PHP always running
and not having to care about the permissions of the file, meaning you now had some persistent process running what was
essentially executable code without the usual safeguards that a shared server would have.

This actually seemed like a good thing at the time, but then many, many pieces of software started allowing arbitrary
people to upload images, and often wouldn't make sure that what was supposedly an image was *actually* an image...

And so that's where we stand today.

This makes sites potentially vulnerable even if they aren't written in PHP themselves; for example, if your HTML
directory permissions are set to be slightly too permissive, and another site on the server gets hacked, that hacked site
can potentially be used to place a `.php` file into your site, and since `mod_php` doesn't check ownership permissions
it now runs on your site with whatever permissions PHP would normally run in your account. (And this isn't just a
theoretical; I've had sites hacked in this way! Now I run a nightly script that ensures that my directory permissions
are correct and tells me about new `.php` files that appeared since the last check, just to be sure.)

So, long story short, one of the biggest problems with PHP isn't with the language itself, but with the way that PHP
gets run; people (or bots) can find ways to upload
arbitrary files with a .php extension and, if that upload is visible to the webserver (which it often will be), then a
request to view that file will execute that file, regardless of its origin.

Or, in short: the sandbox that ensured that a file was meant to be executable was long gone.

### Other PHP features of note

Granted, the erroneously-executable upload feature is only responsible for *some* of the security exploits I've
seen in the wild. I wasn't really intending to get into language-specific issues (after all, I linked to much
better, more-comprehensive articles about it in the introduction), but it's worth mentioning some of them
anyway, as I have seen all of these be used to hack websites I've helped to clean up and secure.

For example, for a very long time, the [`include()` function](http://php.net/manual/en/function.include.php)
would happily support any arbitrary URL and would download and run whatever URL it was given. And it was very easy for a
PHP script to be accidentally written to allow an arbitrary user to provide such an arbitrary URL. (And by "a very long time"
I mean that this was the default configuration until very recently, and many hosts still configure it that way for backwards
compatibility.)

> Some might be looking at the PHP docs I linked to there and thinking, "wait, but it's not running the PHP code locally."
> What the docs mean are that if you do like `include('http://example.com/foo.php');` it's the output of `foo.php` that gets
> included. However, that output could in turn be more PHP code, which would then be executed locally, meaning on your server.
> And PHP doesn't even care what the file extension is; doing an `include()` on `asdf.txt` or `pony.jpg` will happily execute whatever `<?php ?>`
> blocks exist inside of it as well.

There's also a few other features of PHP that lend itself to arbitrary code execution. One particularly *fun* one was the
PCRE `e` flag, which indicated that the result of the regular expression should be executed as arbitrary code; and as PCRE
flags are embedded into the regular expression itself, a carefully-crafted search term (on a less-carefully-crafted search page)
could run arbitrary code. Fortunately, this has been removed in PHP 7; unfortunately, a lot of web hosts still run PHP 5
(or older!) and so this option — which never had a single legitimate usage — is still available on the vast majority of
web servers out there.


### How Flask (and therefore Publ) are different

So, I'm posting this on the Publ blog, which implies that I'm trying to build a favorable comparison for Publ. And that's
a perfectly fine inference to take.

Publ is built on Flask, which uses the [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) (Web Server Gateway Interface),
rather than the CGI, model of execution. This is a bit more complicated
than I want to get into but the short version is that rather than the web server running a program based on the URL,
Publ stays running as a standalone program that the webserver sends commands to as requests come in. So, it's
never asking a file how it should be run, but instead it's telling a single program to handle a request. So, there's
no danger of some random file being executed when it shouldn't be.

"But wait," you might ask, "isn't that exactly what you were complaining about `mod_php` doing?" Well, that's true, `mod_php` works by
always having the PHP interpreter running and able to execute whatever arbitrary code it comes across. However, in the Python
world, simply loading a file won't just outright execute it (unless you've done something really silly); code is kept
separate from data. Loading a URL in Flask isn't mapping to a script file that gets loaded and run, it's calling an established
function that handles content as content.

Another thing that Flask does is it separates out template content from static file content. Static files aren't executable
by default. Templates can
embed arbitrarily-complex code, but there's some language-level safeguards to prevent that code from getting *too* complex,
and templates can only run the functions that are provided to them — there's no direct access to the entire Python standard
library, for example, and so the most dangerous functions aren't included by default. (And Publ does not provide any of
those functions either, at least not purposefully.)

> Note that when I say static files aren't executable by default, there's a huge caveat on Dreamhost; their WSGI
> setup still allows `mod_cgi` and `mod_php` to execute on static content files, and this is likely the case for many
> other shared hosting providers as well. So, you still need to worry about your static content directory being
> secure from third parties.

Publ itself also further separates page content (namely entries and images) from templates and static files. So if a
`.php` file somehow ends up in the content directory, it won't matter at all — Publ just ignores it. It will never
attempt to run code that's embedded in a content file, nor does it even even know *how* to. And Publ doesn't handle
arbitrary user uploads anyway (nor is there any plan to ever support this); anything that would be potentially hazardous
would have been put there by some other means.

If your directory permissions are set wrong, someone can still use someone else's exploited PHP-based site to attack
your account and modify Publ's code.

Publ's design is basically just a fancy way of presenting static files, just like in the early days of the web. It just
serves up the static files dynamically. Or, as I keep on saying, Publ is like a static publishing system, only dynamic.

It would of course be foolish of me to claim that Publ is 100% secure and impossible to hack. And at least on Dreamhost
there's the very real possibility that somehow an arbitrary .php file gets injected into the static files (perhaps by an
incorrect directory permission or whatever), which isn't a flaw in Publ itself but the end result (a hacked site) is the
same. So far as I can tell there's no way to entirely disable PHP on a Dreamhost-based Publ instance, and it's really the
ability to run PHP that makes PHP so dangerous in this world.

So, I'm not going to claim that Publ is 100% secure or unhackable. But it sure has one heck of a head start.