from ses_s3_inbox import create_app
from os import environ

config_path = environ.get("READER_CONFIG_PATH", "config.yaml")
app = create_app(config_path=config_path)
