from airflow.notifications.basenotifier import BaseNotifier
from airflow.configuration import conf
import urllib.parse
import pendulum
from textwrap import dedent
import requests
from airflow.utils.state import State

class MMNotifier(BaseNotifier):

    def __init__(self):
        pass

    def notify(self, context):
    
        # Send notification here, below is an example
        self._send_alert(context)
      
    def _send_alert(self, context):
        """
        Function to be used as a callable for on_<event>_callback.
        Send a Mattermost alert.
        """
        try:
            base_url = conf.get('webserver', 'base_url')
            task_state = context["task_instance"].state
            
            
            # TODO: make it to secret
            mm_webhook_url = context['params']['MM_WEBHOOK_URL'] 

            ist_tz = pendulum.timezone("Asia/Kolkata")
            logical_date = ist_tz.convert(context["logical_date"]).format('YYYY-MM-DD HH:mm:ss')
            
            interval_start = context["data_interval_start"]
            actual_start = ist_tz.convert(interval_start).format('YYYY-MM-DD HH:mm:ss')
            
            interval_end = context["data_interval_end"]
            
            
            duration = interval_end.diff_for_humans(absolute=True)
            
            dag_id = context["dag"].dag_id
            task_name = context["task"].task_id
            task_id = context["task_instance"].task_id
            params = context["params"]
            run_id = context["run_id"]
            
            # execution_date_pretty = context["logical_date"].strftime("%a, %b %d, %Y at %-I:%M %p UTC")

            # Generate the link to the logs
            execution_date = context["ts"]
            log_params = urllib.parse.urlencode({"dag_id": dag_id, "task_id": task_id, "execution_date": execution_date})
            log_link = f"{base_url}/log?{log_params}"
            log_link_markdown = f"[View Logs]({log_link})"

            bodyTableRows = [
                "| Field  | Value |",
                "| ------ | ----- |",
                f"| Logs | {log_link_markdown} |",
                f"| dag_id | {dag_id} |",
                f"| task_name | {task_name} |",
                f"| task_id | {task_id} |",
                f"| params | {params} |",
                f"| run_id | {run_id} |",
                f"| logical_date | {logical_date} |",
                f"| actual_start | {actual_start} |",
                f"| duration | {duration} |",
            ]
            
            
            body_table_str = "\n".join(bodyTableRows)
            
            emoji = ":rocket:" if (task_state == State.SUCCESS) else ":savdhaan:" 
            body = dedent(
            f"""
            Result for {dag_id} {emoji}
            {body_table_str}
            """
            )
            # self.post_alert(body, mm_webhook_url)
            
            # url = 'https://hungry-ghosts-cry.loca.lt'
            myobj = {
                'text': body
            }
            x = requests.post("https://hungry-ghosts-cry.loca.lt", json = myobj)
            print(x.text)
            return
        
        except Exception as e:
            url = 'https://hungry-ghosts-cry.loca.lt'
            myobj = {
                'text': 'error',
                'base_url': base_url,
                'task_state': task_state,
                'err_msg': e.__str__
            }
            x = requests.post(url, json = myobj)
            print(x.text)
            return
        
    def post_alert(body, webhook_url):
        payload = {"username": "Airflow Deposits", "text": body}
        x = requests.post(webhook_url, json = payload)
        print(x.text)