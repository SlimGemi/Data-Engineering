# pokemon_etl_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from Pokedex import get_pokemon_details, extract_pokemon_info, insert_pokemon_data, preprocess_data

default_args = {
    'owner': 'Ashley',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'pokemon_etl_dag',
    default_args=default_args,
    description='A comprehensive DAG for Pokémon ETL',
    schedule='@daily',
    catchup=False,
)

def fetch_pokemon_data(**kwargs):
    chosen_pokemon = kwargs['params']['chosen_pokemon']
    pokemon_details = get_pokemon_details(chosen_pokemon)
    return extract_pokemon_info(pokemon_details)

def preprocess_and_insert_data(**kwargs):
    pokemon_info = kwargs['task_instance'].xcom_pull(task_ids='fetch_pokemon_data_task')
    preprocessed_data = preprocess_data(pokemon_info)
    insert_pokemon_data(preprocessed_data)

fetch_pokemon_data_task = PythonOperator(
    task_id='fetch_pokemon_data_task',
    python_callable=fetch_pokemon_data,
    provide_context=True,
    params={'chosen_pokemon': 'charmander'},
    dag=dag,
)

preprocess_and_insert_data_task = PythonOperator(
    task_id='preprocess_and_insert_data_task',
    python_callable=preprocess_and_insert_data,
    provide_context=True,
    dag=dag,
)

fetch_pokemon_data_task >> preprocess_and_insert_data_task

if __name__ == "__main__":
    dag.cli()
