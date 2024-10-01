# from datetime import datetime
from airflow import DAG
# from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
import shlex
from utils.notifier import MMNotifier

# Define a simple DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    # 'on_success_callback': MMNotifier(),
    # 'on_failure_callback': MMNotifier(),
}

params = {
    # "testString": Param(
    #     default=0,
    #     description="Enter your name please",
    #     type="string"
    # ),
    # "sampleObj": Param(
    #     default=0,
    #     description="Enter an obj",
    #     type="object"
    # ),
    "MM_WEBHOOK_URL": Param(
        default=0,
        description="MM_WEBHOOK_URL",
        type="string"
    ),
}

with DAG(
    dag_id='test-kube-pod-dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    # render_template_as_native_obj=True,
    params = params,
    
    on_failure_callback=MMNotifier(),
    on_success_callback=MMNotifier(),

    
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

        on_finish_action='delete_succeeded_pod',
        
        # on
    )
