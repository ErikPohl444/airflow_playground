from airflow import DAG
from datetime import datetime
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.http.sensors.http import HttpSensor
import airflow.providers.http.operators.http as hx
import json
from airflow.operators.python import PythonOperator
from pandas import json_normalize
from airflow.providers.postgres.hooks.postgres import PostgresHook
import sys
import os


def _process_user(ti):
    user = ti.xcom_pull(task_ids="extract_user")
    user = user["results"][0]
    processed_user = json_normalize(
        {
            "firstname": user["name"]["first"],
            "lastname": user["name"]["last"],
            "country": user["location"]["country"],
            "username": user["login"]["username"],
            "password": user["login"]["password"],
            "email": user["email"],
        }
    )
    print(processed_user)
    path = "/tmp/processed_user.csv"
    processed_user.to_csv(path, index=False, header=False)
    if os.path.exists(path):
        print("File exists!")
    else:
        print("File does not exist.")


def _store_user():
    hook = PostgresHook(postgres_conn_id="postgres")
    path = "/tmp/processed_user.csv"
    if os.path.exists(path):
        print("File exists!")
        with open(path, "rt") as fhandle:
            for line in fhandle:
                print(line)
    else:
        print("File does not exist.")
    """
     hook.copy_expert(
            sql=f"COPY users FROM '{path}' WITH DELIMITER as ','",
            filename='/tmp/processed_user.csv'
     ) 
     """
    hook.copy_expert(
        sql=f"COPY users FROM stdin WITH DELIMITER as ','",
        filename="/tmp/processed_user.csv",
    )


with DAG(
    "user_processing2_vsc",
    start_date=datetime(2022, 11, 12),
    schedule_interval="*/1 * * * *",
    catchup=False,
) as dag:

    print("setup is create_table task")
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres",
        sql="""
                CREATE TABLE IF NOT EXISTS users (
                firstname TEXT PRIMARY KEY,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL);
                """,
    )
    print("done")

    print("setup is api available? task")
    is_api_available = HttpSensor(
        task_id="is_api_available", http_conn_id="user_api", endpoint="api/"
    )
    print("done")

    print("setup extract_user task")
    extract_user = hx.HttpOperator(
        task_id="extract_user",
        http_conn_id="user_api",
        endpoint="api/",
        method="GET",
        response_filter=lambda response: json.loads(response.text),
        log_response=True,
    )
    print("done")

    print("setup process user task")
    process_user = PythonOperator(task_id="process_user", python_callable=_process_user)
    print("done")

    print("setup process user task")
    store_user = PythonOperator(task_id="store_user", python_callable=_store_user)
    print("done")

    print("setup task dependencies")
    create_table >> is_api_available >> extract_user >> process_user >> store_user
    print("done")
