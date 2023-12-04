from django.contrib import admin
from django.urls import path
from . import views

app_name = "rockscipaper"
urlpatterns = [
    path('rsp/',views.rsp,name='rsp'),
    path('rsp_start/',views.rsp_start,name='rsp_start'),
    path('rspResult/',views.rsp_result,name='rspResult')
    
]