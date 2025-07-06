from django.contrib import admin
from .models import ProgrammingLanguage, Topic, Prompt

class PromptInline(admin.TabularInline):
    model = Prompt
    extra = 1 

class TopicInline(admin.TabularInline):
    ininlines = [PromptInline]
    model = Topic
    extra = 1  # Количество пустых форм для добавления тем
    fk_name = 'programming_language'  # Связь с языком программирования
    

class ProgrammingLanguageAdmin(admin.ModelAdmin):
    inlines = [TopicInline]  # Добавляем тему как вложенный объект в админке
    list_display = ('language_name',)  # Чтобы отображался язык программирования

class TopicAdmin(admin.ModelAdmin):
    inlines = [PromptInline]  # Добавляем препромт как вложенный объект в админке
    list_display = ('topic_name', 'programming_language')  # Чтобы отображалась тема и язык программирования

# Регистрируем модели с настройками админки
admin.site.register(ProgrammingLanguage, ProgrammingLanguageAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Prompt)
