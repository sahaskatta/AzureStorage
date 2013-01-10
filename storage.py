from django.conf import settings
from django.core.files.storage import Storage

from azure.storage import *
from tempfile import SpooledTemporaryFile
from datetime import datetime
import os, mimetypes

class AzureStorage(Storage):

    def __init__(self, container=None):
        self.blob_service = BlobService(account_name=settings.AZURE_STORAGE_ACCOUNT, account_key=settings.AZURE_STORAGE_KEY)
        if not container:
            self.container = settings.AZURE_STORAGE_CONTAINER
        else:
            self.container = container
        self.blob_service.create_container(self.container, x_ms_blob_public_access='blob')

    def _open(self, name, mode='rb'):
        data = self.blob_service.get_blob(self.container, name)
        temp_file = SpooledTemporaryFile(mode='wb')
        temp_file.write(data)
        return temp_file

    def _save(self, name, content):
        content.open(mode="rb")
        data = content.read()
        content_type = mimetypes.guess_type(name)[0]
        metadata = {"modified_time": "%f" % os.path.getmtime(content.name)}
        self.blob_service.put_blob(self.container, name, data, x_ms_blob_type='BlockBlob', x_ms_blob_content_type=content_type, x_ms_meta_name_values=metadata)
        return name

    def delete(self, name):
        try:
            self.blob_service.delete_blob(self.container, name)
        except: pass
        return name

    def exists(self, name):
        blob = self.blob_service.list_blobs(self.container, prefix=name)
        if (len(blob) == 0) or (blob.blobs[0].name != name):
            return False

        else:
            return True

    def listdir(self, path):
        dirs = []
        files = []
        blobs = self.blob_service.list_blobs(self.container, prefix=(path or None))
        for blob in blobs:
            directory, file_name = os.path.split(blob.name)
            dirs.append(directory)
            files.append(file_name)
        return (dirs, files)

    def size(self, name):
        properties = self.get_blob_properties(self.container, name)
        return properties.get('content-length')

    def url(self, name):
        blob = self.blob_service.list_blobs(self.container, prefix=name)
        return blob.blobs[0].url

    def modified_time(self, name):
        metadata = self.blob_service.get_blob_metadata(self.container, name)
        modified_time = float(metadata.get('x-ms-meta-modified_time'))
        return datetime.fromtimestamp(modified_time)