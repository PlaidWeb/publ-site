""" Main Publ application """


import logging
import logging.handlers
import os
import signal
from urllib.parse import urlparse

import arrow
import authl.flask
import flask
import publ
import werkzeug.exceptions
from flask_github_webhook import GithubWebhook
from werkzeug.middleware.proxy_fix import ProxyFix

if os.path.isfile('logging.conf'):
    logging.config.fileConfig('logging.conf')
else:
    try:
        os.makedirs('logs')
    except FileExistsError:
        pass
    logging.basicConfig(level=logging.WARNING,
                        handlers=[
                            logging.handlers.TimedRotatingFileHandler(
                                'logs/publ.log', when='D'),
                            logging.StreamHandler()
                        ],
                        format="%(levelname)s:%(threadName)s:%(name)s:%(message)s")

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

    # Disable the content watchdog when running in production
    'index_enable_watchdog': bool(os.environ.get('FLASK_DEBUG')),

    # How often to clean the rendition cache, in seconds
    # 'image_cache_interval': 3600,

    # Maximum age for image renditions, in seconds
    # 'image_cache_age': 86400 * 7,  # one week

    # Only enable the content watchdog when running in test/debug mode
    'index_enable_watchdog': bool(os.environ.get('FLASK_DEBUG')),

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

    # How many image rendering threads to use
    'image_render_threads': 2,

    # The timezone for the site
    # 'timezone': tz.tzlocal(),      # default; based on the server
    'timezone': 'US/Pacific',      # by name

    # Caching configuration; see https://pythonhosted.org/Flask-Cache for
    # more information
    'cache': {
        'CACHE_TYPE': 'memcached',
        'CACHE_DEFAULT_TIMEOUT': 3659,
        'CACHE_THRESHOLD': 500,
        'CACHE_KEY_PREFIX': 'publ.beesbuzz.biz',
    } if not os.environ.get('FLASK_DEBUG') else {
        'CACHE_NO_NULL_WARNING': True
    },

    'auth': {
        'AUTH_FORCE_HTTPS': not os.environ.get('FLASK_DEBUG'),

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

    'secret_key': os.environ.get('AUTH_SECRET', 'A totally unguessable secret key!'),

    'search_index': '_index',
}

# Create the application instance
app = publ.Publ(__name__, config)

# Configure the GitHub publishing webhook
app.config['GITHUB_WEBHOOK_ENDPOINT'] = '/_gh'
app.config['GITHUB_WEBHOOK_SECRET'] = os.environ.get('GITHUB_SECRET')


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


def keymaster(sid):
    """ Generates a salted token for the browser """
    import hashlib

    parts = [
        str(sid),
        flask.request.remote_addr,
        flask.request.headers.get('User-Agent')
    ]
    token = hashlib.md5('|'.join(parts).encode('utf-8'))
    return token.digest()


@app.before_request
def antiscraper():
    """ Dissuade aggressive bots from pummeling the site """

    # Logged-in users have passed the test already
    if publ.user.get_active():
        return

    # Send possible crawlers to the login page
    score = len(list(flask.request.args.items(True)))
    if score > 1:
        # Check for an existing sentience token
        try:
            sid, token = flask.session['vinz']
            if (arrow.now().shift(hours=-1) < arrow.get(float(sid)) < arrow.now() and
                    keymaster(sid) == token):
                return
        except (KeyError, ValueError, arrow.ParserError):
            pass

        raise werkzeug.exceptions.TooManyRequests("Sentience test")

    return


@app.route('/_zuul', methods=['POST'])
def gatekeeper():
    """ Check the test response and set the salted token upon passing """
    try:
        sid = float(flask.request.form['sid'])
        if arrow.get(sid) > arrow.now():
            # Someone's trying to set a token that'll last longer
            raise werkzeug.exceptions.BadRequest("Hello time traveler")
        if arrow.get(sid) < arrow.now().shift(minutes=-5):
            # Someone took a while to respond to the form
            raise werkzeug.exceptions.TooManyRequests("Try again")
    except ValueError:
        raise werkzeug.exceptions.BadRequest("Nice try")

    redir = flask.request.form['redir']
    flask.session['vinz'] = sid, keymaster(sid)
    return flask.redirect(f'{redir}', code=303)


# Deployment hook for self-hosted instance
hooks = GithubWebhook(app)


@hooks.hook()
def deploy(data):
    import subprocess
    import threading

    import flask

    LOGGER.info("Got github hook with data: %s", data)

    try:
        result = subprocess.check_output(
            ['./deploy.sh', 'nokill'],
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        LOGGER.error("Deployment failed: %s", err.output)
        return flask.Response(err.output, status=500, mimetype='text/plain')

    def restart_server(pid):
        LOGGER.info("Restarting")
        os.kill(pid, signal.SIGHUP)

    LOGGER.info("Restarting server in 3 seconds...")
    threading.Timer(3, restart_server, args=[os.getpid()]).start()

    return flask.Response(result, mimetype='text/plain')


app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
