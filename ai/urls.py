from django.urls import path
from . import views

urlpatterns = [
    path('ai/chat/', views.chat_view, name='chat_view'),
    path('ai/base/', views.base_view, name='base_view'),  # Новый маршрут
]
