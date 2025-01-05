from airflow import DAG
# from airflow.providers.http.operators.http import SimpleHttpOperator
import airflow.providers.http.operators.http as hx
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'simple_http_dag',
    default_args=default_args,
    description='A simple DAG using SimpleHttpOperator',
    schedule_interval=timedelta(days=1),
)

# get_weather = SimpleHttpOperator(
#     task_id='get_weather',
#     http_conn_id='weather_api',
#     endpoint='/data/2.5/weather',
#     method='GET',
#     data={"q": "Dallas", "appid": "your_api_key"},
#     headers={"Content-Type": "application/json"},
#     dag=dag,
# )

# get_weather

extract_user = hx.HttpOperator(
    task_id="extract_user",
    http_conn_id="user_api",
    endpoint="api/",
    method="GET",
    response_filter=lambda response: json.loads(response.text),
    log_response=True,
    dag=dag,
)

extract_user