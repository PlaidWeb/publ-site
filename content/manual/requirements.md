Title: Runtime requirements
Date: 2019-12-31 15:07:29-08:00
Entry-ID: 46
UUID: 9a00a7df-d9c4-5ff0-98b5-99904c0c6c4d
Sort-Title: 000Requirements
Status: HIDDEN

What you need in order to run Publ

.....

Publ requires the following to work:

* [Python](https://python.org/) 3.5 or later
* The ability to run a Python application on your web hosting provider (if you can run Django or Flask, you can run Publ!)
* That's it!

It also benefits from the following:

* A persisting file system (i.e. not EC2/Heroku/Google AppEngine/etc.)
* Some sort of Python package manager (`pipenv` recommended)
* A caching provider that's supported by [Flask-Caching](https://pythonhosted.org/Flask-Caching/), such as MemcacheD or Redis
