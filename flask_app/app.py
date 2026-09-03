from flask import Flask, render_template, request
import mlflow
import pickle
import os
import pandas as pd
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import time
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import re
import dagshub
import numpy as np

import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")

from src.connections.credentials import Credential
from src.connections import s3_connection
from preprocessing_utility import normalize_text


#Dags_HUb authentication
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


# Initialize Flask app
app = Flask(__name__)


# Create a custom registry and metrics using prometheus_client
registry = CollectorRegistry()

# Define your custom metrics using this registry
REQUEST_COUNT = Counter(
    "app_request_count", "Total number of requests to the app", ["method", "endpoint"], registry=registry
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Latency of requests in seconds", ["endpoint"], registry=registry
)
PREDICTION_COUNT = Counter(
    "model_prediction_count", "Count of predictions for each class", ["prediction"], registry=registry
)

# Function Fetch the latest model
def get_latest_model_version(model_name):


    client = mlflow.MlflowClient()

    # Delete previously registerd model
    # for i in range(36, 48):
    #     client.delete_model_version(name=model_name, version=f"{i}")

    versions = client.search_model_versions(f"name='{model_name}'")
    if not versions:
        raise ValueError(f"No registered model versions found for '{model_name}'")
    
    latest_version = max(versions, key=lambda v: int(v.version))
    return latest_version.version

#Fetch the latest model
model_name = "my_model"
model_version = get_latest_model_version(model_name)
model_uri = f'models:/{model_name}/{model_version}'
print(f"Fetching model from: {model_uri}")
model = mlflow.pyfunc.load_model(model_uri)

# Load the vectorizer
Bucket_Name = os.getenv(Credential.S3_Bucket_Name)
Access_Key = os.getenv(Credential.Access_Key)
Secret_Key = os.getenv(Credential.Secret_Key)

s3 = s3_connection.s3_operations(Bucket_Name, Access_Key, Secret_Key)
vectorizer = s3.load_pkl('vectorizer.pkl')

# Routes
@app.route("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    start_time = time.time()
    response = render_template("index.html", result=None)
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start_time)
    return response

@app.route("/predict", methods=["POST"])
def predict():
    REQUEST_COUNT.labels(method="POST", endpoint="/predict").inc()
    start_time = time.time()

    text = request.form["text"]
    # Clean text
    text = normalize_text(text)
    # Convert to features
    features = vectorizer.transform([text])
    features_df = pd.DataFrame(features.toarray(), columns=[str(i) for i in range(features.shape[1])])

    # Predict
    result = model.predict(features_df)
    prediction = result[0]

    # Increment prediction count metric
    PREDICTION_COUNT.labels(prediction=str(prediction)).inc()

    # Measure latency
    REQUEST_LATENCY.labels(endpoint="/predict").observe(time.time() - start_time)

    return render_template("index.html", result=prediction)

@app.route("/metrics", methods=["GET"])
def metrics():
    """Expose only custom Prometheus metrics."""
    return generate_latest(registry), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # app.run(debug=True) # for local use
    app.run(debug=True, host="0.0.0.0", port=5000)  # Accessible from outside Docker
