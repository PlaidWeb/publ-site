Title: Why Publ won't support magic auth links
Tag: auth
Tag: design
Tag: WebSub
Tag: indieweb
Syndication: https://news.indieweb.org/en
Date: 2019-10-25 17:36:11-07:00
Entry-ID: 1266
UUID: 6695ff51-4390-5f69-affd-544a44f80f8a

Since adding user authentication to Publ, I've been thinking of ways of allowing people to subscribe to sites from feed readers while getting their own native authorization, so that people can see entries directly in their readers rather than needing the clumsy mechanisms of unauthorized placeholder entries.

Out of the box, Publ authentication does support a shared cookie jar; if you can provide your cookies to your feed reader in some way, then things will Just Work. Unfortunately, I don't know of any feed readers that actually support this, at least not easily. (Back when most browsers had a feed reader built-in this was a lot simpler. But time marches on.)

The two mechanisms which seemed most promising are [AutoAuth](https://indieweb.org/AutoAuth) and "magic links," where users get signed URLs that come pre-authenticated and show the full authorized content for that user. AutoAuth is still in a draft phase that's stuck in a chicken-and-egg situation (and also requires a lot of buy-in to IndieWeb protocols, which is still a pill too large to swallow for most of the folks who follow my blog), so magic feed links seemed like the best path forward.

I even got so far as to [draft out an implementation](https://github.com/PlaidWeb/Publ/issues/282), but there's a few bad issues with it which just made me opt not to.

.....

## Feed discovery

Right now, when people want to subscribe to a feed, they usually point their feed reader at the URL for the website, and then let the reader software discover the feed. Usually there will be a `<link>` tag that provides the feed URL, like:

```html
    <link rel="alternate" type="application/atom+xml" title="Atom feed" href="feed" />
```

Sometimes there may be more than one of these `<link>` tags for different styles of feed; for example, it might have both RSS and Atom versions, or there might be a choice between full-content and summary, or a comments feed, or so on. Some feed readers will show a list and allow the user to select which feed to use, while others will simply use the first one on the list.

In the case of a magic link, however, these links are only provided to the person who is logged in. An external feed reader won't be logged in, and therefore won't see the magic link.

So, an alternate discovery mechanism must be provided; usually this will take the form of a widget in the corner of the page where clicking on it will expand a text box you can select the (possibly really long) feed link from and then paste *that* into your feed reader. There is no standard approach to doing this, and is confusing and weird.

## Item sharing

The bigger problem, however, and the reason I decided to abandon the project entirely, is that the way that Atom specifies item sharing makes this incredibly dangerous.

Atom provides a way of sharing items; [Feed on Feeds](https://github.com/fluffy-critter/Feed-on-Feeds) implements this, for example. If you share an item, its Atom entry looks like this:

```xml
<entry>
<id>urn:uuid:dacd7607-380e-526d-b688-60d8d334bde7</id>
<link href="https://beesbuzz.biz/comics/journal/3675-ADDitive" rel="alternate" type="text/html"/>
<title type="html">Journal: ADDitive</title>
<summary type="html">
<!-- actual item content goes here -->
</summary>
<updated>2019-10-15T23:14:52Z</updated>
<source>
  <id>https://beesbuzz.biz/</id>
  <link href="https://beesbuzz.biz/" rel="alternate" type="text/html"/>
  <link href="https://beesbuzz.biz/feed" rel="self" type="application/atom+xml"/>
  <title>busybee</title>
</source>
</entry>
```

That `<source>` block is what to look at; namely, the `rel="self"`. It provides a link back to the original feed. This means that if someone were to share an item from an authenticated feed -- regardless of the privacy of the item itself -- it would also share the authenticated feed URL. This can be *very, very bad.*

## So what are the alternatives?

As stated in the preamble, the two major alternatives are shared cookies, and AutoAuth. Neither is a perfect solution.

Shared cookies are great if you can synchronize your session cookies between your browser and your feed reader. (This is especially feasible if your feed reader is hosted in your browser.) Most feed readers don't work that way. So, you could export your cookies to be used by the feed reader (which hopefully uses the presence of a cookie to avoid deduping subscriptions! I'm pretty sure Feed On Feeds doesn't!), but if cookies have an expiration date on them (which Publ cookies absolutely do) this means having to re-export periodically.

Some sort of feed metadata indicating that there is a login/auth mechanism available might be workable; something like `<link rel="authenticate">` which prompts the browser to pop up some sort of proxy popup so that it can intercept the login cookie, for example. This might be a nice middle ground to AutoAuth without requiring every user to buy in fully to the IndieWeb experience.

(And, of course, supporting AutoAuth would be ideal for those who *do*.)

I think having some sort of "hey, please log in" metadata in the feed is also helpful if only because it gives a cue to a subscriber that there's something to authenticate against in the first place. But this purpose is already served by having empty "private post" stub entries...

## Other things to consider

While I'm ramble-thinking about this stuff, I'd also like to see a better mechanism for dealing with authentication around [WebSub](https://indieweb.org/WebSub). As far as I've seen, there are three kinds of WebSub push:

1. Full-feed "fat ping" (i.e. the push notification contains the entire feed content)
2. Update-only "fat ping" (i.e. it only contains the new/changed items)
3. Notification-only "thin ping" (it only sends a notification of the update and then the recipient needs to do a pull of the content, once notified)

The WebSub model doesn't really have any provisions for determining authentication/authorization status, as there's no mechanism for associating authentication stuff with the subscription topic. In case 3 it doesn't really matter -- the client will just provide its normal content-pull credentials -- but in cases 1 and 2 it matters quite a lot, as the content needs to be pre-filtered through the authentication layer.

For what it's worth, on all of my sites I use [SuperFeedr](http://superfeedr.com/) as my WebSub hub, which does case 2 (actually a particularly annoying version of it where it only pushes *new* items, rather than including changed items). It definitely doesn't provide the extensibility required for authenticated WebSub, and I doubt that this is anything they ever would add even if a standard were to be adopted. So, I think for the non-thin push case, it would become necessary to have a different hub. [Switchboard](https://switchboard.p3k.io/) appears to do a full-content push (case 1 above) and doesn't currently support AutoAuth; however, given the author, I would expect it to add that functionality when it becomes more commonplace.

In the meantime, I think I'll continue on with my unauthorized stub entries; they're annoying to unauthorized users and they leak the fact I'm posting private entries to the world, but at least they prompt people to sign in and notify folks that there might be something for them to read. And for better or worse it also works with my [POSSE](https://indieweb.org/POSSE) setup.

## Conclusion

Software is hard.
