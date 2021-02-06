from django.urls import path
from . import views


app_name = 'quiz'
urlpatterns = [

    path('', views.index, name='index'),

    path('<int:quiz_id>/', views.single_quiz_page, name='single_quiz_page'),
    path('<int:quiz_id>/<int:question_id>/', views.single_question_page, name='single_question_page'),
    path('<int:quiz_id>/<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:quiz_id>/results', views.results_page, name='results_page'),
    path('create/', views.create_quiz_page, name='create_quiz_page'),
    path('create/<int:quiz_id>/<int:question_id>/', views.create_new_question_page, name='create_question_page'),

]
