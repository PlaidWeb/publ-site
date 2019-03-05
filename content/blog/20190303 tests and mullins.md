Title: Tests removed from main site
Date: 2019-03-03 16:29:33-08:00
Entry-ID: 332
UUID: 4b92a66e-cccd-5fc0-a0af-4cc32275ba6b

I finally got [my first contribution to Publ](https://github.com/PlaidWeb/Publ/pull/169), which is really great, but it led to me finally realizing that putting the smoke tests for the software in the main site wasn't so great. So the tests have been moved into the library itself, so they're only really visible to people who are actually working on the code for Publ itself.

Eventually I'll make a "features" section that demonstrates the features of Publ instead, since some of the tests were used (clumsily) for that purpose.

While I'm here, I figured I'd mention that the [day job's website](https://mullinslab.microbiol.washington.edu) is now running on Publ. Woo.
