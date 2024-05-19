from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['ostapenko.vctr@gmail.com'],
    'start_date': datetime(2024, 4, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': 5,
}

# Define DAG
dag = DAG(
    dag_id='first_dag',
    start_date=datetime(2024, 4, 13),
    default_args=default_args,
    schedule_interval="0 5 * * *",
    description='A simple DAG to run a Python script',
)

# Define Python function to be executed
def print_hello():
    print("Hello Airflow! Task completed!")

# Define tasks
task_hello = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag,
)

empty_task = DummyOperator(
    task_id='empty_task',
    dag=dag,
)

# Task dependencies
# task_hello
