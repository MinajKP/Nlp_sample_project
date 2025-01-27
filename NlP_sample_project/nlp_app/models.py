from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Text, Keyword, connections

# Elasticsearch connection setup
connections.configure(
    default={
        'hosts': ['https://12f8d987e674446f89c40f2863bb357b.us-central1.gcp.cloud.es.io'],
        'http_auth': ('elastic', '9UtmuLqBeCiGdo3pbgRpeNxo'),
        'scheme': 'https',
        'port': 9243,
    }
)

# Define the Elasticsearch document for indexing files
class UploadedFileIndex(Document):
    title = Text()
    content = Text()
    file_id = Keyword()

class Index:
    name = 'file_index'  # Elasticsearch index name

    def save(self, **kwargs):
        return super().save(**kwargs)


class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Signal to index file content in Elasticsearch when an UploadedFile is saved
@receiver(post_save, sender=UploadedFile)
def index_file_in_es(sender, instance, **kwargs):
    try:
        file_index = UploadedFileIndex(
            meta={'id': instance.id},  # Use the model's ID as the Elasticsearch document ID
            title=instance.title,
            content=instance.content,
            file_id=str(instance.id),
        )
        file_index.save()
    except Exception as e:
        print(f"Error indexing file in Elasticsearch: {e}")


# Signal to remove file content from Elasticsearch when an UploadedFile is deleted
@receiver(pre_delete, sender=UploadedFile)
def delete_file_from_es(sender, instance, **kwargs):
    try:
        es = Elasticsearch(
            hosts=['https://12f8d987e674446f89c40f2863bb357b.us-central1.gcp.cloud.es.io'],
            http_auth=('elastic', '9UtmuLqBeCiGdo3pbgRpeNxo'),
            scheme='https',
            port=9243,
        )
        es.delete(index='file_index', id=str(instance.id))
    except Exception as e:
        print(f"Error deleting file from Elasticsearch: {e}")
