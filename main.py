""" Main Publ application """

from dateutil import tz

import os
import logging
import logging.handlers

import publ

if os.path.isfile('logging.conf'):
    logging.config.fileConfig('logging.conf')
else:
    if not os.path.isdir('logs'):
        os.makedirs('logs')
    logging.basicConfig(level=logging.INFO,
                        handlers=[
                            logging.handlers.TimedRotatingFileHandler(
                                'logs/publ.log'),
                            logging.StreamHandler()
                        ])

logging.info("Setting up")

APP_PATH = os.path.dirname(os.path.abspath(__file__))

config = {
    # The database connection string. NOTE: If this involves credentials
    # (e.g. mysql, postgres, etc.) you should put this into an appropriate
    # environment variable in a file that doesn't get checked in.
    'database': 'sqlite:///index.db',

    # Where we keep our content files
    #'content_folder': os.path.join(APP_PATH, 'content'),

    # How often to forcibly rescan the content index (0 or None to disable)
    #'index_rescan_interval': 300

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
    #'timezone': 'US/Pacific',      # by name

    # Caching configuration; see https://pythonhosted.org/Flask-Cache for
    # more information
    'cache': {
        'CACHE_TYPE': 'simple',
        'CACHE_DEFAULT_TIMEOUT': 30,
        'CACHE_THRESHOLD': 100
    } if not os.environ.get('FLASK_DEBUG') else {},
}

app = publ.publ(__name__, config)

if __name__ == "__main__":
    app.run(port=os.environ.get('PORT', 5000))
