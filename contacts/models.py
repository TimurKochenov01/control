from django.db import models

class ContactInfo(models.Model):
    legal_address = models.CharField('Юридический адрес', max_length=300, blank=True)
    actual_address = models.CharField('Фактический адрес', max_length=300, blank=True)
    phone = models.CharField('Телефон', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    social_vk = models.URLField('ВКонтакте', blank=True)
    social_tg = models.URLField('Telegram', blank=True)
    social_ok = models.URLField('Одноклассники', blank=True)
    yandex_map_url = models.URLField(
        'Ссылка на Яндекс.Карту (widget)',
        blank=True,
        help_text='Например: https://yandex.ru/map-widget/v1/?text=Владикавказ%20Тургеневская%20415',
    )

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return 'Контактная информация'

    @classmethod
    def load(cls):
        return cls.objects.first() or cls()
