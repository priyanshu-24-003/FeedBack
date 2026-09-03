import boto3
import pandas as pd
try:    
    from src.logger import logging
except Exception as e:
    import logging
    
from io import StringIO
import pickle


class s3_operations:
    def __init__(self, bucket_name, aws_access_key, aws_secret_key, region_name="us-east-1"):
        """
        Initialize the s3_operations class with AWS credentials and S3 bucket details.
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        logging.info("Data Ingestion from S3 bucket initialized")

    def fetch_file_from_s3(self, file_key):
        
        try:
            logging.info(f"Fetching file '{file_key}' from S3 bucket '{self.bucket_name}'...")
            obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
            logging.info(f"Successfully fetched and loaded '{file_key}' from S3 that has {len(df)} records.")
            return df
        except Exception as e:
            logging.exception(f"❌ Failed to fetch '{file_key}' from S3: {e}")
            return None


    def Push_file_to_s3(self,from_file, file_key):

        try:
            logging.info(f"Pushing file '{file_key}' to '{self.bucket_name}'...")

            self.s3_client.upload_file(
                Filename=from_file,
                Bucket=self.bucket_name,
                Key=file_key,
            )

            logging.info(f"Pushed file '{file_key}' to '{self.bucket_name}'...")

        except Exception as e:
            logging.exception(f"❌ Failed to push {file_key}' to S3: {e}")
            return None


    def load_pkl(self, file):
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file)
            pkl_bytes = response["Body"].read()
            pkl = pickle.loads(pkl_bytes)
            logging.info(f'loaded the vectorizer from s3')
            return pkl
        except Exception as e:
            logging.info(f'Could notload the vectorizer from s3')
            return None



