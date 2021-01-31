from django.shortcuts import render
from .models import Quiz


def index(request):
    all_quizzes = Quiz.objects.all()
    context = {'all_quizzes': all_quizzes}
    return render(request, 'index.html', context)
