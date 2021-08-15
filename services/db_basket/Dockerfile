FROM mysql

ENV MYSQL_DATABASE=basket_test \
    MYSQL_ROOT_PASSWORD=testSQL

ADD basket_test.sql /docker-entrypoint-initdb.d

EXPOSE 3306



