import json
import os
from django.conf import settings
from django.core.mail import EmailMessage


def send_appeal_email(appeal):
    subject = f'Новое обращение #{appeal.pk} — {appeal.full_name}'
    body = (
        f'ФИО: {appeal.full_name}\n'
        f'Телефон: {appeal.phone}\n'
        f'Email: {appeal.email}\n'
        f'Адрес: {appeal.address}\n'
        f'Дата: {appeal.created_at:%d.%m.%Y %H:%M}\n\n'
        f'Суть обращения:\n{appeal.message}\n\n'
        f'Согласие: {"да" if appeal.consent_given else "нет"} '
        f'(версия {appeal.consent_text_version})\n'
        f'IP: {appeal.consent_ip or "—"}\n'
    )
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.APPEAL_RECIPIENT_EMAIL],
    )

    # --- ПРИКРЕПЛЯЕМ ФАЙЛЫ ---
    if appeal.files:
        try:
            # Читаем JSON-список путей к файлам
            file_paths = json.loads(appeal.files)

            for path in file_paths:
                # Собираем полный путь к файлу на диске
                full_path = os.path.join(settings.MEDIA_ROOT, path)

                # Проверяем, существует ли файл, и прикрепляем его
                if os.path.exists(full_path):
                    with open(full_path, 'rb') as f:
                        # Берем только имя файла (без папок) для отображения в письме
                        filename = os.path.basename(path)
                        email.attach(filename, f.read())
        except Exception as e:
            print(f"Ошибка прикрепления файлов: {e}")

    email.send(fail_silently=False)