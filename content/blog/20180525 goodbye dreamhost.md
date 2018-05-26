Title: So much for Dreamhost
Date: 2018-05-25 21:42:32-07:00
Entry-ID: 358
UUID: 1c5aad01-e4f5-4c6c-8322-941734f47fe6

One of the overarching reasons I decided to build Publ the way I did was in order to take advantage of Dreamhost's support for Passenger WSGI. I was expecting that to be the primary means of hosting my main site (which is way too big for a Heroku instance) and given how smoothly things were working with this site on Dreamhost I figured it wouldn't be a big deal.

However, there was a *huge* monkey wrench thrown into things when I switched my site's configuration over to Passenger; despite all of my configuration being exactly the same between publ.beesbuzz.biz and beesbuzz.biz, the rendition cache on beesbuzz.biz was getting its permissions set wrong, and there was some rather weird behavior with how it was making the temporary files to begin with.

In investigating this I attempted to upgrade my packages on publ.beesbuzz.biz, and all h\*ck broke loose.

.....

Basically, Dreamhost, being shared hosting, is in the business of overselling capacity. They used to do a very good job of managing their capacity. But then things like WordPress happened, and more sites got bigger and more complex and started taking way more memory, and for whatever reason Dreamhost decided that they would shift towards *only* supporting sites built in WordPress (or basic static hosting), and then they started getting increasingly more aggressive about their "procwatch" process-killer, and somewhere along the line it reached a tipping point where now you can't even run `pipenv install` without tripping their process monitoring.

I must have just been at the knife's edge of that with publ.beesbuzz.biz, because spinning up a second Publ app was too much for it to handle.

So, for now, I've rolled beesbuzz.biz back to my old MovableType-based site, I have made the Heroku instance of publ.beesbuzz.biz the official one (if you are reading this then great, DNS has propagated!), and I am going to look into deploying Publ on my [LiNode](https://www.linode.com/?r=3387618616c77ee52a3a617c0218697a9c36bc9b) VPS, which it turns out has *way* more capacity than I'm using (thanks to them having given me incremental upgrades over the 6.5 years I've been with them) and which should be just fine for this purpose.

In the long run I'm going to move my stuff away from Dreamhost, because beesbuzz.biz was my last major site running there and at this point I'm basically paying $7/month for mediocre DNS service.

So, while setting things up on [LiNode](https://www.linode.com/?r=3387618616c77ee52a3a617c0218697a9c36bc9b) is going to be more difficult, that is what I'll be going with for now (mostly because my LiNode plan just renewed like a month ago so I have two more years prepaid anyway).

In the longer term I'm going to look at other webhosts; [WebFaction](https://www.webfaction.com) looks pretty good, for example, and they come highly-recommended in the Python developer community. And their pricing is quite competitive!

Anyway, getting Flask running on gunicorn with an Apache reverse proxy was fairly straightforward. It's not the simplest thing to get going but at least I have a [working site](http://beesbuzz.biz) (modulo DNS caching, anyway). Hopefully I can get my SSL sorted out soon too.
