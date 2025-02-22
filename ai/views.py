from django.shortcuts import render

from django.http import JsonResponse
from .models import ProgrammingLanguage

def chat_view(request):
    return render(request, 'ai/chat.html')

def decide_task_view(request):
    return render(request, 'ai/decide-task.html')

def find_error_view(request):
    return render(request, 'ai/find-error.html')



def get_languages(request):
    languages = ProgrammingLanguage.objects.all().values('id', 'language_name')
    return JsonResponse(list(languages), safe=False)
