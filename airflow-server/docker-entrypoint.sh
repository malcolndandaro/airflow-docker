#!/bin/bash
set -m 
airflow db init
airflow users create --username admin --password admin --role Admin --email placeholder@gmail.com --firstname admin --lastname admin
airflow webserver --port 8080 &
airflow scheduler
fg %3
