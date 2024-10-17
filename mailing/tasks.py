# from django_journal.celery import app
#
#
# @app.task
# def send_notification(user_email):
#     """
#     Тестовая функция заглушка.
#     Предназначена для отправки email\sms\message по контактным данным пользователя.
#     Рассылку сообщений инициирует учитель.
#     """
#     return user_email
# from django.core.mail import send_mail
# from django.conf import settings
# from celery import shared_task
#
# @shared_task
# def send_notification(user_email):
#     """
#     Отправка уведомления на указанный email.
#     """
#     try:
#         subject = "Уведомление из электронного журнала"
#         message = "Вы получили новое уведомление от учителя."
#         from_email = settings.DEFAULT_FROM_EMAIL  # Убедитесь, что это настроено в settings.py
#
#         # Отправляем письмо
#         send_mail(subject, message, from_email, [user_email])
#     except Exception as e:
#         # Логируем ошибку, если отправка не удалась
#         print(f"Ошибка отправки email на {user_email}: {e}")
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

@shared_task
def send_notification(user_email, subject, message):
    """
    Отправка уведомления на указанный email.
    """
    try:
        from_email = settings.DEFAULT_FROM_EMAIL  # Убедитесь, что это настроено в settings.py

        # Отправляем письмо
        send_mail(subject, message, from_email, [user_email])
    except Exception as e:
        # Логируем ошибку, если отправка не удалась
        print(f"Ошибка отправки email на {user_email}: {e}")

