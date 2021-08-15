FROM mysql:5.7

ENV MYSQL_DATABASE=clients_test \
    MYSQL_ROOT_PASSWORD=testSQL

ADD clients_test.sql /docker-entrypoint-initdb.d

EXPOSE 3306



