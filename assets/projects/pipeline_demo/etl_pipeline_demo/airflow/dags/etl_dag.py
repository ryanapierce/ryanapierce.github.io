from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from api_extraction.extract import fetch_yahoo_data, load_data_to_firebase
from transformation.transform import process_data
from database.load_data import load_to_db

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_data_dynamic(**kwargs):
    """Wrapper function to fetch data dynamically based on user input from Airflow UI."""
    symbols = kwargs.get('dag_run').conf.get('symbols', ["AAPL", "GOOGL", "MSFT"])
    fetch_yahoo_data(symbols)

dag = DAG(
    'yahoo_finance_etl',
    default_args=default_args,
    description='ETL pipeline from Yahoo Finance API to SQL database and Firebase',
    schedule_interval=timedelta(days=1),
)

# Define tasks with appropriate function calls
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=fetch_data_dynamic,
    provide_context=True,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=process_data,
    dag=dag,
)

load_to_db_task = PythonOperator(
    task_id='load_data_to_db',
    python_callable=load_to_db,
    dag=dag,
)

load_to_firebase_task = PythonOperator(
    task_id='load_data_to_firebase',
    python_callable=load_data_to_firebase,
    op_kwargs={'symbols': ["AAPL", "GOOGL", "MSFT"]},  # Add more symbols as needed
    dag=dag,
)

# Set task execution order
extract_task >> transform_task >> load_to_db_task >> load_to_firebase_task