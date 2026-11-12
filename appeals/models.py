from django.db import models
from django.utils import timezone
import uuid, os
import json


def appeal_file_upload_to(instance, filename):
    ext = filename.split('.')[-1].lower()
    return os.path.join('appeals', timezone.now().strftime('%Y/%m'), f'{uuid.uuid4().hex}.{ext}')


class Appeal(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('done', 'Рассмотрено'),
    ]

    full_name = models.CharField('ФИО', max_length=200)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email')
    address = models.CharField('Адрес', max_length=300)
    message = models.TextField('Суть обращения')
    files = models.TextField('Файлы (JSON)', blank=True, default='[]')

    consent_given = models.BooleanField('Согласие дано', default=False)
    consent_text_version = models.CharField('Версия согласия', max_length=20, blank=True)
    consent_ip = models.GenericIPAddressField('IP', blank=True, null=True)
    consent_user_agent = models.CharField('User-Agent', max_length=300, blank=True)

    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    email_sent = models.BooleanField('Письмо отправлено', default=False)
    sheet_row_id = models.CharField('ID строки в Google Sheets', max_length=100, blank=True)

    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self):
        return f'{self.full_name} — {self.created_at:%d.%m.%Y %H:%M}'