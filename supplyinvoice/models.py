from django.db import models
import uuid
from django_mysql.models import ListCharField
from model_utils import Choices

# Create your models here.
class ImageIdentification(models.Model):
    img_id = models.UUIDField(primary_key = True,default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=150)
    img = models.ImageField( upload_to=None, height_field=None, width_field=None, max_length=None)
    
class ImageModel(models.Model):
    model_name = models.CharField( max_length=50)
    identification_text = models.CharField(max_length = 100)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_date']
        
class MAppingModels(models.Model):
    text    = models.CharField(max_length = 100)
    TYPE    = Choices('value', 'label')
    type    = models.CharField(choices=TYPE, default=TYPE.label, max_length=20)
    x_axis  = models.IntegerField() 
    y_axis  = models.IntegerField() 
    width   = models.IntegerField() 
    height  = models.IntegerField() 
    status  = models.BooleanField(default = True)
    block   = models.CharField( max_length=50)
    csv_column = ListCharField(
        base_field=models.CharField(max_length=50),
        size=10,
        max_length=(10 * 51)  # 6 * 10 character nominals, plus commas
    )
    model_id = models.ForeignKey(ImageModel,  on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_date']
    
    
 
    