Title: Heroku
Date: 2018-10-13 14:23:23-07:00
Entry-ID: 1210
UUID: 5744383f-5712-5011-9a9d-1b3c9806e090
Path-Alias: /heroku

How to deploy a Publ website to [Heroku](http://heroku.com).

.....

Heroku is probably the easiest environment to configure for Publ, especially for
smaller websites. (Larger sites *may* work but Heroku imposes a [1 GB limit on your deployment size](https://devcenter.heroku.com/articles/limits#git-repos) and a [500MB limit on your slug size](https://devcenter.heroku.com/articles/limits#slug-size).)

### Prerequisites

You'll need a [Heroku](http://heroku.com) account, of course, and you'll want to go through their [Python introduction](https://devcenter.heroku.com/articles/getting-started-with-python) to get your local environment configured.

This also assumes you are using a git repository to manage your website files.

### Setting up your site files

The easiest way to configure Heroku is using `pipenv` and `gunicorn`. Assuming you have a local test version of your site on your computer, do the following:

```bash
cd (website_directory)
pipenv --three install Publ gunicorn
```

This will install all of the deployment requirements for Heroku, and configure them in your `Pipfile` and `Pipfile.lock`. Check these files into your git repository.

At this point you should be able to run it locally with:

```bash
pipenv run gunicorn main:app
```

and connecting to the URL gunicorn tells you (likely `http://127.0.0.1:8000/`).

Next, you'll need a `Procfile` which tells Heroku how to launch your site:

```
web: gunicorn main:app
```

Check this file in as well.

### Setting up Heroku

Now you should be ready to deploy! You'll need to add your Heroku remote to your site's git repository with e.g.:

```bash
heroku git:remote
```

Deploying to Heroku is now as simple as:

```bash
git push heroku
```

You may also want to run `heroku logs --tail` to watch its progress.

### Improving performance with a database

Most of the website startup time is taken up by the content indexing. Since Heroku does not persist your filesystem, you might want to consider using a SQL database to store the index persistently.

From your local git repository, type the following:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

This creates a database and then exports it to your environment as `DATABASE_URL`. Unfortunately, PonyORM does not *quite* directly support database connection URLs, so we need to do a bit more work on our end. Namely, in `main.py`, change the `database_config` part to the following:

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

A full example can be seen in the [`main.py` for this site's repository](https://github.com/PlaidWeb/publ-site/blob/master/main.py).

You will also need to install the `psycopg2` library; this is simply:

```bash
pipenv install psycopg2
```

For local testing (to make sure everything is wired up correctly) you can do:

```bash
DATABASE_URL=`heroku config:get DATABASE_URL` pipenv run gunicorn main:app
```

although be advised that the database scan will probably be much slower than in production.
