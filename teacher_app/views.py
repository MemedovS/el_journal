
from django.shortcuts import render
from journal_app.models import TeachingAssignment, Grade,StudentGroup
from django.contrib.auth.decorators import login_required


# @login_required
# def teacher_dashboard(request):
#     teacher = request.user.teacher
#     assignments = TeachingAssignment.objects.filter(teacher=teacher)
#
#     # Структура данных для отображения студентов по предметам
#     students_with_grades = {}
#     for assignment in assignments:
#         subject = assignment.subject
#         student = assignment.student
#         grades = Grade.objects.filter(student=student, subject=subject)
#
#         # Сортировка по предмету
#         if subject not in students_with_grades:
#             students_with_grades[subject] = []
#
#         # Добавление студента и его оценок
#         students_with_grades[subject].append({
#             'student': student,
#             'grades': grades
#         })
#
#     return render(request, 'teacher_app/dashboard.html', {
#         'students_with_grades': students_with_grades,
#         'teacher': teacher
#     })
@login_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    groups = StudentGroup.objects.filter(teacher=teacher)

    # Структура данных для отображения студентов по предметам
    students_with_grades = {}
    for group in groups:
        assignments = TeachingAssignment.objects.filter(group=group)
        for assignment in assignments:
            subject = assignment.subject
            student = assignment.student
            grades = Grade.objects.filter(student=student, subject=subject)

            # Сортировка по предмету
            if subject not in students_with_grades:
                students_with_grades[subject] = []

            # Добавление студента и его оценок
            students_with_grades[subject].append({
                'student': student,
                'grades': grades
            })

    return render(request, 'teacher_app/dashboard.html', {
        'students_with_grades': students_with_grades,
        'teacher': teacher
    })
