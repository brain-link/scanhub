"""Hello world DAG example."""
from datetime import datetime, timezone

import pendulum
from airflow.decorators import dag, task


@dag(
    dag_id='hello_world',
    default_args = {
        'owner': 'BRAIN-LINK',
    },
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def taskflow_api() -> None:
    """Create taskflow."""

    @task()
    def get_current_datetime() -> str:
        """Return current datetime as string."""
        now = datetime.now(tz=timezone.utc)
        return now.strftime("%Y-%m-%d %H:%M:%S")

    @task()
    def hello_world(current_datetime: str) -> None:
        """Output hello world with current datetime."""
        print(f"Hello World! ({current_datetime})")

    now = get_current_datetime()
    hello_world(now)

taskflow_api()
