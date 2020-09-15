from supplyinvoice.models import  ImageModel,MAppingModels,FileModel
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# Serializers define the API representation.
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
        fields = ("id","mapping","model_id","created_date")
        
# class PDFModelSerializer(serializers.ModelSerializer):
#     id  = serializers.IntegerField(read_only=True)
#     class Meta:
#         model = PDFModels
#         fields = ("id","file")


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ("id","pdf_files","is_processed")





    