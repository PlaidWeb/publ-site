Title: Continuous deployment with git
Date: 2018-12-16 23:23:07-08:00
Entry-ID: 441
UUID: b023c99e-0f41-51ea-9d41-5e575b37339d

How to use git hooks to automatically deploy site content

.....

## Same-server deployment

This is the approach I use for managing my site content on [my main website](http://beesbuzz.biz). It requires that your git repository lives on the same server as your actual Publ installation.

On your webserver, create a private git repository wherever you want it, for example, `$HOME/sitefiles/example.com.git`; here is an example of how to do so (after logging into your server with `ssh`):

```bash
mkdir -p $HOME/sitefiles
git init --bare $HOME/sitefiles/example.com.git
cd
git clone $HOME/sitefiles/example.com.git example.com
```

Now you'll have a bare repository in `sitefiles/example.com.git` and an application directory in `example.com`.

Back on your desktop (or wherever you're developing your site), configure the bare repository as your publishing remote; for example:

```bash
git remote add publish username@servername:sitefiles/example.com.git
```

Now back on the server, you need two git hooks. First, the post-update hook on the bare repo, e.g. `$HOME/sitefiles/example.com.git/hooks/post-update`:

```bash
#!/bin/sh

echo "Deploying new site content..."

cd $HOME/example.com
unset GIT_DIR
git pull --no-ff
```

Next, the post-merge hook on the deployment repo, e.g. `$HOME/example.com/.git/hooks/post-merge`:

```bash
#!/bin/sh

if git diff --name-only HEAD@{1} | grep -q Pipfile.lock ; then
    echo "Pipfile.lock changed; redeploying"
    cd "$GIT_DIR/.."
    pipenv install
fi

echo "Restarting web services"
killall -HUP gunicorn
```


Now, when you push new content to the `publish` remote, it will go to the bare repo, which will then tell the deployment repo to pull the latest changes. After these changes are deployed, it will update whatever packages changed in your Pipfile, and then restart your gunicorn processes. (Yes, all of them. If you have multiple gunicorn sites you'll probably want to do something to track the process ID on a per-site basis.)

## Different-server deployment

If your git repository and site live on different servers, you need to get a bit fancier.

First, create a file called `deploy.sh` in your top-level site directory:

```bash
#!/bin/sh
# wrapper script to pull the latest site content and redeploy

cd  $(dirname $0)
git pull --ff-only || exit 1

if git diff --name-only HEAD@{1} | grep -q Pipfile.lock ; then
    echo "Pipfile.lock changed; redeploying"
    pipenv install || exit 1
fi

if [ "$1" != "nokill" ]; then
    echo "Restarting web services"
    killall -HUP gunicorn
fi

```

Then, in your `main.py`, add a function like this (changing the `/_deploymenthook` and `secret` to strings only you know); it should go somewhere between `app = publ.publ(...)` and `app.run(...)`:

```python
@app.route('/_deploymenthook', methods=['POST'])
def deploy():
    import threading

    if flask.request.form.get('secret') != os.environ.get('REDEPLOY_SECRET'):
        raise http_error.Forbidden()

    try:
        result = subprocess.check_output(
            ['./deploy.sh', 'nokill'],
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        logging.error("Deployment failed: %s", err.output)
        return flask.Response(err.output, status_code=500, mimetype='text/plain')

    def restart_server(pid):
        logging.info("Restarting")
        os.kill(pid, signal.SIGHUP)

    logging.info("Restarting server in 3 seconds...")
    threading.Timer(3, restart_server, args=[os.getpid()]).start()

    return flask.Response(result, mimetype='text/plain')
```

Then,  in whatever mechanism you use to run the website, set the environment variable `REDEPLOY_SECRET` to some secret string. For example, if you're using a `systemd` service, add a line like:

    Environment="REDEPLOY_SECRET=the secret password"

Deploy these changes to your website and restart it. Now you should be able to make your website re-deploy from git and restart itself with a command like:

```bash
curl -s https://example.com/_deploymenthook -d "secret=the secret password"
```

after changing `example.com`, `_deploymenthook`, `secret`, and `the secret password` as appropriate.

Finally, on your main git repository, create a `post-receive` hook which looks like this:

```bash
#!/bin/bash

DEPLOY=
while read oldrev newrev refname; do
    branch=$(git rev-parse --symbolic --abbrev-ref $refname)
    if [ "master" == "$branch" ]; then
        DEPLOY=1
    fi
done

if [ "$DEPLOY" ] ; then
    # send a deployment signal to the site
    curl -s https://example.com/_deploymenthook -d "secret=the secret password"
fi
```

again modifying the `curl` command as above.

Now when you push a change to the `master` branch of your repository, it should send a very basic signal to your website to tell it to run the `deploy.sh` script, which in turn will attempt to update the site from git. If this is successful, this hook will wait 3 seconds and then tell the controlling process to restart.

### GitHub web hooks

If you're hosting your site files on GitHub, you cannot make your own custom `post-receive` hook. Fortunately, they provide a built-in webhook mechanism which you can use to do the same thing as the above; go to your repository settings, then "Webhooks," then "Add webhook." On the new webhook, set your payload URL to your deployment hook (e.g. `http://example.com/_deploymenthook`), the content type to `application/x-www-form-urlencoded`, and the secret to some secret string.

Then in the `deploy` function, change the lines:

```python
    if flask.request.form.get('secret') != os.environ.get('REDEPLOY_SECRET'):
        raise http_error.Forbidden()
```

to:

```python
    ### [[[TODO: verify that this works! ]]]
    import hmac
    digest = hmac.new(os.environ.get('GITHUB_SECRET'), flask.request.get_data(), digestmod='sha1')
    if not hmac.compare_digest(digest.hexdigest(),
                               flask.request.headers.get('X-Hub-Signature')):
        raise http_error.Forbidden()
```

Finally, in whatever mechanism you use to run the website, set the value of the `GITHUB_SECRET` environment variable to match the secret string provided to GitHub.
