FROM python:2.7-onbuild

VOLUME ["/etc/ses-se-reader/"]

ENV READER_CONFIG_PATH "/etc/ses-se-reader/config.yaml"
ENV FLASK_APP "app.py"

# TODO: move this to a nicer uwsgi container
ENTRYPOINT [ "flask", "run" ]
CMD ["--host=0.0.0.0"]