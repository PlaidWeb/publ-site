Title: In better news, v0.1.18
Date: 2018-05-26 01:19:29-07:00
Entry-ID: 381
UUID: 22d0906c-4dc7-48cd-9c75-4f9e5a17c765
Tag: release

So aside from the Dreamhost issues, I would like to share what's new in the latest version as part of my big "get my website online" push:

* PERFORMANCE: Improved the threading mechanisms around image renditions for better stability and performance
* BUGFIX: Made markup tagging work consistently between image types
* FEATURE: `view.link()` now allows overriding `category`
* FEATURE: You can now mark an entry with an `Entry-Status` of `DELETED` or `GONE`, which results in a 410 error instead of a 404 (be the envy of your web-developer nerd friends!)
* FEATURE: Error templates will automatically use the x00 error code as a potential fallback (e.g. error code 503 will also fall back to a template for 500)
* FEATURE: Entry titles can now have Markdown in them, and it usually works most of the time!
* BUGFIX: Now when running in debug mode you don't end up with two watchdog threads
* FEATURE/QUALITY: Refactored the way error pages are handled, and now if you get a 404-type error on a page while the index is being asynchronously scanned, it'll turn into a 503 with a `Retry-After` disposition in case it's just something that hasn't been indexed yet
* UX: View pagination URLs now all use `id` as the query parameter rather than a miasma of contextually-dependent `start`, `last`, or `first` which made no sense anyway

