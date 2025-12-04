#!/bin/bash

# 連到 MySQL，對 data 這個資料庫執行建表
mysql -P 3306 -u user -p data < src/001_create_tables.sql

# 再執行插入假資料
mysql -P 3306 -u user -p data < src/002_insert_sample_data.sql
