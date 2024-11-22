import re
import openpyxl
from openpyxl.utils import get_column_letter
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime, timedelta


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View

from django_journal.permissions import TeacherPermissionsMixin, TeacherLessonPermissionsMixin
from django_journal.settings import TEACHER
from people.models import User
from .models import GroupStudent, Score, Lesson,RatingItemStatus,LessonTopic,AttendanceScore
from utils.service import ScoreJournalMixin

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
#


class GroupStudentListView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    """Список классов/групп в школе."""
    template_name = 'journal/group_list.html'
    context_object_name = 'users_teachers'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager__grade').filter(user_status=TEACHER)
        return queryset


class GroupStudentDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
    """Информация о конкретном классе."""
    model = GroupStudent
    template_name = 'journal/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super(GroupStudentDetailView, self).get_context_data()
        context['students'] = User.objects.select_related('student__group')\
            .filter(student__group_id=self.kwargs['pk'])
        return context

class ScoreLessonListView(LoginRequiredMixin, TeacherLessonPermissionsMixin, ScoreJournalMixin, ListView):
    """Журнал оценок класса по предмету."""
    template_name = 'journal/journal_lesson_list.html'
    context_object_name = 'scores'
    permission_denied_message = 'В доступе отказанно'



    def get_queryset(self):
        group_student = GroupStudent.objects.select_related('grade')
        self.group = get_object_or_404(group_student, id=self.kwargs['group_id'])
        self.lesson = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])

        # Получаем ID учителя
        try:
            teacher_id = self.request.user.teacher.id
        except User.teacher.RelatedObjectDoesNotExist:
            teacher_id = None  # Если у пользователя нет связанного учителя, ставим None

        #print("Учитель ID:", teacher_id)  # Логирование ID учителя

        # Проверяем, является ли текущий пользователь администратором или руководителем класса
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Acer').exists():#self.request.user.is_staff:#
            # Если это администратор или руководитель класса, показываем все оценки
            queryset = Score.objects.select_related('group', 'lesson') \
                .filter(group=self.group, lesson=self.lesson)
        else:
            # Если это обычный учитель, показываем только его оценки
            queryset = Score.objects.select_related('group', 'lesson') \
                .filter(group=self.group, lesson=self.lesson, teacher_id=teacher_id)

        #print("Отфильтрованные оценки:", queryset)  # Логирование отфильтрованных оценок
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ScoreLessonListView, self).get_context_data(**kwargs)
        date_period = self.create_date_period_list()
        students = User.objects.filter(student__group=self.group)

        scores = self.get_queryset()  # Получаем только свои оценки
        lesson_topics_queryset = LessonTopic.objects.filter(lesson=self.lesson, date__in=date_period)
        lesson_topics = {topic.date: topic.topic for topic in lesson_topics_queryset}

        # Обновляем данные посещаемости
        attendance_scores = AttendanceScore.objects.filter(lesson=self.lesson)
        attendance_scores_dict = {record.student_id: record.score for record in attendance_scores}

        context["students"] = students
        context["attendance_scores"] = attendance_scores_dict
        context["date_period"] = date_period
        context["scores_dict"] = self.create_scores_dict(
            date_period,
            scores.values("id", "student", "score", "created"),
            students,
            "student",
        )
        context["group"] = self.group
        context["lesson"] = self.lesson
        context["lesson_topics"] = lesson_topics
        return context


@csrf_exempt
def add_attendance_score(request):
    if request.method == "POST":
        try:
            user_id = request.POST.get("student")
            attendance_value = request.POST.get("attendance")
            lesson_id = request.POST.get("lesson")

            if not (user_id and attendance_value and lesson_id):
                return JsonResponse({"error": "Недостаточно данных для сохранения оценки."}, status=400)

            user = User.objects.get(pk=user_id)
            lesson = Lesson.objects.get(pk=lesson_id)

            # Проверка, существует ли уже запись
            if AttendanceScore.objects.filter(student=user, lesson=lesson).exists():
                return JsonResponse({"error": "Оценка уже установлена и не может быть изменена."}, status=403)

            attendance, created = AttendanceScore.objects.update_or_create(
                student=user,
                lesson=lesson,
                defaults={"score": attendance_value}
            )
            return JsonResponse({"status": "success"})
        except User.DoesNotExist:
            return JsonResponse({"error": "Пользователь не найден."}, status=404)
        except Lesson.DoesNotExist:
            return JsonResponse({"error": "Урок не найден."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Неверный метод запроса."}, status=405)




class AddScore(LoginRequiredMixin, TeacherLessonPermissionsMixin, View):
    """Добавление оценки."""
    def post(self, request):
        score_id = request.POST.get('score_id')
        if score_id == '0':
            score_id = None

        teacher_id = request.user.teacher.id  # Получаем ID учителя

        # Логирование ID учителя
        #print("Учитель ID:", request.user.id)
        #print("ID учителя в базе:", teacher_id)

        score_params = {
            'score': request.POST.get('score_value'),
            'group_id': request.POST.get('group'),
            'lesson_id': request.POST.get('lesson'),
            'student_id': request.POST.get('student'),
            'teacher_id': teacher_id,
            'score_status_id': request.POST.get('score_status'),
            'created': request.POST.get('score_date'),
        }

        # Проверка, что оценка задана
        if score_params['score'] is not None:
            try:
                Score.objects.update_or_create(id=score_id, defaults=score_params)
                return JsonResponse({'status': 'ok'})
            except Exception as e:
                # Логирование ошибки
                #print(f"Ошибка при добавлении/обновлении оценки: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        else:
            if score_id:
                try:
                    Score.objects.get(id=score_id).delete()
                    return JsonResponse({'status': 'ok'})
                except Score.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Оценка не найдена.'}, status=404)
            return JsonResponse({'status': 'error', 'message': 'Оценка не указана.'}, status=400)

def save_lesson_topic(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        topic = request.POST.get('topic')
        lesson_id = request.POST.get('lesson')

        if date and lesson_id:
            lesson_topic,created = LessonTopic.objects.get_or_create(
                lesson_id=lesson_id,
                date=date
            )
            lesson_topic.topic = topic
            lesson_topic.save()

            return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'}, status=400)

#########
def export_scores_to_excel(request, group_id, lesson_id):
    # Получаем класс и предмет
    group = GroupStudent.objects.get(id=group_id)
    lesson = Lesson.objects.get(id=lesson_id)

    # Создаем заголовок листа и заменяем недопустимые символы
    sheet_title = f"{group.grade} - {lesson.name}"
    sheet_title = re.sub(r'[\/:*?"<>|]', '-', sheet_title)  # Замена недопустимых символов на дефис

    # Обрезаем заголовок листа до 31 символа
    if len(sheet_title) > 31:
        sheet_title = sheet_title[:31]

    # Создаем новую книгу Excel и рабочий лист
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = sheet_title

    # Устанавливаем заголовки для столбцов
    worksheet["A1"] = "ФИО студента"

    # Генерируем список всех дней в текущем месяце
    start_date = datetime.now().replace(day=1)
    end_date = start_date + timedelta(days=31)
    end_date = end_date.replace(day=1) - timedelta(days=1)
    date_period = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    # Добавляем даты в заголовки столбцов
    for col_num, date in enumerate(date_period, start=2):
        worksheet.cell(row=1, column=col_num, value=date.strftime('%Y-%m-%d'))

    # Получаем список студентов в группе
    students = User.objects.filter(student__group=group).order_by('last_name', 'first_name')

    # Добавляем имена студентов и их оценки
    for row_num, student in enumerate(students, start=2):
        worksheet.cell(row=row_num, column=1, value=f"{student.get_full_name()}")

        # Получаем оценки студента
        scores = Score.objects.filter(group=group, lesson=lesson, student=student)

        # Создаем словарь с оценками для быстрого доступа
        score_dict = {score.created: score.score for score in scores}

        # Заполняем оценки в соответствующие ячейки
        for col_num, date in enumerate(date_period, start=2):
            score_value = score_dict.get(date.date(), "--")  # Используем "--", если оценка отсутствует
            if score_value == -1:
                score_value = "q"
            elif score_value == -2:
                score_value = "İ"  # Заменяем -1 на НБif score_value == -1:

            worksheet.cell(row=row_num, column=col_num, value=score_value)
    # Настраиваем размеры столбцов
    for col_num in range(1, worksheet.max_column + 1):
        column_letter = get_column_letter(col_num)
        worksheet.column_dimensions[column_letter].width = 20

    # Создаем ответ с заголовком "Content-Disposition"
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{group.grade}-{lesson.name}.xlsx"'

    # Сохраняем рабочую книгу в память и прикрепляем к ответу
    with BytesIO() as buffer:
        workbook.save(buffer)
        buffer.seek(0)
        response.write(buffer.getvalue())

    return response


