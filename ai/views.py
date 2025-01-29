from django.shortcuts import render


def chat_view(request):
    return render(request, 'ai/chat.html')

def decide_task_view(request):
    return render(request, 'ai/decide-task.html')

def find_error_view(request):
    return render(request, 'ai/find-error.html')
