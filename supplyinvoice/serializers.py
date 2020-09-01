from supplyinvoice.models import ImageIdentification, ImageModel,MAppingModels
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# Serializers define the API representation.
class ImageIdentificationSerializer(serializers.HyperlinkedModelSerializer):
    img_id = serializers.UUIDField()
    class Meta:
        model = ImageIdentification
        fields = ("img_id","text","img")

class ImageModelSerializer(serializers.ModelSerializer):
    id                  = serializers.IntegerField(read_only=True)
    identification_text = serializers.CharField(required=True, allow_blank=False, max_length=100)
    model_name          = serializers.CharField(required=True, allow_blank=False, max_length=50)
    class Meta:
        model = ImageModel
        fields = ("id","identification_text","created_date","model_name")
        validators = [
            UniqueTogetherValidator(
                queryset=ImageModel.objects.all(),
                fields=['model_name']
            )
        ]
        
class MAppingModelsSerializer(serializers.ModelSerializer):
    id  = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = MAppingModels
        fields = ("id","text","type","x_axis","y_axis","width","height","status","block","csv_column","model_id","created_date")
        
    
        







    