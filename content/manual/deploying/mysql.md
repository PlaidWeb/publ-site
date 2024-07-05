Title: Using MySQL/MariaDB as your backing store
Tag: mysql
Tag: deployment
Tag: configuration
sort-title: 500
Date: 2024-07-05 11:45:08-07:00
Entry-ID: 764
UUID: f9569d5a-44b7-549f-b536-1de795fdd8d7

How to use MySQL as the index database

.....

For smaller Publ sites, the suggested configuration is to use [SQLite](https://sqlite.org/) for the index database, as it is low-maintenance and performs very well due to being in-process and taking advantage of the operating system's disk cache.

However, sometimes it's helpful to use a larger-scale database system for the deployment, primarily to gain access to finer-grained locking. This is especially useful in situations where there are many thousands of entries and a desire to keep the site running at full capacity during a reindex.

Here is a configuration snippet that allows you to use MySQL/MariaDB on your Publ site:

```python
!app.py

# ...

if 'DATABASE_URL' in os.environ:
    import urllib.parse
    parsed = urllib.parse.urlparse(os.environ['DATABASE_URL'])
    user = re.match(r'(.*):(.*)@(.*)', parsed.netloc)
    db_config = {
            'provider': parsed.scheme,
            'user': user.group(1),
            'password': user.group(2),
            'host': user.group(3),
            'database': parsed.path[1:],
            # charset and collation must be specified, as the MySQL defaults do
            # not properly support emoji and other 4-byte characters
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_bin',
        }
else:
    db_config = {'provider': 'sqlite', 'filename': os.path.join(APP_PATH, 'index.db')}

config = {
    'database_config': db_config,
    # ...
```

Then when running the site, set an environment variable such as:

```
DATABASE_URL='mysql://username:password@server/dbname'
```

If migrating from SQLite to MySQL, it is a good idea to create the index first before flipping the configuration:

```
DATABASE_URL='mysql://username:password@server/dbname' poetry run flask publ reindex
```

An alternate way to store the database configuration is to put it into a local `db_config.py` file, like so:

```python
!db_config.py

db_config = {
    'provider': 'mysql',
    'user': 'db username',
    'password': 'db password',
    'host': 'localhost',
    'database': 'my_site',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_bin'
}
```

```python
!app.py

# ...

try:
    from .db_config import db_config
except ImportError:
    db_config = {'provider': 'sqlite', 'filename': os.path.join(APP_PATH, 'index.db')}

config = {
    'databse_config': db_config,
    # ...
}
```

but as always it is important to ensure the security of this file; environment-based configuration is traditionally considered to be much easier to secure and prevent mishaps such as accidentally checking it into source control.
