from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from extract_utils import get_current_weather
from airflow.models import Variable

KEYWORDS = Variable.get('SCRAPE_KEYWORDS_1').split(",")
SITE = Variable.get('SCRAPE_SITE_1')
EP = Variable.get('API_EP_OOB')

default_args = {
    "start_date":datetime(2023, 8, 11),
    "retries":1,
    "retry_delay":timedelta(minutes=5)
}

with DAG('dag_weather', schedule_interval='0/15 * * * *', default_args=default_args, catchup=False, tags=['weather']) as dag:

    retrieve_data = PythonOperator(
        task_id = 'task_id_1',
        python_callable = process_main,
        op_args = [EP, SITE, KEYWORDS]
    )
