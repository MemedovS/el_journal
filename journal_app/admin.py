# journal_app/admin.py

from django.contrib import admin
from .models import Student, Subject, Teacher, Grade,TeachingAssignment,StudentGroup

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(StudentGroup)
admin.site.register(Grade)
admin.site.register(TeachingAssignment)