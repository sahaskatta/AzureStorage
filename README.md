# AzureStorage Backend for Django
Implements a Django storage subclass for use with Azure Blob storage.
Works for Static and Media files.

## Set-Up
- Install the Azure Python SDK: `pip install azure`.
- Copy `storage.py` into your project folder.
- Open your `settings.py` and add the following settings:

```python
# Replace <...> appropriately with your information

# AzureStorage Settings
AZURE_STORAGE_ACCOUNT = "<account_name>"
AZURE_STORAGE_KEY = "<account_key>"
AZURE_STORAGE_CONTAINER = "<default_storage_container>" # statics will use this container

# Static Settings
STATICFILES_STORAGE = "<my_project>.storage.AzureStorage"
STATIC_URL = "http://<storage account>.blob.core.windows.net/<default_storage_container>/"

# Media Settings
MEDIA_URL = 'http://storage.pepperdeck.com/<media_container>/'
```

**Note:** AzureStorage will create a container for you if the specified one does not exist.

## Using Static Files
```bash
python manage.py collectstatic
```
- AzureStorage sets file modified metadata, so the next time you collectstatic only changed files will be copied.
- **Note:** It may look like the terminal is hanging, but it's actually checking the modified times.

## Using Media Files or Other Custom Implementations:

- We needed to set a default container earlier, however we can override this!

Model Field Example:
```python
from django.db import models
from <my_project>.storage import AzureStorage

class MyModel(models.Model):
    my_file = models.FileField(upload_to="files", storage=AzureStorage(container="<media_container>"))
    my_image = models.ImageField(upload_to="images", storage=AzureStorage(container="<media_container>"))
```

Custom Example:
```python
# Instantiating the storage class with specified container
storage = AzureStorage(container="<some_container>")

# Instantiating with no arguements (uses previously defined AZURE_STORAGE_CONTAINER)
storage = AzureStorage()
```

**Note**: The following methods have been implemented:
`save`, `delete`, `exists`, `listdir`, `size`, `url`, `modified_time`
Full documentation on what each method does can be found: [Django File Storage API](https://docs.djangoproject.com/en/dev/ref/files/storage/#the-storage-class)

## Additional Resources
[Azure Python SDK](https://github.com/WindowsAzure/azure-sdk-for-python)
[Django Custom File Storage](https://docs.djangoproject.com/en/dev/howto/custom-file-storage/)