from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
from .models import ProgrammingLanguage, Topic, Prompt

def chat_view(request):
    return render(request, 'ai/chat.html')

def decide_task_view(request):
    return render(request, 'ai/decide-task.html')

def find_error_view(request):
    return render(request, 'ai/find-error.html')



def get_languages(request):
    languages = ProgrammingLanguage.objects.all().values('id', 'language_name')
    return JsonResponse(list(languages), safe=False)


def get_topics(request):
    topics = list(Topic.objects.values('id', 'topic_name', 'programming_language'))
    return JsonResponse(topics, safe=False)



def get_prompts(request):
    prompts = list(Prompt.objects.values(
        'id', 
        'topic_id',  # ID Topic
        'topic__programming_language',  # ID ProgrammingLanguage
        'prompt_text'
    ))
    return JsonResponse(prompts, safe=False)
