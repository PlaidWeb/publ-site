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

1. Add the following functions to your `app.py`:

    ```python
    !app.py
    import arrow
    import flask
    import werkzeug.exceptions

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
    ```

2. Add the following template as `templates/429.html`:

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

    <form method="POST" id='proxy' action="{{url_for('gatekeeper')}}">
        <input type="hidden" name="redir" value="{{request.full_path}}">
        <input type="hidden" name="sid" value="{{arrow.now().format('X')}}">
        <input type="submit" value="I'm actually here">
    </form>
    </body>
    </html>
    ```

Out of the box, this will present a sentience check to anyone who is exhibiting basic bad-crawler behavior, which will be skipped for anything that has a cookie indicating that the test has previously been passed. For folks running browsers with JavaScript the test should automatically pass, as well.

The test is very simple; it just indicates that the form has been submitted within the past hour and that the agent submitting the form still has the same IP address and browser user agent, as those values will be stable during a particular browsing session and tend to be randomized by the AI crawlers. Keep in mind that there may be some situations in which the IP address for a legitimate user is randomized on a per-request basis, though (such as certain VPN or caching proxy configurations, or particularly dysfunctional CGNAT deployments).