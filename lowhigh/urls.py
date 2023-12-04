from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('lowhigh/',views.lowhighView,name='lowhigh'),
    path('lowhighStart/',views.lowhighStart,name='lowhighStart'),
    path('lowhighResult/',views.lowhighResult,name='lowhighResult'),
]
    