# git_webhooks


## Overridden commit webhook
This is a simple web.py Github webhook server to track commits overriden by force pushes to Github branches.

## Why is this needed?
Git stores the changes to refs in the reflog, so even when a branch is overriden, you can get the old branch back. Github, however does not expose the reflog. So if someone else overrides the branch or if you loose the local reflog, there is no easy way to recover the overriden ref.

What does it do exactly?
The server is an endpoint to receive Github Webhook Events push events.

When setup properly on Github, any time someone pushes to Github, this server will receive an event.

This server then parses the event, and saves any force push events by ref name so that you can look them up by ref or branch name later. The endpoints provided allow you to request details on any force pushes to a ref/branch so you can easily recover from an accidental override by another user.
