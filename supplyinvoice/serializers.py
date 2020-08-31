from supplyinvoice.models import ImageIdentification
from rest_framework import serializers


# Serializers define the API representation.
class ImageIdentificationSerializer(serializers.HyperlinkedModelSerializer):
    img_id = serializers.UUIDField()
    class Meta:
        model = ImageIdentification
        fields = ("img_id","text","img")
