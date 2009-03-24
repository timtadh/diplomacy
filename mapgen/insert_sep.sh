#!/bin/sh

# the following should be in:
# . config.sh

DB_UNAME="root"
DB_PASS="gurkan12"
DB_HOST="localhost" 
DB_NAME="seperation"
CONN_STR="--user=$DB_UNAME --password=$DB_PASS -h $DB_HOST"

$num = '100'

echo "# inserting seperations"


echo "# create uniprot db if it doesn't exist"
mysql $CONN_STR -e "create database if not exists seperation;"

mysql $DB_NAME $CONN_STR -e "drop table if exists sep_" + $num


echo "# create table"

mysql $DB_NAME $CONN_STR -e "CREATE TABLE IF NOT EXISTS sep_100 (a int(11), b int(11), sep int(11), CONSTRAINT pk_ab PRIMARY KEY (a, b));"


echo "#import Data"
mysql $DB_NAME $CONN_STR -e "truncate table sep_" + $num;

# TIM: just add refseq to the columns (in the right order)
mysqlimport $DB_NAME $CONN_STR --ignore-lines=1  --local --delete --fields-terminated-by=', ' --fields-escaped-by='\\'  --lines-terminated-by='\n' --columns='a, b, sep' sep_100
