from rest_framework import routers
from django.conf.urls import url
from django.urls import path, include
from supplyinvoice import views

router = routers.DefaultRouter()

router.register(r'image_models/',views.ImageModelViews)
router.register(r'mapping_models/',views.MAppingModelsViews)
router.register(r'file_upload/',views.FileUploadView)
router.register(r'mapping_details/',views.MappingModelDetail,basename='MappingModelDetail')
router.register(r'process_pdf/',views.ProcessFiles, 'ProcessFiles')


urlpatterns = [
    
    path('', include(router.urls)),
    # path('file_upload/', views.FileUploadView.as_view())
    
]