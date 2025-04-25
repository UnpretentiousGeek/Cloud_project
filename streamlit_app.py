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

st.title("📁 Upload Files to S3")
st.write("This app uploads files directly to AWS S3")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Generate unique filename with timestamp
    filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Generate presigned URL
    presigned_url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': S3_BUCKET,
            'Key': filename,
            'ContentType': 'text/csv'
        },
        ExpiresIn=3600
    )
    
    # Upload file to S3
    try:
        response = requests.put(
            presigned_url,
            data=uploaded_file.getvalue(),
            headers={'Content-Type': 'text/csv'}
        )
        if response.status_code == 200:
            st.success(f"✅ File uploaded successfully to: `s3://{S3_BUCKET}/{filename}`")
            st.balloons()
        else:
            st.error(f"Upload failed with status {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
