Title: Now with ∞% more OpenGraph support
UUID: b3cb957c-70f0-4184-80e0-d67d8fff964d
Date: 2018-05-10 19:06:04-07:00
Entry-ID: 138

I have now implemented the basic [OpenGraph API](http://ogp.me) to Publ, so now a template can generate an OpenGraph card with `entry.card`.
So in theory when this entry gets autoposted to Twitter, this first paragraph should appear, as should the below image:

![{gallery_id=None}](/tests/rawr.jpg)

Anyway that's what's new in v0.1.11 (as well as a bunch of internal refactoring to support this addition).
