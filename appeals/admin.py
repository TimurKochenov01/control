from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import json
from .models import Appeal


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'created_at', 'status', 'email_sent')
    list_filter = ('status', 'created_at', 'email_sent')
    search_fields = ('full_name', 'phone', 'email', 'message')

    # Поля, которые нельзя редактировать (только читать)
    readonly_fields = (
        'consent_given', 'consent_text_version',
        'consent_ip', 'consent_user_agent', 'created_at',
        'media_preview'  # <-- Наша новая функция для просмотра
    )

    fieldsets = (
        ('Заявитель', {'fields': ('full_name', 'phone', 'email', 'address')}),
        ('Обращение', {'fields': ('message', 'files', 'media_preview', 'status')}),  # <-- Выводим preview после files
        ('Согласие (152-ФЗ)', {'fields': ('consent_given', 'consent_text_version',
                                          'consent_ip', 'consent_user_agent')}),
        ('Служебное', {'fields': ('email_sent', 'sheet_row_id', 'created_at')}),
    )

    # Функция для красивого отображения фото и видео
    def media_preview(self, obj):
        if not obj.files:
            return "Файлы не прикреплены"

        try:
            # Читаем JSON-строку и превращаем её в список путей
            file_paths = json.loads(obj.files)
        except:
            return "Ошибка чтения файлов"

        if not file_paths:
            return "Файлы не прикреплены"

        html_output = ""
        for path in file_paths:
            # Формируем правильный URL (предполагая, что медиа доступно по /media/)
            file_url = f"/media/{path}"
            file_name = path.lower()

            # 1. Если это ФОТО
            if file_name.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                html_output += format_html(
                    '<a href="{}" target="_blank">'
                    '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 8px; margin: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 2px solid #ddd;" />'
                    '</a>',
                    file_url, file_url
                )

            # 2. Если это ВИДЕО
            elif file_name.endswith(('.mp4', '.webm', '.mov')):
                html_output += format_html(
                    '<video controls style="max-width: 300px; max-height: 200px; border-radius: 8px; margin: 5px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">'
                    '<source src="{}" type="video/mp4">'
                    'Ваш браузер не поддерживает видео.'
                    '</video>',
                    file_url
                )

            # 3. Если это PDF
            elif file_name.endswith('.pdf'):
                html_output += format_html(
                    '<div style="margin: 5px;"><a href="{}" target="_blank" style="background: #2B6CB0; color: white; padding: 8px 15px; border-radius: 5px; text-decoration: none;">📄 Открыть PDF</a></div>',
                    file_url
                )

            # 4. Другие файлы
            else:
                html_output += format_html(
                    '<div style="margin: 5px;"><a href="{}" target="_blank" style="background: #A97E39; color: white; padding: 8px 15px; border-radius: 5px; text-decoration: none;">📎 Скачать файл</a></div>',
                    file_url
                )

        return mark_safe(html_output)

    media_preview.short_description = 'Предпросмотр прикрепленных файлов'