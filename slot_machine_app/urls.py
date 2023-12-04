from django.urls import path
from . import views

urlpatterns = [
    path('spin/', views.spin, name='spin'),
    path('spin_start/',views.spin_start, name='spin_start'),
    path('game_over/', views.slot_result, name='game_over'),  # game_over URL 패턴 추가
]