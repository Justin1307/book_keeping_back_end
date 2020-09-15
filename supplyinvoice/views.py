from supplyinvoice.models import ImageModel, MAppingModels,FileModel
from rest_framework import viewsets
from supplyinvoice.serializers import ImageModelSerializer,MAppingModelsSerializer,FileSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status



# ViewSets define the view behavior.

class ImageModelViews(viewsets.ModelViewSet):
    queryset         = ImageModel.objects.all()
    serializer_class = ImageModelSerializer    

class MAppingModelsViews(viewsets.ModelViewSet):
    queryset         = MAppingModels.objects.all()
    serializer_class = MAppingModelsSerializer
        
class FileUploadView(viewsets.ModelViewSet):
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer
    parser_class = (FileUploadParser,)

    def pre_save(self, obj):
        obj.samplesheet = self.request.FILES.get('file')
        
class MappingModelDetail(viewsets.ViewSet):
    """
    Retrieve, update or delete a MAppingModels instance.
    
    """
    def create(self, request):
        input_data = request.data
        print(input_data)
        pk = input_data.get("id")
        queryset = MAppingModels.objects.filter(id = pk)
        serializer = MAppingModelsSerializer(queryset, many=True)
        queryset.delete()
        return Response(serializer.data)
    
class ProcessFiles(viewsets.ViewSet):
    
    def create(self,request):
        # image_models     = ImageModel.objects.all()
        # serializer       = ImageModelSerializer(image_models,many=True)
        # data = serializer.data
        # for d in data:
        #     print(dict(d))
      
        from supplyinvoice.process import PdfFileProcessing
        pdf_process = PdfFileProcessing()
        pdf_process.process_pdf()
        return Response("data")
    