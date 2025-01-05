from airflow import DAG
from datetime import datetime
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.operators.python import PythonOperator
from pandas import json_normalize

def _process_user(ti):
        user = ti.xcom_pull(task_ids="extract_user")
        user = user['results'][0]
        processed_user = json_normalize({
                'firstname': user['name']['first'],
                'lastname': user['name']['last'],
                'country': user['location']['country'],
                'username': user['login']['username'],
                'password': user['login']['password'],
                'email': user['email']
        })
        processed_user.to_csv('/tmp/processed_user.csv')
        

with DAG("user_processing_vsc",
         start_date= datetime(2022, 11, 12), 
         schedule_interval="*/5 * * * *", 
         catchup=False) as dag:
        create_table = SQLExecuteQueryOperator(
                task_id="create_tablex",
                conn_id="postgres",
                sql="""
                CREATE TABLE IF NOT EXISTS users (
                firstname TEXT PRIMARY KEY,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL);
                """
        )
    