from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

# Define a simple DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

with DAG(
    dag_id='test-kube-pod-dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # Kubernetes Pod Operator Task
    kubernetes_task = KubernetesPodOperator(
        image='deposit-job:latest',
        # cmds=["python", "-c"],
        task_id="deposit-task",
        # arguments=["print('Hello from Airflow Kubernetes Pod Operator!')"],
        get_logs=True,
        in_cluster=True,

        # cluster_context='docker-desktop',  # Specify your local Kubernetes context
        # config_file='/home/airflow/.kube/config',  # Path inside the Docker container

        # wait_until_job_complete=True,

        image_pull_policy="IfNotPresent",

        on_finish_action='delete_succeeded_pod'
    )
