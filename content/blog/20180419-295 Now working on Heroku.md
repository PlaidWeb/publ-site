Title: Now working on Heroku!
Date: 2018-04-19 17:45:24-07:00
Entry-ID: 295
UUID: 819292e1-0a5c-44ab-af2e-2098009a7662

Converting Publ into a pip-installable library ended up making the Heroku deployment
really easy. While [the main site](http://publ.beesbuzz.biz) is running on Dreamhost,
there is an [instance on Heroku as well](http://publ.herokuapp.com), which seems to
be running reliably (although if it gets hammered with activity I assume Heroku will
shut it down until I start actually paying them money).

There's a few pluses and minuses to Heroku compared to traditional
hosting on a persistent server (such as Dreamhost).

.....

### The pluses

Heroku can be set to automatically pull/deploy from GitHub when there's a content
update. So, now when I push changes to this blog, Heroku redeploys it automatically!

You also have a choice of fronting server. I went with [gunicorn](http://gunicorn.org)
since that's what most people seem to recommend with Flask (including Heroku themselves).
And the way I had the local test process setup made it absolutely trivial to use with
gunicorn's default launcher. My procfile is literally just:

```
web: gunicorn app:app
```

This also means that the site can scale way more easily if necessary; if, for some
reason, it gets pelted with a lot of traffic it's pretty easy to tell Heroku to
spin up more instances and load-balance them.

Heroku also has memcached support available, and configuring that to work with
Publ should be pretty trivial.

### The minuses

Every deployment completely wipes the instance and re-pulls everything fresh.

Immediately, this means that unless you configure Publ to use a persistent database (like
MySQL), it has to do a full content index on every restart. Fortunately, content
scans are pretty quick.

Another implication of this is that it changes the way you have to think about making
content. For example, one of my medium-term ideas is to have a cron job that
consumes and republishes content from an external feed (to syndicate content
I post on other sites, like SoundCloud or whatever). In this world, the necessary
approach would be to have a cron job running somewhere that can persist data and
use that to check the new files into github instead, which isn't ideal. Fortunately,
"somewhere" can be a home computer or whatever, but it still is something to
have to think about.

Oh, and my guidance has generally been to add your image rendition cache to
`.gitignore`. But this setup means that Heroku will have to rebuild the rendition
cache every time it spins up. Once a site gets to a certain size, that implies
that the rendition cache will take longer and longer to populate. The alternative
is to pre-warm your rendition cache and check it into your git repo instead and that is
extremely not ideal for quite a few reasons.

Come to think of it, using memcached means that it's quite likely for a cached
page render to persist beyond any cached image renditions it references. So, to that
end, I would not recommend using memcached on Heroku at this time.

### Possible future stuff

It's *possible* (although extremely unlikely) that there may be a way to push content back
up to git from the Heroku instance.

It might also be worth making it possible to store the image rendition cache
into some sort of persistent object store like S3. But that's already getting
far beyond the weeds and goes off into distant tundra, as far as I'm concerned
for the purposes of this project. (But if someone else wants to add that as an
*optional* feature, I wouldn't turn it down!)

There's also a possibility that it would make sense to use some other, distributed
file storage mechanism for storing content. Like an sshfs mount or something.
That continues to not be ideal for ***so many reasons***, though.