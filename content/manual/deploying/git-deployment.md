Title: Continuous deployment with git
Date: 2018-12-16 23:23:07-08:00
Entry-ID: 441
Sort-Title: 200
UUID: b023c99e-0f41-51ea-9d41-5e575b37339d

How to use git hooks to automatically deploy site content

.....

It's pretty common to use git to host your website files. There are a few different ways that you can use git itself to automate the deployment of site updates, depending on the specifics of your git hosting situation. The below methods should cover the vast majority of git-based workflows, at least if you're [self-hosting Publ](self-hosting.md).

## Deployment script

Regardless of your actual git hosting situation, you will need a deployment script, which does a `git pull` and updates package versions if the `poetry.lock` has changed. Save this file as `deploy.sh` in your website repository, and make sure it's set executable:

```bash
#!/bin/sh
# wrapper script to pull the latest site content and redeploy

cd  $(dirname $0)

# see where in the history we are now
PREV=$(git rev-parse --short HEAD)

git pull --ff-only || exit 1

if git diff --name-only $PREV | grep -qE '^(templates/|app\.py)' ; then
    echo "Configuration or template change detected"
    disposition=reload-or-restart
fi

if git diff --name-only $PREV | grep -q poetry.lock ; then
    echo "poetry.lock changed"
    poetry install || exit 1
    disposition=restart
fi

if [ "$1" != "nokill" ] && [ ! -z "$disposition" ] ; then
    # insert server restart command here (see note), e.g.
    # systemctl --user $disposition SERVICE-NAME.service
fi
```

The remainder of the deployment process depends on how you're actually hosting your git repository.

## Self-hosted git repository

### Repository on same server as the website

For this example, we will keep the main git repository in `$HOME/sitefiles/example.com.git` and the deployment directory in `$HOME/example.com`.

On your webserver, create a private bare git repository wherever you want it; for example, on the server, run:

```bash
# change this!
SITENAME=example.com

# create the bare repository
mkdir -p $HOME/sitefiles
git init --bare $HOME/sitefiles/$SITENAME.git

# add the post-update hook
cat > $HOME/sitefiles/$SITENAME.git/hooks/post-update << EOF
#!/bin/sh

echo "Deploying new site content..."

cd \$HOME/$SITENAME
unset GIT_DIR
if [ ! -x ./deploy.sh ] ; then
    echo "Deployment script not available or not executable" 1>&2
    exit 1
fi
./deploy.sh || echo "Deployment script failed"
EOF
chmod u+x $HOME/sitefiles/$SITENAME.git/hooks/post-update

# set up the live/deployment workspace
cd $HOME
git clone $HOME/sitefiles/$SITENAME.git
# optional: make this repository share the raw objects (to save some disk space)
# see https://git.wiki.kernel.org/index.php/Git_FAQ#How_to_share_objects_between_existing_repositories.3F
cd $SITENAME
echo "$HOME/sitefiles/$SITENAME.git/objects/" > .git/objects/info/alternates
git gc
```

Now you'll have a bare repository in `$HOME/sitefiles/example.com.git` and a live deployment workspace in `$HOME/example.com`, and pushing to the bare repository will run the deployment script in the live workspace, if it exists.

On your local repository (i.e. where you're actually working on your site) add the bare repository as your remote:

```bash
git remote add origin user@server.example.com:sitefiles/example.com.git
git push -u origin master
```

This should push all of your content into the bare repository; however, since the live workspace won't yet have `deploy.sh` you'll need to do one `git pull` manually. After this, every push to the bare repository should automatically run your deployment script.

### Separate servers using an `ssh` key

If you keep your git repository on a separate server from where it's deployed to, set up an [ssh key](https://www.ssh.com/ssh/key/) or other authentication mechanism other than password so that you can do passwordless ssh from the repository server to the deployment server, and then add this as a `post-update` hook on the repository:

```bash
#!/bin/sh

echo "Deploying new site content..."

ssh DEPLOYMENT_SERVER 'cd example.com && ./deploy.sh'
```

replacing `DEPLOYMENT_SERVER` with the actual server name, and `example.com` with the directory that contains the site deployment.


## Simple webhook deployment

If you don't have the ability to run arbitrary `post-update` hooks but do have some sort of webhook functionality, you can add a webhook to your Publ site to run `deploy.sh`; for example, you can add this to your `app.py`:

```python
@app.route('/_deploy', methods=['POST'])
def deploy():
    import threading
    import signal
    import subprocess
    import flask

    if flask.request.form.get('secret') != os.environ.get('REDEPLOY_SECRET'):
        return flask.abort(403)

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

Then, in whatever mechanism you use to run the website, set the environment variable `REDEPLOY_SECRET` to some secret string. For example, if you're using a `systemd` service, add a line like:

    Environment="REDEPLOY_SECRET=the secret password"

Deploy these changes to your website and restart it. Now you can configure a webhook on your git repository that sends a POST request to the `/_deploy` route with the `secret` parameter set to your `REDEPLOY_SECRET` key.

## GitHub-style web hooks

If you're using GitHub (or something GitHub-compatible) to host your site files, there is a more secure way to run a webhook.

First, install the [flask-hookserver](https://pypi.org/project/flask-hookserver) package into your environment (with e.g. `poetry install flask-hookserver`).

Next, add the following to your `app.py` somewhere after the `app` object gets created:

```python
from flask_hookserver import Hooks

app.config['GITHUB_WEBHOOKS_KEY'] = os.environ.get('GITHUB_SECRET')
app.config['VALIDATE_IP'] = False

hooks=Hooks(app, url='/_gh')

@hooks.hook('push')
def deploy(data, delivery):
    import threading
    import signal
    import subprocess
    import flask

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

Now, set up your deployment to have an environment variable called `GITHUB_SECRET` set to some random, unguessable string. Do a manual redeployment.

Finally, go to your GitHub repository settings, then "Webhooks," then "Add webhook." On the new webhook, set your payload URL to your deployment hook (e.g. `http://example.com/_gh`), the content type to `application/x-www-form-urlencoded`, and the secret to the value of your `GITHUB_SECRET` string. It should look something like this:

![Configuration settings for the GitHub webhooks{scale=2}](github-webhook-setup.png)

Anyway, once you have it set up, every time you commit to GitHub, your site should automatically pull and redeploy the latest changes.

An example of this in action can be seen at the [files for this site](/github-site); in particular, see the [`app.py`](https://github.com/PlaidWeb/publ-site/blob/master/app.py) and [`deploy.sh`](https://github.com/PlaidWeb/publ-site/blob/master/deploy.sh) files.

## Troubleshooting

### Site doesn't update, or "updates rejected"

This is usually a sign that something changed on your deployment repository that's causing a git conflict. `ssh` into your live workspace and do a `git pull` to see what's going on. Chances are there was a change on your live repository that's causing an update conflict, for example you checked in an entry which didn't yet have an assigned `Entry-ID` or the like.

Generally you can fix this by going into your live repository and doing `git status` to see what's changed, and a command like `git checkout . && git pull` or `git reset --hard origin/master` will sort everything out (but be sure not to lose any changes you meant to make directly on the server).

### Webhook is timing out

If your packages change, the webhook will likely time out while `poetry install` runs. This should be okay, but try `ssh`ing into your live workspace and running `./deploy.sh` manually.
