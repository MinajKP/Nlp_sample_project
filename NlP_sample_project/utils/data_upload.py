import logging

from boto3.dynamodb.conditions import Key
from django.conf import settings
import boto3
import hashlib

class DataUpload:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
        self.table = self.dynamodb.Table(settings.DYNAMODB_TABLE_NAME)

    def index_uploaded_file(self,file):
        # Generate a unique hash for the file content or use an existing one
        file_hash = self.generate_file_hash(file)
        doc = {
            'FileHash': file_hash,
            'file_id': str(file.id),
            'title': file.title,
            'content': file.content,
        }

        logging.info(f"Inserting item into DynamoDB: {doc}")
        #insert data into DynamoDB
        self.table.put_item(Item=doc)

    def generate_file_hash(self, file):
        # Function to generate a simple hash for the file
        return hashlib.sha256(file.content.encode('utf-8')).hexdigest()

    def get_file_by_id(self,file_id):
        # Fetch file from DynamoDB by file_id
        response = self.table.query(
            IndexName='file_id-index',# Use the name of your GSI
            KeyConditionExpression=Key('file_id').eq(file_id)
        )
        # item key returns a dictionary of file_id, title and content
        # Return the first item from the results (if exists)
        return response.get('Items', [])[0] if response.get('Items') else None
