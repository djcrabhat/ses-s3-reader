ses-s3-inbox
=====

Sometimes, you just wanna pump some emails from SES to S3.  But what good is a pile of MIME files?
This webapp helps make reading that pile a little easier

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