from rest_framework import routers
from django.conf.urls import url
from django.urls import path, include
from supplyinvoice import views

router = routers.DefaultRouter()

router.register(r"image_identification/",views.ImageIdentificationViewSet)
router.register(r'image_models/',views.ImageModelViews)
router.register(r'mapping_models/',views.MAppingModelsViews)


urlpatterns = [
    
    path('', include(router.urls)),
    
]