# el_journal/urls.py
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('journal_app.urls')),  # Подключение к приложению students
    path('teacher/', include('teacher_app.urls')),   # Подключение к приложению teachers
    path('', lambda request: redirect(reverse_lazy('students_list'))),  # Редирект с корневого URL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
