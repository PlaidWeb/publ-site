Title: Getting closer to usefulness

I finally separated out Publ-the-library from the main Publ website files, and
[released v0.1.0 on PyPI](https://pypi.org/project/Publ/), making this the first
time I've released anything there. Woo!

.....

Anyway, this means that much of [the manual](/manual) is now obsolete, but it
also means that actually making one's own site using Publ is going to hopefully
be much easier. I was originally envisioning what was pretty much a big mess
of git submodules and other such things, and now Publ itself is just an
installable dependency and I can provide [the main website files](http://github.com/fluffy-critter/publ.beesbuzz.biz)
as an example of how to build your own site.

I'll pretty much have to rewrite the manual, and also there's some stuff I need
to learn about properly using `pipenv` when developing an upstream dependency
in tandem with the thing itself, but I'm sure I'll figure it out eventually.
(Plus, [Stack Overflow](http://stackoverflow.com) is pretty good for these kinds of questions.)

Also, as part of all these changes I've done cleanup such that it's feasible to
deploy on Heroku! So that'll be good for performance testing as well as a much
more compelling deployment target for most people.