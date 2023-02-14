from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    # path('<str:room_info>/<str:user_info>', views.room, name='room'),
    # path('check_view/', views.check_view, name='check_view'),
    # path('send/', views.send, name='send'),
    # path('get_messages/<str:room_name>/', views.get_messages, name='get_messages'),
]