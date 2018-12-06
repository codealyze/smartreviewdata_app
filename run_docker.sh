#!/bin/bash
docker run --name sqldocker -p 8001:3306 -e MYSQL_ROOT_PASSWORD=root \
   -v "$(pwd)"/sqldata:/sqldata2 -d mysql/mysql-server:latest

sleep 20

#Give permissions and init
docker exec sqldocker sh -c "mysql -u root -proot < /sqldata2/sqlscript --verbose"
docker exec sqldocker sh -c "echo 'max_allowed_packet=1024M' >> etc/my.cnf"
#Load data into sql 
#docker exec sqldocker sh -c \
#  "mysql -u root -proot smartreview < /sqldata2/`ls sqldata/*sql -t1 | head -n 1 | cut -d "/" -f 2`"
