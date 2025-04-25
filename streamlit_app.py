import requests
import streamlit as st
import boto3
import os
from datetime import datetime

# AWS Configuration (use environment variables or Streamlit secrets)
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = st.secrets["AWS_SECRET_KEY"]
S3_BUCKET = "mini-projectsu"  # Your upload bucket
REGION = "us-east-1"  # Change to your region

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)
try:
    s3.list_objects(Bucket=S3_BUCKET, MaxKeys=1)
    st.text("Credentials valid")
except Exception as e:
    st.text(e)