ses-s3-inbox
=====

![Message Screenshot](/docs/email.png?raw=true)


Sometimes, you just wanna pump some emails from SES to S3.  But what good is a pile of MIME files?
This webapp helps make reading that pile a little easier

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