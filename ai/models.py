from django.db import models

# Модель темы
class Topic(models.Model):
    topic_name = models.CharField(max_length=255)

    def __str__(self):
        return self.topic_name

# Модель подтемы
class Subtopic(models.Model):
    subtopic_name = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.subtopic_name

# Модель языка программирования
class ProgrammingLanguage(models.Model):
    language_name = models.CharField(max_length=255)

    def __str__(self):
        return self.language_name

# Модель предпочтений пользователя
class UserPreference(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('topic', 'subtopic', 'language')

# Модель препромпта
class Prompt(models.Model):
    user_preference = models.ForeignKey(UserPreference, on_delete=models.CASCADE)
    prompt_text = models.TextField()

    def __str__(self):
        return self.prompt_text