import requests

token = "<your-access-token>"
deployment_url = "localhost:8081"
response = requests.get(
   url=f"http://{deployment_url}/api/v1/dags",
   auth=("airflow", "airflow")
)

print(response.json())
# Prints data about all DAGs in your Deployment

