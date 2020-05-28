Title: User authentication
Date: 2019-07-13 02:00:10-07:00
Entry-ID: 706
UUID: babb5cdc-e98f-53dc-9fc8-e7edae684291

How to configure post privacy in Publ.

.....

Publ supports the use of [Authl](https://github.com/PlaidWeb/Authl), an authentication wrapper library, to make it easier to control access to private posts.  By configuring a few values in the [application configuration](publ-python.md) and setting up some user groups, you can get fine-grained control over who can see specific posts.

The main things to pay attention to are as follows:

## Application configuration

### <span id="secret_key"></span>`secret_key`

`app.secret_key` controls the signing of the authentication tokens. Essentially, it needs to be kept secret, to prevent others from gaining access that they shouldn't have.

By default this is set randomly every time the application starts, which is secure but it means that any time the server restarts, everyone will be logged out. So, you'll probably want to set this to a secret value that gets set with an environment variable or the like; for example, after the `app` is created:

```python
app.secret_key = os.environ['AUTH_SECRET']
```

Alternately, you might want to automatically generate the secret key as a local file:

```python
if not os.path.isfile('.sessionkey'):
    import uuid
    with open('.sessionkey', 'w') as file:
        file.write(str(uuid.uuid4()))
    os.chmod('.sessionkey', 0o600)
with open('.sessionkey') as file:
    app.secret_key = file.read()
```

### <span id="auth">`auth`</span>

This is a key-value dictionary that is sent along to Authl's `from_config` settings. See the Authl documentation for the most up-to-date configuration flags; here are some that you are likely to want to use:

* SSL options:
    * <span id="force_https">`AUTH_FORCE_HTTPS`: set to True if logins should all go over HTTPS instead of HTTP (highly recommended!)</span>
* Email options:
    * `SMTP_HOST`: the email host (required; usually `localhost`)
    * `SMTP_PORT`: the email port (required; usually `25`)
    * `SMTP_USE_SSL`: whether to use SSL for the SMTP connection (not necessary for `localhost` but highly recommended for anything else)
    * `EMAIL_FROM`: the From: address to use when sending an email (required)
    * `EMAIL_SUBJECT`: the Subject: to use for a login email (required)
    * `EMAIL_LOGIN_TIMEOUT`: How long (in seconds) the user has to follow the login link
* [IndieAuth](https://indieweb.org/IndieAuth) options:
    * `INDIEAUTH_CLIENT_ID`: The client ID to send to the remote IndieAuth endpoint (required)[^clientid_iauth]
* Fediverse (e.g. [Mastodon](https://joinmastodon.org/)) options:
    * `FEDIVERSE_NAME`: the name of your website (required)
    * `FEDIVERSE_HOMEPAGE`: your website's main URL (recommended)
* [Twitter](https://twitter.com/) options:
    * `TWITTER_CLIENT_KEY`, `TWITTER_CLIENT_SECRET`: a Twitter application client key and secret

        Note that for safety's sake these should be read from environment variables, rather than checked in to code.

        In order to get these you need to go to the [Twitter developer portal](https://developer.twitter.com/) and register your website as an application. If asked for app usage, simply say "To provide Login with Twitter functionality to my website" or similar.

        You will also need to register your Twitter login callback URLs; this will probably be something like `https://example.com/_cb/t`.

* Test handler options:
    * `TEST_ENABLED`: whether to enable the `test:` test handler. Don't do this.

[^clientid_iauth]: Authl provides a convenience function, `authl.flask.client_id`, which will fill this in correctly. To use this, you will need to `import authl.flask` at the top of your `app.py` and then set `INDIEAUTH_CLIENT_ID` to that, *without* quotes; for an example see [this website's `app.py`](https://github.com/PlaidWeb/publ-site/blob/master/app.py).

### <span id="user_list"></span>`user_list`

This is the filename of a file where you configure access to users and groups. The format is based on a common configuration file format; see the [`user.cfg` format](formats/user config.md) for more information.

### <span id="admin_group"></span>`admin_group`

This configuration setting specifies which user group will have administrative access; by default this is set to `admin`. Thus, in the above example, the user who logs in as `http://example.com/me` will be a member of that group.

You can also set this configuration option to a specific identity.

Members of the administrative group will always be able to see all entries, and will also have access to the administrative functions of the site (such as being able to see the user log).

## Adding authentication to entries

See [the Auth: header](322#auth).

## Seeing who's been logging on

The admin dashboard lives at `/_admin`; for example, [on this site](/_admin). It is restricted to members of the administrative group (you can [log in as `test:admin`](/_login/_admin?me=test:admin) to see it).
