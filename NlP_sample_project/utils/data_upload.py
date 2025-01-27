from elasticsearch_dsl import connections
from django.conf import settings

class DataUpload:
    def __init__(self):
        # Elasticsearch connection setup
        connections.configure(default={
            'hosts': [settings.ELASTICSEARCH_HOST],
            'http_auth': tuple(settings.ELASTICSEARCH_AUTH.split(',')),
        })

    def index_uploaded_file(self,file):
        doc = {
            'title': file.title,
            'content': file.content,
            'file_id': str(file.id),
        }
        connections.get_connection().index(index='file_index', id=file.id, body=doc)
