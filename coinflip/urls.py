from django.urls import path
from . import views

urlpatterns = [
    path('coinflip', views.coinflip, name='coinflip'),
    path('coinre',views.result,name='coinre')
]