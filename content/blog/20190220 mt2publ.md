Title: An early-alpha Movable Type importer
Date: 2019-02-20 15:42:18-08:00
Entry-ID: 999
UUID: 11c6297c-2dc9-54f6-a781-ec43d0ed1d00
Tag: tools
Tag: import
Tag: mt2publ

For those folks who want to import their content from Movable Type over to Publ, I've finally gotten around to writing an [importer](https://github.com/PlaidWeb/mt2publ). Currently it only attempts to convert entry content and category metadata, and only using SQLite-formatted database dumps.

See its `README.md` for the (incredibly rough) usage instructions.

Eventually I want to try to automatically convert templates from MT's scripting language to Jinja-Publ templates, although there's a bunch of stuff that's going to be difficult to port across and a lot of stuff is just plain not feasible to even try, so don't expect that to become a major thing any time soon.