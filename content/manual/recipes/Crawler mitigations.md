Title: Crawler mitigations
Tag: recipe
Tag: security
Tag: performance
Tag: stability
Date: 2026-02-26 10:48:15-08:00
UUID: b2ccc8e0-270c-4cde-8b36-b3c313cd0c2e
Entry-ID: 210

Reducing server load caused by badly-behaved web crawlers.

.....

In this day and age it's necessary to have mitigations in place to prevent badly-behaving web crawlers from taking down every single website. Both legitimate search bots *and* things like AI/LLM crawlers do a bunch of nasty tricks to try to extract as much detail as possible from a website, even when signals are present to indicate which pages are worth crawling.

This recipe is a starting point for implementing a simple "sentience check" into Publ websites, which has shown itself to be just as effective as more heavyweight options such as Anubis or Cloudflare's "managed challenge" CAPTCHA. Setting it up is pretty simple:

1. Add the [`user-agents`](https://pypi.org/project/user-agents) package to your environment (typically with `poetry add user-agents`)

2. Add the following functions to your `app.py`:

    ```python
    !app.py
    @app.before_request
    def antiscraper():
        """ If something looks like a scraper, give it a sentience check """
        import flask
        import user_agents
        import werkzeug.exceptions

        # Flag bots to remove page elements
        if user_agents.parse(flask.request.headers.get('User-Agent', '')).is_bot:
            flask.g.is_bot = True

        # Logged-in users have passed the test already
        if publ.user.get_active():
            return

        # Users with an 'sid' cookie have passed the test already
        if flask.session.get('sid'):
            return

        # Send possible crawlers to the login page
        # Initial score: number of items in the GET arguments
        score = len(list(flask.request.args.items(True)))

        # add any other custom signals to the score

        if score > 2:
            raise werkzeug.exceptions.TooManyRequests("Sentience test")

        return

    @app.route('/_zuul', methods=['POST'])
    def gatekeeper():
        """ Sentience check callback """
        import datetime
        import flask

        redir = flask.request.form['redir']
        LOGGER.info(f"redirecting to {redir}")
        flask.session['sid'] = datetime.datetime.now()
        return flask.redirect(f'{redir}', code=303)
    ```

3. Add the following template as `templates/429.html`:

    ```html+jinja
    !templates/429.html
    <!DOCTYPE html>
    <html><head><title>Sentience test</title>
    <script>
    window.addEventListener("load", () => {
        document.forms['proxy'].submit();
    });
    </script>
    </head>
    <body>
    <h1>Sentience check</h1>

    <form method="POST" id="proxy" action="{{url_for('gatekeeper')}}">
        <input type="hidden" name="redir" value="{{request.full_path}}">
        <input type="submit" value="I'm actually here">
    </form>
    </body>
    </html>
    ```

Out of the box, this will present a sentience check to anyone who is exhibiting basic bad-crawler behavior, which will be skipped for anything that has a cookie indicating that the test has previously been passed. For folks running browsers with JavaScript the test should automatically pass, as well.

This recipe also adds a `g.is_bot` flag to all page views, which can be used to suppress page elements for properly-disclosed webcrawlers. For example, you may want to not show email links, comment forms, or tag browsers to bots, as even good bots will now try to traverse tag browsers, and spammers will historically look for specific page features to try to find sites to spam. For example:

```jinja
{% if not g.is_bot %}
{{render_tagcloud(entry)}}
{% endif %}
```

You can also use this functionality to present different content entirely to crawlers; for example:

```jinja
{% if g.is_bot %}
Hello bot!
{% else %}
Hello user!
{% endif %}
```
