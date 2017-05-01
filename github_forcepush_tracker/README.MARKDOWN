# Github Force Push Tracker

#### This is a simple web.py Github webhook server to track commits overriden by force pushes to Github branches.


## Why is this needed?
Git stores the changes to [refs](https://git-scm.com/book/en/v2/Git-Internals-Git-References) in the [reflog](https://git-scm.com/docs/git-reflog), so even when a branch is overriden, you can get the old branch back. Github, however does not expose the reflog. So if someone else overrides the branch or if you loose the local reflog, there is no easy way to recover the overriden ref.

## What does it do exactly?
The server is an endpoint to receive [Github Webhook Events](https://developer.github.com/webhooks/) push events.

When setup properly on Github, any time someone pushes to Github, this server will receive an event.

This server then parses the event, and saves any force push events by [ref name](https://git-scm.com/book/en/v2/Git-Internals-Git-References) so that you can look them up by ref or branch name later. The endpoints provided allow you to request details on any force pushes to a ref/branch so you can easily recover from an accidental override by another user.


## How do I set this up?

todo: improve once this is on pypi
**TL;DR**

  1. First you need to setup this server on some machine and expose it to the internet/whatever IP's you want to access it. I'd recommend spinning up an EC2 Linux box. Then:
      * (optional) create and activate a virtualenv
      * install the python requirements, `pip install -r requirements.txt`
      * run the server with `python main.py`
      * (optional) add venv activation and running this server to your system startup script/ bashrc file.
  2. Setup the webhook on Github. You'll want to use `<path_to_your_webserver>:<port>/github_hook`. Here are some good guides on where to add it on Github:
      * https://developer.github.com/webhooks/creating/#setting-up-a-webhook
      * https://support.hockeyapp.net/kb/third-party-bug-trackers-services-and-webhooks/how-to-set-up-a-webhook-in-github#in-github-1
  3. (Optional, but recommended) Setup a shared secret token to validate that calls are actually coming from your gitub webserver.

## Security

Todo talk about: not much data exposed via api, only author guhub username and commit ahshes, and there is no sensitive information in commit hashes.

Using github secret to validate the request using the signature.



## What are the endpoints?
todo

## Limitations
Currently only support one repo per server. To support multiple repos on one server, minor changes to the endpoints are required.

Currently webhook server ping is not supported.
