import os
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

def run_client(query):
    credentials = service_account.Credentials.from_service_account_file(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

    project_id = os.getenv("PROJECT_ID")

    client = bigquery.Client(credentials=credentials, project=project_id)

    query_job = client.query(query)

    query_job.result()

    results = query_job.result()
    
    return results

