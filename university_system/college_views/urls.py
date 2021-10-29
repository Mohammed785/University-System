from django.urls import path
from .views import home,index,support

urlpatterns = [
    path('',home,name='home'),
    path('index/',index,name='index'),
    path('support/',support,name='support-view')
]

