from django.urls import path, include

from . import views
from .views import GroupStudentListView, GroupStudentDetailView, ScoreLessonListView, AddScore


urlpatterns = [
    path('people/', include('people.urls')),
    path('groups/', GroupStudentListView.as_view(), name='group_student_list'),
    path('group/<int:pk>/', GroupStudentDetailView.as_view(), name='group_student_detail'),
    path('<int:group_id>/<int:lesson_id>/', ScoreLessonListView.as_view(), name='score_lesson'),
    path('addscore/', AddScore.as_view(), name='add_score'),
    path('export_scores/excel/<int:group_id>/<int:lesson_id>/', views.export_scores_to_excel, name='export_scores_to_excel'),
    path('save_lesson_topic/', views.save_lesson_topic, name='save_lesson_topic'),
    path('add_attendance_score/', views.add_attendance_score, name='add_attendance_score'),
    path('add_sum_score/', views.add_sum_score, name='add_sum_score'),

]
