from django import template
from django.core.exceptions import ObjectDoesNotExist
from people.models import Teacher, User

register = template.Library()

@register.inclusion_tag('people/tpl/student_sidebar_tpl.html', name='student_sidebar')
def student_sidebar(user):
    """Формирует сайдбар для студента."""
    try:
        # Получаем группу студента
        group_student = user.student  # Прямо получаем связанный объект
        # Получаем менеджера группы
        user_group_manager = User.objects.select_related('teacher')\
            .get(teacher__group_manager=group_student.group_id)
        return {'user': user, 'user_group_manager': user_group_manager}
    except ObjectDoesNotExist:
        # Возвращаем пустые данные или обработайте как-то иначе
        return {'user': user, 'user_group_manager': None}

@register.inclusion_tag('people/tpl/teacher_sidebar_tpl.html', name='teacher_sidebar')
def teacher_sidebar(user):
    """Формирует сайдбар для учителя."""
    try:
        teacher = Teacher.objects.get(user=user.id)
        return {'teacher': teacher, 'user': user}
    except Teacher.DoesNotExist:
        # Если учитель не найден, возвращаем пустые данные или обрабатываем ошибку
        return {'teacher': None, 'user': user}
