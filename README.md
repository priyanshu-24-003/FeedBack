# FeedBack
LEARNING: Compelete MLOPS system for feedback classification on text input : classic NLP usecase



End-to-end MLOps pipeline for training, evaluating, registering, containerizing,deploying  and monitoring a machine learning model.

## Project Flow

```text
Data (S3)

   ↓

Data Ingestion

   ↓

Data Preprocessing

   ↓

Feature Engineering

   ↓

Model Building

   ↓

Model Evaluation

   ↓

Model Registration

   ↓

DVC Pipeline

   ↓

Flask API

   ↓

Docker → ECR

   ↓

EKS Deployment

   ↓

Prometheus → Grafana
```

## 1. Environment Setup

Create the virtual environment:

```bash
python3 -m venv envname
```

Activate it:

```bash
source envname/bin/activate
```

## 2. Experiment Tracking

Set up **MLflow** for experiment tracking and use **DagsHub** as the remote tracking server.

## 3. Pipeline Components

All pipeline code is maintained inside `src/`.

| Component                | Responsibility                                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------------------- |
| `logger/`                | Configured logger for the entire pipeline; stores logs in `data/log/`                                         |
| `data_ingestion.py`      | Pulls data from S3 and stores artifacts in `data/raw/`                                                        |
| `data_preprocessing.py`  | Processes `data/raw/`, including lemmatization, dropping NA values, etc.; stores artifacts in `data/interim/` |
| `feature_engineering.py` | Applies Bag of Words to `data/interim/`; stores artifacts in `data/processed/` and `models/vectorizer.pkl`    |
| `model_building.py`      | Trains Logistic Regression using `data/processed/`; stores the model in `model/model.pkl`                     |
| `model_evaluation.py`    | Evaluates the model on test data and stores `metrics.json` and `experiment_info.json`                         |
| `register_model.py`      | Registers a new model version when enabled by `params.yaml` and pushes the compatible vectorizer to S3        |

## 4. DVC Pipeline

DVC has been used for pipeline automation and versioning.

```bash
dvc repro
```

Pipeline parameters are configured in:

```text
params.yaml
```

Data and artifacts are versioned and pushed to an S3 bucket.

## 5. Flask Application

A Flask application serves the trained model through an API.

## 6. CI Pipeline

GitHub Actions is used for continuous integration.

The CI workflow performs:

1. Environment setup
2. Configure environment variables
3. Run the DVC pipeline
4. Train/evaluate the model
5. Run unit tests
6. Run Flask integration tests

### Tests

```text
tests/
├── test_model.py
└── test_flask_app.py
```

* `test_model.py` — unit tests for the newly produced model.
* `test_flask_app.py` — integration tests for the Flask application with the newly produced model.

The tests are executed as part of the CI workflow.

## 7. AWS Configuration

Configure the following GitHub Actions secrets/variables:

```text
AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_REGION

ECR_REPOSITORY

AWS_ACCOUNT_ID
```

The ECR repository used by the project is:

```text
feedback-image
```

The AWS IAM user requires:

```text
AmazonEC2ContainerRegistryFullAccess
```

## 8. CI/CD — Docker & ECR

The CI/CD pipeline builds the Docker image and pushes it to **Amazon ECR**.

```text
GitHub Actions

      ↓

DVC Repro

      ↓

Tests

      ↓

Docker Build

      ↓

Amazon ECR
```

## 9. EKS Deployment

Deploy the application to Amazon EKS using:

* AWS CLI
* `eksctl`
* `kubectl`
* GitHub Actions

```text
ECR

 ↓

EKS

 ↓

Flask Application
```

## 10. Monitoring

### Prometheus

Prometheus server is hosted on an external EC2 instance, with a modified scrape configuration to monitor the application deployed in the EKS cluster.

### Grafana

Grafana is hosted on an external EC2 instance for visualization and alerting. The EC2 instance running Prometheus is configured as the Grafana data source.

```text
EKS Application

      ↓

 Prometheus

      ↓

   Grafana
```

### Scope of Improvement

* Model performance is not that great due to the project's primary focus on the MLOps aspect. It can be improved with advanced feature engineering and feature selection techniques.
* A single logger file can be configured to produce one log file mapped to a single `run`.
