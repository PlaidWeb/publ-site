Title: User authentication
Date: 2019-07-13 02:00:10-07:00
Entry-ID: 706
UUID: babb5cdc-e98f-53dc-9fc8-e7edae684291

How to configure post privacy in Publ.

.....

==Note:== This functionality is experimental. Use at your own risk.

Publ supports the use of [Authl](https://github.com/PlaidWeb/Authl), an authentication wrapper library, to make it easier to control access to private posts.  By configuring a few values in the [application configuration](publ-python.md) and setting up some user groups, you can get fine-grained control over who can see specific posts.

The main things to pay attention to are as follows:

## Application configuration

### <span id="secret_key"></span>`secret_key`

This configuration setting controls the signing of the authentication tokens. Essentially, it needs to be kept secret, to prevent others from gaining access that they shouldn't have.

By default this is set randomly every time the application starts, which is secure but it means that any time the server restarts, everyone will be logged out. So, you'll probably want to set this to a secret value that gets set with an environment variable or the like.

### <span id="auth"></span>`auth`

This is a key-value dictionary that is sent along to Authl's `from_config` settings. See the Authl documentation for the most up-to-date configuration flags; at present the following configuration flags exist:

* Email options:
    * `SMTP_HOST`: the email host (required; usually `localhost`)
    * `SMTP_PORT`: the email port (required; usually `25`)
    * `SMTP_USE_SSL`: whether to use SSL for the SMTP connection (not necessary for `localhost` but highly recommended for anything else)
    * `SMTP_USERNAME`: the username to use with the SMTP server
    * `SMTP_PASSWORD`: the password to use with the SMTP server
    * `EMAIL_FROM`: the From: address to use when sending an email (required)
    * `EMAIL_SUBJECT`: the Subject: to use for a login email (required)
    * `EMAIL_LOGIN_TIMEOUT`: How long (in seconds) the user has to follow the login link
    * `EMAIL_CHECK_MESSAGE`: The message to send back to the user
    * `EMAIL_TEMPLATE_FILE`: A path to a text file for the email message
* [IndieLogin](https://indielogin.com) options:
    * `INDIELOGIN_CLIENT_ID`: the client ID to send to the IndieLOgin service (required)
    * `INDIELOGIN_ENDPOINT`: the endpoint to use for the IndieLogin service (default: https://indielogin.com/auth)
    * `INDIELOGIN_OPEN_MAX`: the maximum number of open requests to track
    * `INDIELOGIN_OPEN_TTL`: the time-to-live of an open request, in seconds
* [Mastodon](https://joinmastodon.org) options:
    * `MASTODON_NAME`: the name of your website (required)
    * `MASTODON_HOMEPAGE`: your website's homepage (recommended)
* Test handler options:
    * `TEST_ENABLED`: whether to enable the `test:` test handler. Don't do this.

### <span id="user_list"></span>`user_list`

This is the filename of a file where you configure access to users and groups. The format is based on a common configuration file format. Here is an example configuration:

```ini
[admin]
http://example.com/me

[friends]
alice@example.com
bob@example.com
http://example.com/~cathy
good_friends

[good_friends]
http://bestfriend.example.com

[http://bestfriend.example.com]
bestfriend@example.com
```

Basically, you describe a group in `[brackets]` and then list the identities associated with that group, and other groups that should be a part of that group. And, identity names can also be used as group names, so if you have someone who logs in using different identities that you want to treat equivalently, you can simply put those other identities into a group.

So, in the above example, `alice@example.com`, `bob@example.com`, `http://example.com/~cathy`, and all members of the `good_friends` group are members of the `friends` group. Then, `http://bestfriend.example.com/` is a member of `good_friends` (and therefore `friends`), and `bestfriend@example.com` is a member of the `http://bestfriend.example.com/` group (and therefore `good_friends` and `friends` as well).

You can also start a line with `#` or `;` to indicate that it's a comment.

### <span id="admin_group"></span>`admin_group`

This configuration setting specifies which user group will have administrative access; by default this is set to `admin`. Thus, in the above example, the user who logs in as `http://example.com/me` will be a member of that group.

You can also set this configuration option to a specific identity.

Members of the administrative group will always be able to see all entries, and will also have access to the administrative functions of the site (such as being able to see the user log).
