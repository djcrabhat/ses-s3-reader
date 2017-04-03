ses-s3-inbox
=====

Sometimes, you just wanna pump some emails from SES to S3.  But what good is a pile of MIME files?
This webapp helps make reading that pile a little easier.

Purpose
-----
So you've got a shiny new domain, and you want a lightweight mail box.  So you think, "Ah!  SES Receipt Rules!"  

SES Setup
-----
First, you'll need an S3 bucket for these emails to be written to.  You'll also need to [give SES permission to write to your bucket](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-permissions.html)

Next, set up SES with a Receipt Rule that will trigger an S3 Action.  I'd suggest using an object_prefix to keep your bucket organized.

[Getting Started Receiving Email with Amazon SES](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-getting-started.html)

[S3 Action Docs](http://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-s3.html)

Running
-----
```
export FLASK_APP=app.py
flask run
```
or, if you're debugging or something, it can be invoked as a script at
```
python server.py
```

Docker
-----
Checkout the repo, then
```
docker build -t ses-s3-reader .
```

To run:
```
docker run --rm -ti -p 5000:5000 -e BUCKET=MY_BUCKET -e OBJECT_PREFIX=email/ ses-s3-reader

```

Current Limitations:
-----
* The To, From, Date data on the Inbox page doesn't fill until you look at a message.
  * TODO: Have some sorta background job fetch message metadata in the background
* No message meta-data is persisted after a restart
* There should probably be a cacheing layer to save calls to S3
* The MIME parsing is pretty bare-bones, wouldn't be suprised if it chokes


Screenshots
-----

![Message Screenshot](/docs/email.png?raw=true)
