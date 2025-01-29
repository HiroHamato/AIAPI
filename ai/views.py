from django.shortcuts import render


def chat_view(request):
    return render(request, 'ai/chat.html')

def base_view(request):
    return render(request, 'ai/base.html')
