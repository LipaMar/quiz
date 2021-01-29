from django.urls import path
from . import views


app_name = 'Quiz wsiz'
urlpatterns = [

    path('', views.index, name='index'),


]