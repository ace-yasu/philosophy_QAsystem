FROM postgres:latest

ENV TZ=Asia/Tokyo

RUN apt-get update&&apt-get install -y\
    git\
    build-essential \
    postgresql-server-dev-all \
    && git clone https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector \
    && make \
    && make install \
    && rm -rf /tmp/pgvector

COPY ./init/ /docker-entrypoint-initdb.d/