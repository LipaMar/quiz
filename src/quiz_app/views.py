from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Quiz, Choice


def index(request):
    all_quizzes = Quiz.objects.all()
    context = {'all_quizzes': all_quizzes}
    return render(request, 'index.html', context)

def single_quiz_page(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    num_of_questions = len(quiz.question_set.all())

    if(num_of_questions == 0):
        quiz.delete()
        all_quizzes = Quiz.objects.all()
        context = {'all_quizzes': all_quizzes}
        return render(request, 'index.html', context)

    quiz.num_questions = num_of_questions
    quiz.save()

    request.session["num_correct"] = 0
    request.session["num_wrong"] = 0

    context = {'quiz': quiz, 'num_questions': num_of_questions}
    return render(request, 'single_quiz_page.html', context)

def single_question_page(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    current_question = quiz.question_set.get(question_num=question_id)

    next_or_submit = "Next"
    last_question_check = False
    if question_id == (len(quiz.question_set.all())):
        last_question_check = True
        next_or_submit = "Submit"

    next_question_id = question_id+1

    all_choices = current_question.choice_set.all()

    context = {
        'current_question': current_question,
        'all_choices': all_choices,
        'quiz': quiz,
        'next_question_id': next_question_id,
        'last_question_check': last_question_check,
        'next_or_submit': next_or_submit
    }

    return render(request, 'single_question_page.html', context)


def vote(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    current_question = quiz.question_set.get(question_num=question_id)

    next_or_submit = "Next"
    if(question_id == (len(quiz.question_set.all()))):
        next_or_submit = "Submit"

    try:
        selected_choice = current_question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'single_question_page.html', {
            'quiz': quiz,
            'current_question': current_question,
            'error_message': "Choose an answer!",
            'next_or_submit': next_or_submit,
        })
    else:
        correct_answer = current_question.choice_set.get(correct=True)

        if(selected_choice == correct_answer):
            request.session["num_correct"] += 1
        else:
            request.session["num_wrong"] += 1

        if(question_id == (len(quiz.question_set.all()))):
            return HttpResponseRedirect(reverse('quiz:results_page', args=(quiz.id, )))
        else:
            return HttpResponseRedirect(reverse('quiz:single_question_page', args=(quiz_id, question_id+1)))


def results_page(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    num_correct = request.session["num_correct"]
    num_wrong = request.session["num_wrong"]

    total_questions = num_correct + num_wrong

    score = num_correct/total_questions
    score_over_75 = False
    if(score >= .75):
        score_over_75 = True
    percentage_score = "{:.0%}".format(score)

    context ={
        'num_correct': num_correct,
        'num_wrong':num_wrong,
        'score_over_75': score_over_75,
        'percentage_score': percentage_score,
        'total_questions': total_questions,
        'quiz': quiz,
    }
    return render(request, 'results_page.html', context)