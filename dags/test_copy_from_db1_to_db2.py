
import datetime

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator
DAG_ID = "test_copy_from_db1_to_db2"

def copy_data_from_db1_to_db2():
    """
    Assume that table exists in source and target databases. Transfer content
    from source to target table overwriting everything in target.
    """
    table = "test"
    tmp_filename = "tmpfile"
    source_hook = PostgresHook(postgres_conn_id="db1")
    target_hook = PostgresHook(postgres_conn_id="db2")

    source_hook.bulk_dump(f"{table}", f"{tmp_filename}")

    sql_stmt = f"TRUNCATE TABLE {table};"
    target_conn = target_hook.get_conn()
    target_cursor = target_conn.cursor()
    target_cursor.execute(sql_stmt)
    target_conn.commit()
    target_cursor.close()
    target_conn.close()

    target_hook.bulk_load(f"{table}", f"{tmp_filename}")

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2022, 2, 2),
    schedule_interval="*/10 * * * *", # every 10 minutes (cron syntax)
    #schedule="@once",
    catchup=False,
) as dag:

    copy_data_from_db1_to_db2 = PythonOperator(
        task_id="transfer_data",
        python_callable=copy_data_from_db1_to_db2,
    )
