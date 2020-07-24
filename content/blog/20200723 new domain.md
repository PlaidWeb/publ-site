Title: New domain!
Tag: meta
Date: 2020-07-23 15:58:27-07:00
Entry-ID: 639
UUID: 2fcbecfd-d526-5b4b-95a9-c3e589f908f7

Since there's now a lot more to [PlaidWeb](https://github.com/PlaidWeb/) than just Publ, there is now a new [organization website](https://plaidweb.site/) which will become the top-level home of these different things, which allows for better organization of this stuff to begin with.

While I'm still trying to work out how I'm going to organize things, my expectations are as follows:

* The Publ documentation and demo site will live at [publ.plaidweb.site](https://publ.plaidweb.site/)
* This dev/release blog will move to the main domain at some point
* Elements which don't have their own website will get a microsite on the main domain
* Every incoming webmention that the old domain received will remain missing/broken in perpetuity (or at least until I get around to adding native webmentions to Publ)

Also, [publ.beesbuzz.biz](https://publ.beesbuzz.biz/) is *intended* to redirect over here, but it's disappeared from my DNS host for some reason; it was actually this happening which inspired me to finally take this action. ~~It seems to be a bug with how LiNode's wildcard domains work, and I have an active support ticket open.~~ ==Update:== Turns out this was a subtle issue with how DNS wildcards work, which is explained below the cut.

.....

> Hi there,
>
> Thank you for taking those steps to aid in troubleshooting and your patience so far in tracking this down.
>
> The reason the publ.beesbuzz.biz does not resolve but also does not come back with an NXDOMAIN status is because wildcard DNS records are always superseded by any record type that is more specific. That is, they will only apply (match) if there isn't already a record in place. In your case, there's currently a TXT record for `_github-challenge-PlaidWeb.publ.beesbuzz.biz` which occupies the space for the publ subdomain and causes this behavior. The wikipedia article on wildcard records has more info on this behavior including citations to the RFCs where this behavior is defined:
>
> [`https://en.wikipedia.org/wiki/Wildcard_DNS_record#Definitions_of_DNS_wildcards`](https://en.wikipedia.org/wiki/Wildcard_DNS_record#Definitions_of_DNS_wildcards)
>
> The easiest solution here would be the one you've already implemented before which just involves setting a specific record for the bare publ subdomain.
>
> I hope this information proves useful to you. If you have any other questions or need help with anything else, always feel free to reach out.
>
> Regards,<br>
> Bo<br>
> Linode Support Team

Thanks, Bo, for your clear and concise explanation of something that's incredibly unintuitive to anyone who isn't intimately familiar with the workings of modern DNS!

(Of course, now that the [GitHub organization](https://github.com/PlaidWeb/) organization has its own domain, the easier fix was to just remove the GitHub validation `TXT` record which is no longer necessary.)
