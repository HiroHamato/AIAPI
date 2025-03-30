from django.urls import path
from . import views

urlpatterns = [
    path('ai/chat/', views.chat_view, name='chat_view'),
    path('ai/decide-task/', views.decide_task_view, name='decide_task_view'),
    path('ai/find-error/',views.find_error_view, name='find_error_view'),
    path('cdn_proxy/', views.cdn_proxy, name='cdn_proxy'),
]

