Title: Hosting options
Date: 2019-10-12 11:01:01-07:00
Entry-ID: 545
Sort-Title: 100
UUID: 8d9bf039-ad27-5772-a5fc-aaf9b869c19c

Here's some options when it comes to hosting Publ sites, with pluses and minuses.

.....

If you know of something that isn't listed, please [open an issue](/newissue). Note that a listing for a specific provider is not necessarily an endorsement.

## Shared hosting

If you can find a compatible shared hosting setup, this is by far the easiest and least-costly way to get running.

Shared hosting providers typically offer very inexpensive bandwidth and storage, with a tradeoff of not having as much flexibility with your environment and service stack. In addition, you'll be sharing resources with other users, which can have both performance and security implications.

Additionally, shared hosting providers typically limit you to PHP and/or CGI. However, there are a few known shared hosting providers which do support Flask (and therefore Publ) to some extent:

* [Nearly Free Speech](https://nearlyfreespeech.net/) claims [direct support for Flask](https://www.nearlyfreespeech.net/about/faq#WorkingApps)
* ~~[Dreamhost](https://dreamhost.com/) ostensibly supports Flask via their [Passenger WSGI wrapper](https://help.dreamhost.com/hc/en-us/articles/215769548-Passenger-and-Python-WSGI) (although I've had [issues with them in the past](358))~~ This is no longer the case.

When considering a shared hosting provider, look specifically to see if they support Flask, or a bit more broadly, WSGI. If they support Django (which is another common WSGI-based framework) it is very likely to support Flask.

However, "supporting Python" doesn't necessarily mean supporting Python WSGI, as sometimes it just means being able to run Python CGI (which is a different, older mechanism which is unsuitable for a modern web stack). If in doubt, ask their support folks if they support Flask.

Once you do find a host, refer to their guides for setting up Flask or WSGI applications to get started with running Publ.

## Self-hosting

If you're savvy with running a Linux server, this is a pretty good choice. The advantages are having complete control over your hosting setup and generally having the cheapest storage available, and a lower overall cost per site if you run multiple sites. The main disadvantage is having to be your own sysadmin, which can be a pretty big burden.

On all of these choices, you'd be running a fronting web server (usually nginx or Apache) and doing a reverse proxy to your Flask application; see the [self-hosting guide](1278) for more detailed information.

### VPS providers

A virtual private server gives you complete control over a virtual slice of hardware. Typically this provides better fault tolerance, easier migration, and simpler server management, with the downside of being slightly lower in performance (in ways which don't matter for hosting websites most of the time).

Some known providers:

* [Linode](https://www.linode.com/?r=3387618616c77ee52a3a617c0218697a9c36bc9b)
* [Digital Ocean](https://www.digitalocean.com/)
* [Amazon EC2](https://aws.amazon.com)

### Physical hosting

Colocation, either with managed hardware or with bring-your-own device. Not for the faint of heart. Generally gives you more performance but worse bang for your buck, worse fault-tolerance, and much more of a management headache when things go wrong.

For some people this can even mean running a server on your home Internet connection. Many ISPs do not take kindly to this; check your terms of service before doing this.

## Cloud app hosting

Cloud app hosting means you provide an image for an application which gets run only when it's actively being used.

The advantages are that there's a lot less administrative overhead on your end, and it's usually easier to deploy your site and also handle scaling and so on.

The disadvantages are numerous, however; usually there's a much lower limit on how much content you can host within the container (and Publ is not designed to use content kept in an external object store), deployments can be significantly slower, and when the site "sleeps" it can take quite some time for it to serve the first page while it wakes up. Also, storage, CPU, and bandwidth tend to be much more expensive than dedicated hosting.

Some known providers:

* [Heroku](https://heroku.com/)
* [Google App Engine](https://console.cloud.google.com/appengine)

