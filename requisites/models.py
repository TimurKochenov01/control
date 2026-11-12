from django.db import models

class Requisites(models.Model):
    about_text = models.TextField('Текст "О нас" (Устав)', blank=True, help_text='Краткая миссия организации для главной страницы')
    full_name = models.CharField('Полное наименование', max_length=300)
    ogrn = models.CharField('ОГРН', max_length=20, blank=True)
    inn = models.CharField('ИНН', max_length=20, blank=True)
    kpp = models.CharField('КПП', max_length=20, blank=True)
    reg_date = models.DateField('Дата регистрации', blank=True, null=True)
    legal_address = models.CharField('Юридический адрес', max_length=300, blank=True)
    actual_address = models.CharField('Фактический адрес', max_length=300, blank=True)
    bank_name = models.CharField('Банк', max_length=200, blank=True)
    bank_account = models.CharField('Расчётный счёт', max_length=30, blank=True)
    bik = models.CharField('БИК', max_length=20, blank=True)
    corr_account = models.CharField('Корсчёт', max_length=30, blank=True)
    director_name = models.CharField('ФИО руководителя', max_length=200, blank=True)
    director_position = models.CharField('Должность руководителя', max_length=200, blank=True)
    minjust_report_url = models.URLField('Отчёт в Минюст', blank=True)

    class Meta:
        verbose_name = 'Реквизиты'
        verbose_name_plural = 'Реквизиты'

    def __str__(self):
        return self.full_name

    @classmethod
    def load(cls):
        return cls.objects.first() or cls()


class Document(models.Model):
    title = models.CharField('Название', max_length=200)
    file = models.FileField('Файл (PDF)', upload_to='docs/')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.title
