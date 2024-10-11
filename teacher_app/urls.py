# teacher_app/urls.py
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
# ]
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='teacher_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Проверьте, чтобы это было правильно,
]
