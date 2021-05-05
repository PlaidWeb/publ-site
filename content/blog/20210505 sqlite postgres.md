Title: SQLite vs. Postgres, at a glance
Tag: performance
Tag: deployment
Tag: SQLite
Date: 2021-05-05 11:28:50-07:00
Entry-ID: 616
UUID: bb6c33bc-50d5-587e-8d94-8820bb28c7e4

There's a general belief that SQLite is a "slow" database and Postgres is "fast," and many software packages (including FOSS) insist that SQLite is only suitable for testing and doesn't scale. However, this doesn't make much sense when you think about it; SQLite is an in-process database so there's no communications overhead between the service and the database, and because it's only designed to be accessed from a single process it can make use of optimistic locking to speed up transactions.

Since I was installing postgres for another purpose on my webserver, I decided to quickly see if Publ performs better on Postgres vs SQLite. To test the performance I compared the timing for [my website](https://beesbuzz.biz/) on both doing a full site reindex, and rendering the Atom feed several times (using the debug Flask server and caching disabled).

.....

Times are in seconds:

| Database | Index | Atom feed |
|----------|-------|-----------|
| SQLite   | 23.267 | 0.799 |
| Postgres 12 | 26.132 | 1.270 |

So, SQLite is, as I had assumed, substantially faster than Postgres, and also has much lower administrative overhead. Thus, I will continue to recommend that as the database of choice for traditionally-hosted deployments.

My belief is that, in general, if you're building something where there's only a single process connecting to the database (i.e. you don't have a cluster talking to a single database instance), SQLite will perform better than Postgres. The reason to use Postgres is so that you can scale to multiple processes or servers talking to a single centralized data store. If you can build your system such that each database connection can be isolated to a single database instance, SQLite is going to perform much better.

There are other considerations, of course, but if performance is your primary concern, SQLite isn't a bad way to go.
