from supplyinvoice.models import ImageIdentification
from rest_framework import viewsets
from supplyinvoice.serializers import ImageIdentificationSerializer

# ViewSets define the view behavior.
class ImageIdentificationViewSet(viewsets.ModelViewSet):
    queryset = ImageIdentification.objects.all()
    serializer_class = ImageIdentificationSerializer

