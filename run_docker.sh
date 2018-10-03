#!/bin/bash
docker run --name sqldocker -p 8001:3306 -e MYSQL_ROOT_PASSWORD=root \
   -v "$(pwd)"/sqldata:/sqldata2 -d mysql/mysql-server:sept_update

sleep 20

#Give permissions and init
docker exec sqldocker sh -c "mysql -u root -proot < /sqldata2/sqlscript --verbose"

#Load data into sql 
docker exec sqldocker sh -c "mysql -u root -proot smartreview < /sqldata2/smartreview.sql --verbose"
