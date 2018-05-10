Title: Even more updates, v0.1.10 released
UUID: 1a697a3a-8156-402f-a2f1-cf34f8719f29
Date: 2018-05-09 23:29:01-07:00
Entry-ID: 4

If you are reading this, it means that Publ v0.1.10 is out. This release is mostly about a few cleanups, such as:

* No longer nests a `<div>` for an image gallery inside of a containing `<p>` (which both fixes an HTML validation error and makes styling more controllable)
* Cleans up error handling somewhat
* Also cleans up a bunch of code for property caching

But there's also a new feature, namely `view.range`, which you can read about [over in the API docs](/api/view).

I am also making significant progress in porting [my main website](http://beesbuzz.biz/) over to Publ and hopefully I'll
have something to show for it soon. (And I promise it looks way nicer than this site!)
