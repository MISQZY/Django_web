FROM python:3.13-slim
SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash django && chmod 777 /opt /run

WORKDIR /django

RUN mkdir /django/static && mkdir /django/media && chown -R django:django /django && chmod 755 /django

COPY --chown=django:django . .

RUN pip install -r requirements.txt

USER django

CMD ["python","manage.py","runserver","0.0.0.0:8000"]