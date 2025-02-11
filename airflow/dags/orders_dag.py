from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

sys.path.append('/home/tigureis/DNC_engenharia_de_dados/DncInsight_Solution/airflow/dags/app')

from app.organizer import bronze_protocol, silver_protocol, gold_protocol

default_args = {
    'owner': 'tigureis',
    'retries': 5,
    'retry_delay': timedelta(seconds=5)
}

#set the dag identification, the rum interval, the number of retries and the interval betwen retries
with DAG(
    dag_id='order_dag',
    default_args=default_args,
    description='order data pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

#Set the tasks
 
    task_1 = PythonOperator(
        task_id="bronze_protocol",
        python_callable = bronze_protocol,
        dag=dag,)

    task_2 = PythonOperator(
        task_id='silver_protocol',
        python_callable=silver_protocol,
        dag=dag,)
    
    task_3 = PythonOperator(
        task_id='gold_protocol',
        python_callable=gold_protocol,
        dag=dag,)


#  Set the tasks order
task_1 >> task_2 >> task_3