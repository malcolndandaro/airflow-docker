from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG(
	dag_id = 'teste2',
	start_date = datetime(2020,12,27),
	schedule_interval = '*/2 * * * *')

def print_hello():
	return "hello!"

def print_goodbye():
	return "goodbye!"

print_hello = PythonOperator(
	task_id = 'print_hello',
	#python_callable param points to the function you want to run 
	python_callable = print_hello,
	#dag param points to the DAG that this task is a part of
	dag = dag)

print_goodbye = PythonOperator(
	task_id = 'print_goodbye',
	python_callable = print_goodbye,
	dag = dag)

#Assign the order of the tasks in our DAG
print_hello >> print_goodbye