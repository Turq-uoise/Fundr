ARG PYTHON_VERSION=3.9-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code


WORKDIR /code/

COPY . /code/

COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

ENV SECRET_KEY "8BhFgqrbhOjSWbLJOrucOmk61VUnjFJslqp31IB7lHuO278bYQ"
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "fundr.wsgi"]
