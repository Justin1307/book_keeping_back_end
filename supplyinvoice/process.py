from supplyinvoice.models import ImageModel, FileModel,MAppingModels
from supplyinvoice.serializers import ImageModelSerializer,FileSerializer,MAppingModelsSerializer
from rest_framework.renderers import JSONRenderer
from supplyinvoice.pdf_converter import pdf_to_image
from book_keeping_back.settings import MEDIA_ROOT
from supplyinvoice.tesseract_operations import TesseractFunctions
tf = TesseractFunctions()

class PdfFileProcessing():
    def __init__(self):
        self.image_models     = ImageModel.objects.all()
        self.img_serializer   = ImageModelSerializer(self.image_models,many=True)
        self.file_model       = FileModel.objects.filter(is_processed = False)
        self.file_serializer  = FileSerializer(self.file_model, many = True)
        
        # self.image_model_json = JSONRenderer().render(self.serializer.data)
        print(self.file_serializer.data)
            # print(serl.data)
    def get_image_text_data_list(self,image_list):
        list_image_text  = []
        list_img_data    = []
        for image in image_list:
            image_text =tf.image_process(image)
            list_image_text.append(image_text.splitlines())
            list_img_data.extend(tf.image_process(image,to_data =True))
        return list_image_text,list_img_data
    
    def get_models(self,list_image_text):
        for model in self.img_serializer.data:
            model = dict(model)
            if model.get("identification_text") in str(list_image_text):
                return model
    def update_file_model(self,file_list):
        print(file_list)
        for file in file_list:
            if file.get('id'):
                file_model= FileModel.objects.filter(id = file.get('id')).update(is_processed = True)
                print
        return file_list
    
    def get_mapping(self,model_id):
        mapping_list = []
        image_mapping_model = MAppingModels.objects.filter(model_id =model_id)
        mapping_serializer = MAppingModelsSerializer(image_mapping_model, many =True)
        for mapping in mapping_serializer.data:
            mapping = dict(mapping)
            mapping_list.append(mapping.get("mapping"))
        return mapping_list
    
        
    
    def process_pdf(self):
        excel_list       = []
        processed_files = []
        unmapped_files = []
        if self.file_serializer.data:
            for pdf in self.file_serializer.data:
                pdf_data = dict(pdf)
                pdf_name = pdf_data.get('pdf_files')
                pdf_name = pdf_name.replace('/media/','')
                pdf_source = MEDIA_ROOT+"\\"+pdf_name
                image_list = pdf_to_image(pdf_source)
                list_image_text,list_img_data = self.get_image_text_data_list(image_list)
                
                model_dict = self.get_models(list_image_text)
                if model_dict:
                    mapping_list = self.get_mapping(model_dict.get("id"))
                
                    from supplyinvoice.data_processing import ProcessingData
                    pd = ProcessingData(list_img_data,mapping_list)  
                    mapping_list = pd.process_data() 
                    excel_list.append(mapping_list)
                    processed_files.append(pdf_data)
                else:
                    unmapped_files.append(pdf_data)
            from supplyinvoice.excel_generation import ExcelGeneration
            eg = ExcelGeneration()
            file_name =eg.excel_creation(excel_list)
            print(processed_files)
            self.update_file_model(processed_files)
        else:
            print("no files to process")
            
            
            
        # pass
        