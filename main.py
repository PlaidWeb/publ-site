""" Main Publ application """

from dateutil import tz

import os
import logging
import logging.handlers
from urllib.parse import urlparse
import flask

import publ

if os.path.isfile('logging.conf'):
    logging.config.fileConfig('logging.conf')
else:
    try:
        os.makedirs('logs')
    except FileExistsError:
        pass
    logging.basicConfig(level=logging.INFO,
                        handlers=[
                            logging.handlers.TimedRotatingFileHandler(
                                'logs/publ.log'),
                            logging.StreamHandler()
                        ])

logging.info("Setting up")

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
    #'content_folder': os.path.join(APP_PATH, 'content'),

    # How often to forcibly rescan the content index (0 or None to disable)
    #'index_rescan_interval': 7200,

    # How often to clean the rendition cache, in seconds
    #'image_cache_interval': 3600,

    # Maximum age for image renditions, in seconds
    #'image_cache_age': 86400 * 7,  # one week

    # Where we keep our template files
    #'template_folder': os.path.join(APP_PATH, 'templates'),

    # Where we keep our static content files
    #'static_folder': os.path.join(APP_PATH, 'static'),

    # Where the static content files should map into URL-space
    # This can be used to put it on a separate domain for e.g. a CDN
    # that is pointed at our static directory
    #'static_url_path': '/static',                      # default
    #'static_url_path': 'https://cdn.example.com/',     # CDN example

    # The name of the directory to put image renditions into within
    # static_directory. This directory will be filled with your image renditions
    # and should probably not be backed up (i.e. put it in .gitignore or
    # similar)
    #'image_output_subdir': '_img',

    # The timezone for the site
    #'timezone': tz.tzlocal(),      # default; based on the server
    'timezone': 'US/Pacific',      # by name

    # Caching configuration; see https://pythonhosted.org/Flask-Cache for
    # more information
    'cache': {
        'CACHE_TYPE': 'simple',
        'CACHE_DEFAULT_TIMEOUT': 600,
        'CACHE_THRESHOLD': 100
    } if not os.environ.get('FLASK_DEBUG') else {
        'CACHE_NO_NULL_WARNING': True
    },
}

app = publ.publ(__name__, config)


@app.route('/issue/<int:id>')
def redirect_github_issue(id):
    return flask.redirect('https://github.com/PlaidWeb/Publ/issues/{}'.format(id))

if __name__ == "__main__":
    app.run(port=os.environ.get('PORT', 5000))
