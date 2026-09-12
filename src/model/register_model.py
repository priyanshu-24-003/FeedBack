import json
import mlflow
import logging
from src.logger import logging
import os
import dagshub

import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")
import pickle

from src.model.model_evaluation import load_model
from src.utilities.utils_functions import load_params

from src.connections.credentials import Credential
from src.connections import s3_connection

logging.critical("Registering model to the 'staging' area")


# Below code block is for production use
# -------------------------------------------------------------------------------------
# Set up DagsHub credentials for MLflow tracking
dagshub_token = os.getenv(Credential.Dags_Token)
if not dagshub_token:
    raise EnvironmentError("DAGS_TOKEN environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = os.getenv(Credential.OWNER)
repo_name = Credential.PROJECT_NAME

# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')
# -------------------------------------------------------------------------------------



def load_model_info(file_path: str) -> dict:
    """Load the model info from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            model_info = json.load(file)
        logging.debug('Model info loaded from %s', file_path)
        return model_info
    except FileNotFoundError:
        logging.error('File not found: %s', file_path)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the model info: %s', e)
        raise

def register_model(model, model_name: str, model_info: dict):
    """Register the model to the MLflow Model Registry."""
    try:
        model_uri = f"runs:/{model_info['run_id']}/{model_info['model_path']}"
        

        mlflow.set_experiment("My-DVC-Pipeline-Experiment")
        with mlflow.start_run(run_id=model_info['run_id']):

            model_info = mlflow.sklearn.log_model(sk_model=model, artifact_path=model_info['model_path'], registered_model_name=model_name)

        logging.debug(f'Model {model_name} version {model_info.registered_model_version} registered and transitioned to Staging.')

        Bucket_Name = os.getenv(Credential.S3_Bucket_Name)
        Access_Key = os.getenv(Credential.Access_Key)
        Secret_Key = os.getenv(Credential.Secret_Key)
        
        s3 = s3_connection.s3_operations(Bucket_Name, Access_Key, Secret_Key)
        df = s3.Push_file_to_s3("models/vectorizer.pkl", "vectorizer.pkl")

        logging.debug(f"A compatible Vectorizer to mymodel has been pushed to s3.")

    except Exception as e:
        logging.error('Error during model registration: %s', e)
        raise

def main():
    params = load_params('params.yaml')
    if not params['registration']['register']:
        logging.info("Model registration is disabled in params.yaml. Exiting.")
        return None
    
    try:
        model_info_path = 'reports/experiment_info.json'
        model_info = load_model_info(model_info_path)
        clf = load_model('./models/model.pkl')
        model_name = "my_model"
        register_model(clf, model_name, model_info)


        logging.critical("Model Registration completed")

    except Exception as e:
        logging.error('Failed to complete the model registration process: %s', e)
        print(f"Error: {e}")

    

if __name__ == '__main__':
    main()