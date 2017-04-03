from flask import Flask, jsonify, render_template, request, Response
import boto3
import os
import StringIO
import email

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False




class CacheLayer:
    '''
    TODO: Persist this data somewhere
    TODO: Could probably fill this data in during a background job
    '''
    def __init__(self):
        self.cache = {}

    def __getitem__(self, key):
        return self.cache.get(key)

    def __setitem__(self, key, value):
        self.cache[key] = {
            "to": value['to'],
            "from": value['from'],
            "date": value['date'],
            "is_multipart": value.is_multipart()
        }

    def clear(self):
        self.cache = {}

    def num_items(self):
        return len(self.cache)

class EmailReader:
    def __init__(self, config):
        self.s3 = s3 = boto3.resource('s3')
        self.cache = CacheLayer()

        if 'BUCKET' in config:
            self.bucket = self.s3.Bucket(config['BUCKET'])
            self.prefix = config.get('OBJECT_PREFIX')
        else:
            raise ValueError("Must set a BUCKET config value")

    def email_summary(self, x, prefix):
        data = {
            "key": x.key,
            "nice_key": x.key[len(prefix):] if prefix else x.key
        }
        cache = self.cache[x.key]
        if cache:
            data.update(cache)
        return data

    def get_email_list(self, StartingToken=None):
        kwargs = {}

        if self.prefix:
            kwargs["Prefix"]=self.prefix
        # if StartingToken:
        #     kwargs["StartingToken"] =StartingToken

        if kwargs:
            ret = [self.email_summary(x, self.prefix) for x in self.bucket.objects.filter(**kwargs)]
        else:
            ret = [self.email_summary(x, self.prefix) for x in self.bucket.objects.all()]

        return ret

    def get_email(self, key):
        # TODO: build cacheing in here
        output = StringIO.StringIO()
        object = self.bucket.download_fileobj(key, output)
        output.seek(0)

        z = email.message_from_file(output)
        self.cache[key] = z


        return z



def create_app(config_path=None):
    app = Flask(__name__)

    # load config from file

    if config_path and HAS_YAML:
        app.logger.debug("loading %s"%config_path)
        path = os.path.join(os.getcwd(), config_path)
        if os.path.exists(path):
            with open(path) as f:
                c = yaml.load(f)
        if c:
            app.config.update(c)

    # env variable overrides
    for x in ["BUCKET", "OBJECT_PREFIX"]:
        if x in os.environ:
            app.config[x] = os.environ[x]


    app.email_reader = EmailReader(app.config)

    @app.route('/')
    def hello_world():
        return render_template('index.html')

    @app.route('/list')
    def list():
        emails = app.email_reader.get_email_list()
        return render_template('list.html', emails=emails)

    @app.route('/email')
    def email():
        key = request.args.get('key')
        email = app.email_reader.get_email(key)
        if email.is_multipart():
            return render_template('email_multi.html', email=email, key=key)
        else:
            return render_template('email.html', email=email, key=key)

    @app.route('/email/<int:num>')
    def email_part(num):
        key = request.args.get('key')
        email = app.email_reader.get_email(key)
        if email.is_multipart():
            msg = email.get_payload(num)
            return Response(msg.get_payload(decode=True), mimetype=msg.get_content_type())
        else:
            return Response(email.get_payload(decode=True), mimetype=email.get_content_type())





    def get_settings():
        return {
            "bucket": app.config['BUCKET'],
            "prefix": app.config.get('OBJECT_PREFIX'),
            "items_in_cache": app.email_reader.cache.num_items()
        }

    @app.route('/settings')
    def settings():
        x = get_settings()
        return render_template('settings.html', settings=x)

    @app.route('/settings/cache/clear', methods=['POST'])
    def settings_clear_cache():
        x = get_settings()
        app.email_reader.cache.clear()
        return render_template('settings.html', settings=x, message="Cached Cleared!")


    return app
