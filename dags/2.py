# from datetime import datetime
from airflow import DAG
# from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
import shlex

# Define a simple DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

params = {
    "yourName": Param(
        default=0,
        description="Enter your name please",
        type="string"
    ),
    "userIds": Param(
        default=0,
        description="Enter user ids to run for",
        type="string"
    ),
    "obj": Param(
        default=0,
        description="Enter an obj",
        type="object"
    ),
    "myArr": Param(
        default=0,
        description="Enter new line scids",
        type="array"
    ),
}

with DAG(
    dag_id='test-kube-pod-dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    # render_template_as_native_obj=True,
    params = params
) as dag:

    # Kubernetes Pod Operator Task
    kubernetes_task = KubernetesPodOperator(
        image='deposit-job:latest',
        cmds=["sh", "-c"],
        arguments=[
            f"npm run start-job -- --params={shlex.quote("{{ params | tojson }}")}"
        ],
        task_id="deposit-task",
        get_logs=True,
        in_cluster=True,

        # cluster_context='docker-desktop',  # Specify your local Kubernetes context
        # config_file='/home/airflow/.kube/config',  # Path inside the Docker container

        # wait_until_job_complete=True,

        image_pull_policy="IfNotPresent",

        on_finish_action='keep_pod',
    )
