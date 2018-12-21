Title: Embedding webmention.io pings on your site
Date: 2018-12-20 23:14:47-08:00
Entry-ID: 1048
UUID: 66ca748a-4597-5381-a0c9-fcf41f7fb75e

Are you using [webmention.io](https://webmention.io) as your webmention endpoint? Want to get your incoming webmentions displayed on your website?

Well you're in luck, I wrote [a simple-ish script for that](@webmention.js). (You'll probably also want to see [the accompanying stylesheet](@webmentions.css) too.) And it doesn't even require that you use Publ -- it should work with any CMS, static or dynamic. The only requirement is that you use either webmention.io or something that has a similar enough retrieval API.

I wrote more about it on [my blog](https://beesbuzz.biz/blog/3743-More-fun-with-Webmentions), where you can also see it in use. For now, I'm just going to use the [sample site repository](/github-site) to manage it (and issues against it).

It's MIT-licensed, so feel free to use it wherever and however you want and to modify it for your needs. I might improve it down the road but for now it's mostly just a quick itch-scratching hack that does things the way I want it to.
