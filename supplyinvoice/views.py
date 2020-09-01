from supplyinvoice.models import ImageIdentification,ImageModel, MAppingModels
from rest_framework import viewsets
from supplyinvoice.serializers import ImageIdentificationSerializer ,ImageModelSerializer,MAppingModelsSerializer

# ViewSets define the view behavior.
class ImageIdentificationViewSet(viewsets.ModelViewSet):
    queryset         = ImageIdentification.objects.all()
    serializer_class = ImageIdentificationSerializer


class ImageModelViews(viewsets.ModelViewSet):
    queryset         = ImageModel.objects.all()
    serializer_class = ImageModelSerializer    

class MAppingModelsViews(viewsets.ModelViewSet):
    queryset         = MAppingModels.objects.all()
    serializer_class = MAppingModelsSerializer
    