# journal_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_list, name='students_list'),
    path('<int:student_id>/', views.student_detail, name='student_detail'),
]


