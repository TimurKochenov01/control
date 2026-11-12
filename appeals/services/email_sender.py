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
    if appeal.file:
        appeal.file.open('rb')
        email.attach(appeal.file.name.split('/')[-1], appeal.file.read())
        appeal.file.close()
    email.send(fail_silently=False)