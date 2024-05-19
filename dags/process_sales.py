from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import requests


def run_job1(dt):
    print(dt)
    json_body={
            "date": dt,
            "raw_dir": 'raw/sales/' + dt
        }
    
    resp = requests.post(
        url=f'http://host.docker.internal:8081/',
        json=json_body
    )

    print(f'Job_2 done! Response code: {resp.status_code}.')


def run_job2(dt):
    json_body={
            "raw_dir": 'raw/sales/' + dt,
            "stg_dir": 'stg/sales/' + dt
        }
    
    resp = requests.post(
        url=f'http://host.docker.internal:8082/',
        json=json_body
    )

    print(f'Job_2 done! Response code: {resp.status_code}.')





# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['ostapenko.vctr@gmail.com'],
    # 'start_date': datetime(2022, 8, 9),
    # 'end_date': datetime(2024, 8, 11),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': 5,
}

# Define DAG
dag = DAG(
    dag_id='process_sales',
    start_date=datetime(2022, 8, 9),
    end_date=datetime(2022, 8, 12),
    default_args=default_args,
    schedule_interval="0 1 * * *",
    max_active_runs=1,
    catchup=True,
)

extract_data_from_api = PythonOperator(
    task_id='extract_data_from_api',
    dag=dag,
    python_callable=run_job1,
    op_args=['{{ds}}'],
    provide_context=True,
)

convert_to_avro = PythonOperator(
    task_id='convert_to_avro',
    dag=dag,
    python_callable=run_job2,
    op_args=['{{ds}}'],
    provide_context=True
)

extract_data_from_api >> convert_to_avro