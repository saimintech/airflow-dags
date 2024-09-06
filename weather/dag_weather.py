from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from weather_utils import get_current_weather
from airflow.models import Variable

WEATHER_API = Variable.get('WEATHER_API_KEY_SECRET')


default_args = {
    "start_date":datetime(2023, 8, 11),
    "retries":10,
    "retry_delay":timedelta(minutes=15)
}

with DAG('dag_weather', schedule_interval='59 16 * * *', default_args=default_args, catchup=False, tags=['weather']) as dag:

    retrieve_data = PythonOperator(
        task_id = 'task_id_1',
        python_callable = get_current_weather,
        op_args = [WEATHER_API]
    )
