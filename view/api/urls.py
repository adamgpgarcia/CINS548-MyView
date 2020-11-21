from django.urls import path,include
#from rest_framework import routers
from .views import viewuser_list, viewuser_Update
from django.conf.urls import url
#router=routers.DefaultRouter()
#router.register(r'ViewUser', viewuser_list)
urlpatterns = [
    #path('', include(router.urls)),
    path('viewuser', viewuser_list),
    path('viewuser/<int:id>',viewuser_Update),
]
