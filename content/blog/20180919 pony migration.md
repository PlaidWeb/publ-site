Title: Goodbye peewee, hello PonyORM
Date: 2018-09-19 02:27:21-07:00
Entry-ID: 1080
UUID: 26ccac61-8792-54c6-8681-eb173adee58c

For a number of reasons, I have replaced the backing ORM. Previously I was using peewee, but now I'm using [PonyORM](http://ponyorm.com). The reason for this is purely ideological; I do not want to use software which is maintained by someone with a track record of toxic behavior.  peewee's maintainer responds to issues and feature requests with shouting and dismissive snark; PonyORM's maintainer responds with helpfulness and grace. I am a [strong proponent of the latter](//beesbuzz.biz/7502).

PonyORM's API is also significantly more Pythonic, and rather than abusing operator overloads for clever query building purposes, it abuses Python's AST functionality to parse *actual Python expressions* into SQL queries. Seriously, [look at this explanation of it](https://stackoverflow.com/questions/16115713/how-pony-orm-does-its-tricks) and tell me that isn't just *amazing*.

.....

There are a few downsides to Pony so far, though:

* While it's possible to adapt arbitrary types into database fields, queries don't actually work on them (so at least for Enums I have to convert at query time, which turns out to not be a huge deal)

* There's no simple way to incrementally build a query with an OR branch in it (which I don't actually use anywhere at present but I did have to rework some query API stuff to do that)

* Not really a downside but Pony treats `''` and `NULL` as equivalent, which has some fun implications for storing empty strings in a table

    Of course, SQLite does this too, internally, and my existing code for that case wasn't actually "correct" (but it happened to work with SQLite anyway). So moving to Pony meant I had to make this *actually correct* which, on the plus side, means that Publ is more likely to work with MySQL or Postgres (which I haven't tested yet)

In addition to PonyORM I evaluated a few other options; my other front-runner was to simply store all of the data in in-memory tables and using `sorted([e for e in model.Entry where e.foo > bar])` or whatever. Which was a gigantic pain to think about. Granted, a lot of what made it painful is stuff I had to do in order to support Pony as well (namely the switch from a query-building syntax to incremental list comprehensions), but the Pony approach happens to also be way more efficient since it can use indexes and also does all the filtering at once and so on.

Anyway, I'm rambling here. How about we look at some quick benchmarks to see if this hurts performance! All these timings are based on building [beesbuzz.biz](http://beesbuzz.biz), which is getting to be a reasonably-large site at this point. These timings are based on simply running it locally on my desktop.

For the index scan I ran a simple Python script that looks like:

```python
from main import app
from publ import model
model.scan_index()
```

which just sets up the configuration as appropriate and scans the index directly and exists. For the spidering I ran it under gunicorn with `gunicorn main:app` and used the command:

    time wget --spider -r http://localhost:8000 -X /static,/comics

To keep things as fair as I could I spidered the entire site once without checking the time (so that the image cache would be pre-populated, to eliminate its I/O overhead as a variable).

### peewee

Initial index scan:

```terminal-session
$ time pipenv run python ./timing-test.py

real    0m33.809s
user    0m10.916s
sys 0m4.004s
```

Time to spider entire website:

```
Total wall clock time: 20s
Downloaded: 421 files, 4.4M in 1.1s (4.12 MB/s)

real    0m20.514s
user    0m0.285s
sys 0m0.435s
```

Memory usage after spidering: around 78.6MB according to macOS Activity Monitor

### PonyORM

Initial index scan:

```
real    0m13.897s
user    0m4.562s
sys 0m2.864s
```

Website spider time:

```
Total wall clock time: 20s
Downloaded: 421 files, 4.4M in 1.3s (3.39 MB/s)

real    0m20.041s
user    0m0.335s
sys 0m0.444s
```

Memory usage after spidering: 72.6MB

### Conclusions

PonyORM takes a little less RAM and it has faster writes. Its queries are also marginally faster. But not enough to make a meaningful difference.

Anyway, I'm mostly just happy that this doesn't significantly *hurt* performance. The fact that it improves the end product while supporting positive influences in the F/OSS community is a bonus!

Anyway, the deployed site is still running Publ v0.2.3, but the first Pony-based release will come soon as v0.3.0.
