FROM mysql:5.7

ENV MYSQL_DATABASE=orders_test \
    MYSQL_ROOT_PASSWORD=testSQL

ADD orders_test.sql /docker-entrypoint-initdb.d

EXPOSE 3306



