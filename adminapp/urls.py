from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('queenAdmin/',views.admin_index),
    path('userlist/', views.user_list, name='userlist'),
    path('moneyApply/',views.moneyApply,name='moneyApply'),
    path('userDelete/' , views.userDelete ,name='userDelete'),
    path('serverStatus/',views.serverStatus,name='serverStatus'),
    path('webServerStatus/',views.webServerStatus,name='webServerStatus'),
    path('wasServerStatus/',views.wasServerStatus,name='wasServerStatus'),
    path('run/',views.run,name='run')
    
]