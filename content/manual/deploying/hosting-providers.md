Title: Hosting options
Date: 2019-10-12 11:01:01-07:00
Entry-ID: 545
Sort-Title: 100
UUID: 8d9bf039-ad27-5772-a5fc-aaf9b869c19c

Here's some options when it comes to hosting Publ sites, with pluses and minuses.

.....

If you know of something that isn't listed, please [open an issue](/newissue). Note that a listing is not necessarily an endorsement.

## Self-hosting

If you're savvy with running a Linux server, this is a pretty good choice. The advantages are having complete control over your hosting setup and generally having the cheapest storage available, and a lower overall cost per site, if you run multiple sites. The main disadvantage is having to be your own sysadmin.

### VPS providers

A virtual private server gives you complete control over a virtual slice of hardware. Typically this provides better fault tolerance, easier migration, and simpler server management, with the downside of being slightly lower in performnace (in ways which don't matter for hosting websites most of the time).

Some known providers:

* [LiNode](https://www.linode.com/?r=3387618616c77ee52a3a617c0218697a9c36bc9b)
* [Digital Ocean](https://www.digitalocean.com/)
* [Amazon EC2](https://aws.amazon.com)

### Physical hosting

Colocation, either with managed hardware or with bring-your-own device. Not for the faint of heart. Generally gives you more performance but worse bang for your buck, worse fault-tolerance, and much more of a management headache when things go wrong.

## Cloud app hosting

Cloud app hosting means you provide an image for an application which gets run only when it's actively being used.

The advantages to this is that there's a lot less administrative overhead on your end, and it's usually easier to deploy your site and also handle scaling and so on.

The disadvantages are numerous, however; usually there's a much lower limit on how much content you can host, deployments can be significantly slower, and when the site "sleeps" it can take quite some time for it to "wake up." Also, storage, CPU, and bandwidth tend to be much more expensive than dedicated hosting.

Some known providers:

* [Heroku](https://heroku.com/)
* [Google App Engine](https://console.cloud.google.com/appengine)

## Shared hosting

Typically this gives you the advantages of self-hosting (cheap storage and bandwidth) and cloud app hosting (managed hosting, no self-administration), with the disadvantages of having to share capacity with other users and not necessarily having the ability to choose your actual service stack.

Most shared hosting providers don't allow running Python apps, but all of the following do:

* [Nearly Free Speech](https://nearlyfreespeech.net/)
* [WebFaction](https://webfaction.com/)
* [Dreamhost](https://dreamhost.com/) (note that I have had [specific issues with them](358) but YMMV)

Note that "supporting Python" doesn't necessarily mean supporting Python *apps*, as sometimes it just means being able to run Python CGI (which is a different, older mechanism). If a provider says they can host WSGI or Django and that they support Python 3, they can definitely host Publ.
