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
    @app.before_request
    def antiscraper():
        """ If something looks like a scraper, give it a sentience check """
        import arrow
        import flask
        import werkzeug.exceptions

        # Logged-in users have passed the test already
        if publ.user.get_active():
            return

        try:
            # Check to see if the session data matches the user's data
            if (flask.session['addr'] == flask.request.remote_addr and
                arrow.get(flask.session['sid']) > arrow.now().shift(days=-3) and
                flask.session['ua'] == flask.request.headers.get('User-Agent')):
                return
        except (KeyError, arrow.ParserError):
            pass

        # Send possible crawlers to the sentience test
        # Initial score: number of items in the GET arguments
        score = len(list(flask.request.args.items(True)))

        # add any other custom signals to the score

        if score > 2:
            raise werkzeug.exceptions.TooManyRequests("Sentience test")

        return

    @app.route('/_zuul', methods=['POST'])
    def gatekeeper():
        """ Sentience check callback """
        import arrow
        import flask

        redir = flask.request.form['redir']
        flask.session['sid'] = flask.request.form['sid']
        flask.session['addr'] = flask.request.remote_addr
        flask.session['ua'] = flask.request.headers.get('User-Agent')
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
        <input type="hidden" name="sid" value="{{arrow.now()}}">
        <input type="submit" value="I'm actually here">
    </form>
    </body>
    </html>
    ```

Out of the box, this will present a sentience check to anyone who is exhibiting basic bad-crawler behavior, which will be skipped for anything that has a cookie indicating that the test has previously been passed. For folks running browsers with JavaScript the test should automatically pass, as well.

The test is very simple; it just indicates that the form has been submitted within the past three days and that the agent submitting the form still has the same IP address and browser user agent, as those values will be stable during a particular browsing session and tend to be randomized by the AI crawlers. Keep in mind that there may be some situations in which the IP address for a legitimate user is randomized on a per-request basis, though (such as certain VPN or caching proxy configurations, or particularly dysfunctional CGNAT deployments).
