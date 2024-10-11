# journal_app/views.py
from django.shortcuts import render, get_object_or_404
from .models import Student, Grade,Subject,Teacher

from django.db.models import Q


def students_list(request):
    query = request.GET.get('q')
    if query:
        # Фильтрация студентов по имени, фамилии или ID
        students = Student.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_id__icontains=query)
        )
    else:
        students = Student.objects.all()

    return render(request, 'journal_app/students_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)  # Измените на id
    grades = Grade.objects.filter(student=student)

    context = {
        'student': student,
        'grades': grades,
    }
    return render(request, 'journal_app/student_detail.html', context)

