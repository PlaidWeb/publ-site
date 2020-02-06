Title: Setting up caching
Sort-title: 400 caching
Entry-ID: 20
UUID: a76ad2de-07c7-53d3-84a0-70835dc90087
Date: 2020-02-05 23:44:04-08:00

Some pointers for setting up the page caching mechanism

.....

When templates start to get particularly complex, Publ can start to slow down; this is one of the tradeoffs when using a dynamic site generator, rather than a static one. Fortunately, it is fairly straightforward to configure Publ with caching; here are some pointers on how.

## Basics

Entire textbooks can (and have been) written on caching and their optimum usage. This is not intended to be an entire textbook, but rather a set of brief-ish guidelines for how to configure Publ's caching mechanism.

### What is a cache?

At its most basic and general, a cache is a temporary storage area where intermediate results get stored for a while.

Fundamentally, there are two algorithms involved in a cache: key generation, and result generation.

The key is basically a filename that tells the cache where to look for a result, and this is computed based on the unique aspects that are involved in generating the result. In the case of Publ's page cache, the key is based on what's being looked at (the selected category, template, entry, and URL parameters), how it's being looked at (the URL), and who's looking at it (the current user, if any).

The result is the result of performing the operation that's being cached. In this case, this is the rendered content of the template.

The goal in any cache is to correctly produce the right result while reusing those results as much as possible, while taking less time on average than what it would take to simply compute the result each time.

### Performance tradeoffs

When setting up a cache, you need to consider what the right balance is between memory usage, performance, and immediacy. These three things are at odds with one another and there is fundamentally no perfect solution that maximizes all three.

Generally-speaking there are two statistics we are looking for in trying to optimize a cache:

* **Hit rate**: How often a page render can be reused; we want this to be as high as possible
* **Staleness**: How out-of-date a page render can be; we want this to be as low as tolerable

There is a third statistic which also matters, namely the active cache size (also called the "hot size," among other things) -- this is simply the total amount of storage used by page renders.

To achieve these goals, there are two "knobs" of particular interest: maximum cache size, and expiration time.

Increasing the expiration time will increase the hit rate, while also increasing the staleness. To understand why, if a page is only accessed once every 15 minutes, and the expiration time is only 5 minutes, then the cached result will be expired before the page is accessed again, making the cache useless. But, if the expiration time is one hour, then if a page changes at all, the update won't appear until an hour after it was rendered.

The other knob, maximum cache size, is simply a measure of how much can be kept in the cache. As long as the expiration time is finite, the cache will never grow to be infinitely large, but you might still want to put a limit on how large it can grow. Raising the cache size won't necessarily increase the hit rate, but decreasing the cache size to be less than the active cache size will decrease it.[^size decrease]

[^size decrease]: The amount by which it does decrease the hit rate does depend a lot; different cache expiry algorithms will have different effects. For example, an LRU (least-recently-used) algorithm will preferentially keep things that have been used more recently, whereas other algorithms such as FIFO (first-in first-out) or random removal will have different effects. These algorithms in turn each have different tradeoffs and discussing those tradeoffs is way outside of the scope of this article.

### <span id="expiration">A note on staleness</span>

To mitigate the staleness problem, Publ uses aspects of when content was last edited as part of its caching mechanism, so if content changes that might affect a page, all previous versions of that page will be discarded.[^staleness mitigation] So, while many caching systems recommend only setting the expiration time to the maximum amount of time you can tolerate a change not being available, Publ does not have this issue.

[^staleness mitigation]: At present (as of v0.5.14), Publ just uses the last update time of any piece of content as a global freshness indicator; if any piece of content changes, it effectively discards the entire cache. In the future, Publ may also keep track of which specific pieces of content went into a rendition and only discard pages which include those specific content elements.

However, some things that Publ can do will still become stale. For example, things that are essentially non-deterministic (such as things based on random numbers) or based on the current time (such as `entry.date.humanize()`) will still be subject to becoming stale. So if you use any of these things in your templates, you'll want to set your expiration time accordingly. Some guidelines:

* If you use `entry.date.humanize()`, an expiration time of around 1 hour is probably fine (although this will make a recent entry's relative time appear to be wrong for its first hour of existence or so)
* If you use random number generation for whatever reason (such as displaying a random image on a particular page), the expiration time should be for however long you are willing to tolerate the number staying the same
* If you want to display the current time on the page for some reason[^some reason], the expiration time should be for the most "slow" you're willing to have the clock be.

[^some reason]: I personally have no idea why you'd want to do this; `entry.last_modified` is more appropriate for any use case I can think of.

Also, if you plan on using any sort of monitoring service (munin, Pingdom, etc.) to measure page load time over time (to get an ongoing performance indicator), it's a good idea to set your expiration time to a nearby prime number; for example, if you want your expiration time to be around an hour, try values of 3593 or 3659 or the like. This helps to prevent sampling bias and gives a much better overall average.

## Configuration

Publ uses [flask-caching](https://flask-caching.readthedocs.io/en/latest/) for its caching layer. The short version of its documentation is it provides caching backends for a number of common caching servers (Redis and a few variants of MemcacheD), as well as file-based and in-process caching.

If you have Redis or MemcacheD available, definitely use those; they have the advantage of persisting beyond your application's run time, and going into a common shared memory pool for all sites that use them, which can be way more memory-efficient than the in-process cache. They also both support distributed caches.

If you are self-hosting and trying to decide which cache server to go with, I suggest MemcacheD, as it's by far the easiest to install and configure, and most distributions pre-configure it with sensible defaults.

If you don't have any of those (for example, you're on shared hosting that doesn't allow you to run your own services), your best choices[^uwsgi] are `FileSystemCache` (file-based) and `SimpleCache` (in-process), which each have strengths and weaknesses. Both of them suffer from not being configurable based on actual storage size; they can only track the number of items in the hot cache. `SimpleCache` is faster, but also makes your process take more memory -- a big concern if you're on a shared system where memory usage is limited. `FileSystemCache` is generally friendlier and fast *enough* (and also will take advantage of the operating system's file cache which makes it kinda-sorta similar to using a caching server), but its performance disadvantage can end up slowing the site down in many cases. But if you can look at the state of the filesystem, `FileSystemCache` gives you better visibility into what's happening with the cache, which can give you better ideas for how to tune it.

[^uwsgi]: If you're hosting on uWSGI, that also provides a caching mechanism, but as far as I can tell it is largely equivalent to `SimpleCache`. However, depending on your hosting provider they may be able to configure something useful for you anyway, although they're much more likely to provide MemcacheD or Redis which are vastly preferable.

In general, I'd recommend this priority order:

1. MemcacheD or Redis
2. FileSystemCache (if you have lots of storage available)
3. SimpleCache (if you have lots of RAM available)

Regardless of caching backend, in your application's [cache configuration](865#cache) you should configure the following:

* `CACHE_KEY_PREFIX`: Set this to some random but fixed string (this helps to prevent certain kinds of attacks that are possible if you share the cache with someone else)
* `CACHE_DEFAULT_TIMEOUT`: Set this to your expiration time, as discussed [above](#expiration)

Some backend-specific notes are below.

### MemcacheD

In order to use MemcacheD you'll also need to add a MemcacheD client to your Python environment. I generally use `python-memcached` as it's easier to install (especially in cross-platform scenarios), but `libmc` and `pylibmc` both have some advantages in performance-critical and large-scale scenarios, being slightly faster as well as supporting [consistent hashing](https://en.wikipedia.org/wiki/Consistent_hashing).

If you're on Google AppEngine, a suitable client is already provided to you and there is no reason to add your own.

### SimpleCache

Set the value of `CACHE_THRESHOLD` to limit the number of items that can be kept in the cache. As noted above, there is no way to limit the size directly, so if you have a specific allocation limit in mind, try to figure out what the average size of a page is (in bytes), and divide your allocation limit by that. That is the value you should use.

### FileSystemCache

Similarly to SimpleCache, this uses `CACHE_THRESHOLD` to limit the number of items in the cache, rather than the total storage size. Since filesystem space is usually much more plentiful than RAM, there's no reason to be particularly miserly with this. Unless you start to run out of storage space, anyway

You should also make sure that the `CACHE_DIR` is set to a directory that you have write access to, and you should set `CACHE_OPTIONS` to `{'mode': 0o600}` (the default).
