from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

@dag(
    "hello_world",
    default_args={
        "owner": "Ibinaldo",
        "depends_on_past": False,
        "email": "ibi.best@gmail.com",
        "email_on_failure": True,
        "email_on_retry": False,
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
        "start_date": datetime(2023,7,23)
    },
    description="DAG to validate git sync",
    schedule_interval="@daily"

)

def hello_world_dag():

    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",

    )

    t1

dag = hello_world_dag()