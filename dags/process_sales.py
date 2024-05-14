from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import requests


def fn_requestor(port, rep_date):
    if port == '8081':
        json_body={
                "date": rep_date,
                "raw_dir": 'raw/sales/' + rep_date
            }
    elif port == '8082':
        json_body={
            "raw_dir": 'raw/sales/' + rep_date,
            "stg_dir": 'stg/sales/' + rep_date
        }
    else:
        json_body={}

    resp = requests.post(
        url=f'http://host.docker.internal:{port}/',
        json=json_body
    )

    return resp.status_code


def run_job1():
    resp = fn_requestor('8081', '2022-08-11')


def run_job2():
    resp = fn_requestor('8082', '2022-08-11')





# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['ostapenko.vctr@gmail.com'],
    'start_date': datetime(2024, 5, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': 5,
}

# Define DAG
dag = DAG(
    dag_id='process_sales',
    start_date=datetime(2024, 5, 13),
    default_args=default_args,
    schedule_interval=None, # "0 0 1 * *",
    max_active_runs=1,
)

extract_data_from_api = PythonOperator(
    task_id='extract_data_from_api',
    dag=dag,
    python_callable=run_job1,
)

convert_to_avro = PythonOperator(
    task_id='convert_to_avro',
    dag=dag,
    python_callable=run_job2
)

extract_data_from_api >> convert_to_avro