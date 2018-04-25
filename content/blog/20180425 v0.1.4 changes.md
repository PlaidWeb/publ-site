Title: More API changes, version 0.1.4 released
Date: 2018-04-25 16:12:27-07:00
Entry-ID: 302
UUID: 9ed2a45c-d791-4195-bdf4-3f04de663728

I've released version 0.1.4 of Publ, which makes the following major changes:

* `limit` has been changed to `count` in the API (for more consistency and clarity)
* Similarly, on image sets, `limit` is now `count` and `limit_offset` is now `count_offset`
* More template functions now support positional (rather than keyword) parameters; this has yet to be documented however

And on this site I've split out the manual to put the various template object
APIs into [their own category](/manual/api), although the organization of the
documentation is still h\*ckin' messy.

