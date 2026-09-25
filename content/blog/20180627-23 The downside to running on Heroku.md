Title: The downside to running on Heroku
Date: 2018-06-27 20:01:46-07:00
Entry-ID: 23
UUID: 3ccbbeb1-b1f2-4ac1-b9ac-702259c4b69f
Tag: design

So, sorry to anyone who was subscribed to the RSS feed for this and got spammed with v0.1.24 release announcements. I made a mistake and pushed a version of the entry that didn't have a canonical ID assigned yet, and as a result, every time Heroku spun up, it assigned a new ID. This is something that's happened before and I really ought to do something about it.

Three things come to mind:

1. Figuring out how to always make IDs get assigned in an idempotent manner (hard to do correctly)
2. Don't run on Heroku so the assignments persist between executions (easy)
3. Add a pre-push hook to the repo that verifies that all entries alread have an assigned ID (???)

2 seems like the easiest approach for now, so that's what I'll probably do.
