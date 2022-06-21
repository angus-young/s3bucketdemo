from flask import Flask, Request
import os
import boto3

app = Flask(__name__)

aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
bucket = os.getenv("bucket")
region = os.getenv("region")

try:
    s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region
    )
except Exception as e:
    print(f"No AWS Client Connention\n\n{e}") 

@app.route('/')
def list_files():
    try: 
        s3_response = s3.list_objects(
            Bucket=bucket,
        )
        object_list = []
        for object in s3_response['Contents']:
            object_list.append(object["Key"])

        return f"{object_list}"
    except Exception as e:
        return f"Not able to connect s3 bucket and list objects\n\n{e}"


@app.route('/create/<parameter>')
def create_file(parameter=None):
    try:
        s3.upload_file('example.txt',bucket,str(parameter))
        return f"{parameter} created!"
    except Exception as e:
        return f"Not able to create object in s3 bucket\n\n{e}"

@app.route('/delete/<parameter>')
def delete_file(parameter=None):
    try:
        s3.delete_object(
            Bucket=bucket,
            Key=str(parameter),
        )
        return f"{parameter} deleted!"
    except Exception as e:
        return f"Not able to delete object from s3 bucket\n\n{e}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
