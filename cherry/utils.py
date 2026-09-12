from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import EmailNotification


def send_achievement_email(award):
    """
    Отправляет email уведомление о выдаче ачивки
    """
    employee = award.employee
    user = employee.user

    if not user.email:
        print(f"У пользователя {user.username} нет email!")
        return False

    # Формируем тему и текст письма
    subject = f"🏆 Вы получили достижение: {award.achievement.name}"

    # Можно использовать шаблон или простой текст
    context = {
        "employee": employee,
        "award": award,
        "achievement": award.achievement,
    }

    # Простой текст письма (можно заменить на шаблон)
    body = f"""
Привет, {user.first_name or user.username}!

Поздравляем! Вам было выдано новое достижение в системе Magma.

🏆 {award.achievement.name}

{award.achievement.description}

Основание выдачи: {award.reason or "Не указано"}

Дата получения: {award.awarded_at.strftime("%d.%m.%Y")}

С уважением,
Команда Magma
    """

    # Отправляем email
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        # Сохраняем в историю
        EmailNotification.objects.create(
            recipient=user, subject=subject, body=body, is_sent=True
        )

        print(f"✅ Email отправлен пользователю {user.email}")
        return True

    except Exception as e:
        print(f" Ошибка отправки email: {e}")

        # Сохраняем неудачную попытку
        EmailNotification.objects.create(
            recipient=user, subject=subject, body=body, is_sent=False
        )

        return False
