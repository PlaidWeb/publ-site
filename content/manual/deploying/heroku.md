Title: Heroku
Date: 2018-10-13 14:23:23-07:00
Entry-ID: 1210
UUID: 5744383f-5712-5011-9a9d-1b3c9806e090
Path-Alias: /heroku
Sort-Title: 300 Heroku

How to deploy a Publ website using [Heroku](http://heroku.com)

.....

Heroku is probably the easiest environment to configure for Publ, especially for
smaller websites. However, it is primarily intended for experimenting with Publ. Heroku comes with a number of limitations:

* Your git deployment size must be [under 1 GB](https://devcenter.heroku.com/articles/limits#git-repos)
* Your slug size must be [under the 500MB Heroku limit](https://devcenter.heroku.com/articles/limits#slug-size)
* SQLite databases will not persist across site deployments, requiring a full reindex every time your site changes
* You can use a Postgres database instead but this causes a (very) slight performance hit on page loads

That said, Heroku is a great platform for running a smaller Publ site. Additionally, on the higher tiers you get some nice features like automatic load-balancing and staged deployments. Which is probably overkill for the sites you're running Publ for, but it's still nice to have.

### Prerequisites

You'll need a [Heroku](http://heroku.com/) account, of course, and you'll want to go through their [Python introduction](https://devcenter.heroku.com/articles/getting-started-with-python) to get your local environment configured.

This also assumes you are using a git repository to manage your website files.

### Setting up your site files

The easiest way to configure Heroku is using `pipenv` and `gunicorn`. Assuming you have a local test version of your site on your computer, do the following:

```bash
cd WEBSITE_DIRECTORY
pipenv --three install Publ gunicorn
```

This will install all of the deployment requirements for Heroku, and configure them in your `Pipfile` and `Pipfile.lock`. Check these files into your git repository.

At this point you should be able to run it locally with:

```bash
pipenv run gunicorn app:app
```

and connecting to the URL gunicorn tells you (likely `http://127.0.0.1:8000/`).

Next, you'll need a `Procfile` which tells Heroku how to launch your site:

```text
web: gunicorn app:app
```

Check this file in as well.

### Setting up Heroku

Now you should be ready to deploy! You'll need to create your Heroku app and add the git remote to your site's git repository with e.g.:

```bash
heroku create
heroku git:remote -a NAME_OF_APP
```

replacing `NAME_OF_APP` with whatever name `heroku create` gave you.

Deploying to Heroku is now as simple as:

```bash
git push heroku
```

You may also want to run `heroku logs --tail` to watch its progress.

### Database persistence

As mentioned above, most of the website startup time is taken up by the initial content index. Since Heroku does not persist your filesystem, you might want to consider using a Postgres database to store the index persistently. Note that this *will* slow your site down a little bit (since accessing an in-process SQLite database is faster than going over the network to talk to Postgres), but it reduces the amount of site downtime during a content update so that might be a worthwhile tradeoff depending on your needs.

This slowdown can also be mitigated by increasing your cache timeout; since the site will be redeployed whenever content updates, the cache timeout really only affects how soon scheduled posts will appear after they are set to go live.

To provision a Postgres database at the free tier, from your local git repository, type the following:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

This creates a database and then exports it to your environment as `DATABASE_URL`. Unfortunately, PonyORM does not *quite* directly support database connection URLs, so we need to do a bit more work on our end. Namely, in `app.py`, change the `database_config` part to the following:

```python
from urllib.parse import urlparse

config = {
    'database_config': {
        'provider': urlparse(os.environ['DATABASE_URL']).scheme,
        'dsn': os.environ['DATABASE_URL']
    } if 'DATABASE_URL' in os.environ else {
        'provider': 'sqlite',
        'filename': os.path.join(APP_PATH, 'index.db')
    },
}
```

A full example can be seen in the [`app.py` for this site's repository](https://github.com/PlaidWeb/publ-site/blob/master/app.py).

You will also need to install the `psycopg2` library; this is simply:

```bash
pipenv install psycopg2
```

If you get an error about it failing to install (accompanied with a gigantic log) you might try pinning the version:

```bash
pipenv install 'psycopg2<2.8'
```

For local testing (to make sure everything is wired up correctly) you can do:

```bash
DATABASE_URL=`heroku config:get DATABASE_URL` pipenv run gunicorn app:app
```

although be advised that the database scan will be *much* slower than in production.
