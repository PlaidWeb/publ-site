Title: User object
Path-Alias: /api/user
Date: 2020-08-01 23:51:44-07:00
Entry-ID: 733
UUID: a16621e8-31a5-5f50-82eb-2f52bdd5330d

Template API for the `user` object
.....

The `user` object provides the following:

* **`identity`**: The identity URL of the user
* **`humanize`**: A humanized version of the identity URL

* **`name`**: The display name of the user

* **`profile`**: The user profile; see the [Authl documentation](https://authl.readthedocs.io/en/latest/authl.html#authl.disposition.Verified) for the relevant keys.

    Note that this will not necessarily be available, depending on how and when the user logged in. For example, if the database has been fully reset (due to e.g. a schema upgrade or a server migration) since they last logged in, or if the user logged in from a different instance on a load-balanced configuration using a per-instance database, the profile will likely not be present.

* **`groups`**: A list of the groups they belong to (not including the user's identity group)
* **`auth_groups`**: The full list of matching authentication groups (including the user's own identity group)

* **`is_admin`**: `True` if the user is a member of the administrative group

* **`auth_type`**: How the user's authentication was obtained; possible values:

    * `'session'`: Normal login flow/session cookie
    * `'token'`: Bearer token

* **`scope`**: The user's permission scopes, if applicable (typically if the login was via a bearer token)

* **`last_login`**: The last time the user logged in

    This may not be available, per the same rules as `user.profile`

* **`last_seen`**: The last time the user was active on the site

Generally there is not much use in providing this information to end-users of the site; for the most part you should only use `user.name` to address the user, and possibly use `user.groups` to check for particular group membership if that is something you want to show them. For example, if you use user groups as a means of managing memberships or rewards or the like, you could do something like:

```jinja

Hello, {{user.name}}.
{% if 'current_members' in user.groups %}
    Your membership is current!
{% else %}
    You aren't currently a member. Please consider <a href="/subscribe">becoming one</a>.
{% endif %}
```

When extending Publ using additional Python functions, the current user can be retrieved with:

```python
import publ.user
user = publ.user.get_active()
```

