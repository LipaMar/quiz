from django.contrib import admin

from .models import Quiz, Question, Choice

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
