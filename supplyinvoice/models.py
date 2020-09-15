from django.db import models
import uuid
from django_mysql.models import ListCharField
from model_utils import Choices
from django_mysql.models import JSONField, Model

# Create your models here.
class ImageModel(models.Model):
    model_name = models.CharField( max_length=50)
    identification_text = models.CharField(max_length = 100)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_date']
        
class MAppingModels(Model):
    mapping = JSONField()
    model_id = models.ForeignKey(ImageModel,  on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_date']
    
# from django.db import models
# from .models import File

class FileModel(models.Model):
    pdf_files = models.FileField(blank=True, default='')
    is_processed = models.BooleanField(default = False)
 
    