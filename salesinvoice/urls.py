from rest_framework import routers
from django.conf.urls import url
from django.urls import path, include

router = routers.DefaultRouter()



urlpatterns = [
    
    path('', include(router.urls)),
    
]