""" Main Publ application """


import logging
import logging.handlers
import os
import signal
from urllib.parse import urlparse

import authl.flask
import flask
import publ
from flask_hookserver import Hooks

LOGGER = logging.getLogger(__name__)
LOGGER.info("Setting up")


APP_PATH = os.path.dirname(os.path.abspath(__file__))

config = {
    # The database connection configuration. This is a list of parameters
    # passed to PonyORM's db.bind() method; see
    # https://docs.ponyorm.com/firststeps.html#database-binding
    # for more information.
    #
    # NOTE: If this involves credentials (e.g. mysql, postgres, etc.) you
    # should put this into an appropriate environment variable in a file that
    # doesn't get checked in.
    'database_config': {
        'provider': urlparse(os.environ['DATABASE_URL']).scheme,
        'dsn': os.environ['DATABASE_URL']
    } if 'DATABASE_URL' in os.environ else {
        'provider': 'sqlite',
        'filename': os.path.join(APP_PATH, 'index.db')
    },

    # Where we keep our content files
    # 'content_folder': os.path.join(APP_PATH, 'content'),

    # How often to forcibly rescan the content index (0 or None to disable)
    # 'index_rescan_interval': 7200,

    # How often to clean the rendition cache, in seconds
    # 'image_cache_interval': 3600,

    # Maximum age for image renditions, in seconds
    # 'image_cache_age': 86400 * 7,  # one week

    # Where we keep our template files
    # 'template_folder': os.path.join(APP_PATH, 'templates'),

    # Where we keep our static content files
    # 'static_folder': os.path.join(APP_PATH, 'static'),

    # Where the static content files should map into URL-space
    # This can be used to put it on a separate domain for e.g. a CDN
    # that is pointed at our static directory
    # 'static_url_path': '/static',                      # default
    # 'static_url_path': 'https://cdn.example.com/',     # CDN example

    # The name of the directory to put image renditions into within
    # static_directory. This directory will be filled with your image renditions
    # and should probably not be backed up (i.e. put it in .gitignore or
    # similar)
    # 'image_output_subdir': '_img',

    # The timezone for the site
    # 'timezone': tz.tzlocal(),      # default; based on the server
    'timezone': 'US/Pacific',      # by name

    # Caching configuration; see https://pythonhosted.org/Flask-Cache for
    # more information
    'cache': {
        'CACHE_TYPE': 'memcached',
        'CACHE_DEFAULT_TIMEOUT': 300,
        'CACHE_THRESHOLD': 500,
        'CACHE_KEY_PREFIX': 'publ.beesbuzz.biz',
    } if not os.environ.get('FLASK_DEBUG') else {
        'CACHE_NO_NULL_WARNING': True
    },

    'auth': {
        'SMTP_HOST': 'localhost',
        'SMTP_PORT': 25,
        'EMAIL_FROM': 'nobody@beesbuzz.biz',
        'EMAIL_SUBJECT': 'Sign in to publ.beesbuzz.biz',

        'FEDIVERSE_NAME': 'Publ CMS',
        'FEDIVERSE_HOMEPAGE': 'http://publ.beesbuzz.biz/',

        'INDIEAUTH_CLIENT_ID': authl.flask.client_id,

        'TWITTER_CLIENT_KEY': os.environ.get('TWITTER_CLIENT_KEY'),
        'TWITTER_CLIENT_SECRET': os.environ.get('TWITTER_CLIENT_SECRET'),

        'TEST_ENABLED': True,
    },
}

# Create the application instance
app = publ.Publ(__name__, config)

# Configure the session security
app.secret_key = os.environ.get('AUTH_SECRET', 'A totally unguessable secret key!')

# Configure the GitHub publishing webhook
app.config['GITHUB_WEBHOOKS_KEY'] = os.environ.get('GITHUB_SECRET')
app.config['VALIDATE_IP'] = False


@app.path_alias_regex(r'/\.well-known/(host-meta|webfinger).*')
def redirect_bridgy(match):
    """ support ActivityPub via fed.brid.gy """
    return 'https://fed.brid.gy' + flask.request.full_path, False


@app.path_alias_regex(r'/issue/(.*)')
def redirect_github_issue(match):
    """ Custom routing rule to redirect /issue/NNN to the corresponding
    issue on GitHub """
    return 'https://github.com/PlaidWeb/Publ/issues/' + match.group(1), True

@app.path_alias_regex(r'/site-issue/(.*)')
def redirect_github_site_issue(match):
    """ Custom routing rule to redirect /issue/NNN to the corresponding
    issue on GitHub """
    return 'https://github.com/PlaidWeb/Publ-site/issues/' + match.group(1), True



# Deployment hook for self-hosted instance
hooks = Hooks(app, url='/_gh')


@hooks.hook('push')
def deploy(data, delivery):
    import threading
    import subprocess
    import flask

    try:
        result = subprocess.check_output(
            ['./deploy.sh', 'nokill'],
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        LOGGER.error("Deployment failed: %s", err.output)
        return flask.Response(err.output, status_code=500, mimetype='text/plain')

    def restart_server(pid):
        LOGGER.info("Restarting")
        os.kill(pid, signal.SIGHUP)

    LOGGER.info("Restarting server in 3 seconds...")
    threading.Timer(3, restart_server, args=[os.getpid()]).start()

    return flask.Response(result, mimetype='text/plain')
