from django.db import models
import uuid

# Create your models here.
class ImageIdentification(models.Model):
    img_id = models.UUIDField(primary_key = True,default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=150)
    img = models.ImageField( upload_to=None, height_field=None, width_field=None, max_length=None)