FROM python:3.11.3-alpine3.16
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ARG COUCHDB_DOMAIN
ENV COUCHDB_DOMAIN $COUCHDB_DOMAIN
ARG COUCHDB_USER
ENV COUCHDB_USER $COUCHDB_USER
ARG COUCHDB_PASSWORD
ENV COUCHDB_PASSWORD $COUCHDB_PASSWORD
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]