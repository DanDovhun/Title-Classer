# pull official base image
FROM python:3.11

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install dependencies
# install spacy dependencies
COPY db.sqlite3 db.sqlite3
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev 

RUN pip install --upgrade pip
RUN python -m pip install tensorflow
RUN pip install -U pip setuptools wheel
RUN pip install seaborn
RUN pip install whitenoise
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN pip install dj-database-url

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser --disabled-password user

RUN chown user:user /app/db.sqlite3
RUN chmod 755 /app/db.sqlite3

USER user