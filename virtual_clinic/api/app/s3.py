from app import app
import boto3
from botocore.exceptions import ClientError
import logging


app.config['UPLOAD_EXTENSIONS'] = ['doc', 'docx', 'jpeg', 'jpg', 'pdf', 'png', 'txt']
s3_client = boto3.client('s3')


def allowed_file_extension(filename):
    """Check if file extension of file is allowed"""

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']


def get_s3_key(patient_id, filename):
    """Generate key name for S3 given a patient_id and filename"""

    return f'{str(patient_id)}/{filename}'


def save_file(file, patient_id, filename):
    """Upload file to S3 bucket

    Returns True if file was uploaded, else False
    """

    try:
        s3_client.upload_fileobj(
            file, app.config['S3_BUCKET'], get_s3_key(patient_id, filename))
    except ClientError as e:
        logging.error(e)
        return False
    return True


def check_file_exists(patient_id, filename):
    """Check if file exists in S3 bucket

    Returns True if file exists, else False
    """

    try:
        s3_client.head_object(Bucket=app.config['S3_BUCKET'],
                              Key=get_s3_key(patient_id, filename))
    except ClientError:
        return False
    return True


def delete_file(patient_id, filename):
    """Delete file from S3 bucket

    Returns True if file was deleted, else False
    """
    try:
        s3_client.delete_object(Bucket=app.config['S3_BUCKET'],
                                Key=get_s3_key(patient_id, filename))
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(patient_id, filename):
    """Download file from S3 bucket"""

    object = s3_client.get_object(Bucket=app.config['S3_BUCKET'],
                                  Key=get_s3_key(patient_id, filename))
    return object['Body']
