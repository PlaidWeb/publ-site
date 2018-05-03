Title: Well, that was embarrassing...
Date: 2018-05-02 22:56:59-07:00
Entry-ID: 216
UUID: 55415435-a738-488b-b407-d140bb040c2c

So, note to self: library version pinning is a good idea. I should also learn how to properly manage my version dependencies.

Thanks to @therealtakeshi for [bringing this to my attention](https://twitter.com/therealtakeshi/status/991908218686377984)!

.....

The short version of what brought this site down was that, as far as I can tell, Flask-Cache pushed out an
update that finally removed a deprecated namespace. Unfortunately, that namespace was still in use by Flask-Cache itself.
So, presumably this means that any Flask app that's using an unpinned version of Flask-Cache is going to break as
soon as they update their dependencies. Oops.

Word on the street is that Flask-Cache is basically abandoned anyway so for now I've switched to flask_caching, which
is being actively maintained.