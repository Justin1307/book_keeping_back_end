from rest_framework import routers
from django.conf.urls import url
from django.urls import path, include
from supplyinvoice import views

router = routers.DefaultRouter()

router.register(r"image_identification/",views.ImageIdentificationViewSet)


urlpatterns = [
    
    path('', include(router.urls)),
    
]