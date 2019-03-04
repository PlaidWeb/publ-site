Title: Continuous deployment with git
Date: 2018-12-16 23:23:07-08:00
Entry-ID: 441
UUID: b023c99e-0f41-51ea-9d41-5e575b37339d

How to use git hooks to automatically deploy site content

.....

This is the approach I use for managing my site content on [my main website](http://beesbuzz.biz).

## Initial setup

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
git pull
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

## Deploying changes

Now, when you push new content to the `publish` remote, it will go to the bare repo, which will then tell the deployment repo to pull the latest changes. After these changes are deployed, it will update whatever packages changed in your Pipfile, and then restart your gunicorn processes. (Yes, all of them. If you have multiple gunicorn sites you'll probably want to do something to track the process ID on a per-site basis.)

