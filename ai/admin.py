from django.contrib import admin
from .models import Topic, Subtopic, ProgrammingLanguage, UserPreference, Prompt

admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(ProgrammingLanguage)
admin.site.register(UserPreference)
admin.site.register(Prompt)
