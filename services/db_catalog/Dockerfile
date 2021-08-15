FROM mysql:5.7

ENV MYSQL_DATABASE=catalog_test \
    MYSQL_ROOT_PASSWORD=testSQL

ADD catalog_test.sql /docker-entrypoint-initdb.d

EXPOSE 3306