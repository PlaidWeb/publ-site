Title: Use with Cloudflare or other caching CDNs
Date: 2025-05-15 22:38:02-07:00
Entry-ID: 675
UUID: b5261c4b-0e8b-517e-b4ed-8c7f5bb4f59b

Using Publ with [Cloudflare](https://cloudflare.com/) is fairly straightforward, but there are a few things you should keep in mind.

.....

Because of the rise in badly-behaved website scraping bots, it can be very helpful for site performance to have a fronting CDN, such as [Cloudflare](https://cloudflare.com/), in front of your origin server. But there are a few things you need to keep in mind.

### Caching

When configuring caching, it is very important that you exclude the following paths from any aggressive caching behavior:

* `/_cb/`
* `/_login` and `/_login/`
* `/_logout` and `/_logout/`

If these paths get cached, it may lead to unpredictable behavior for user login and logout.

### Image CDN

There should be no need for any additional fronting image CDN on Publ, although having it enabled shouldn't hurt. However, because Publ manages its own cache lifetime and the CDN is not aware of this, some strange behaviors may occur in extreme edge cases.

Setting the CDN to aggressively prefetch images or to use status 103 "Early Hints," if possible, is probably a good idea.

