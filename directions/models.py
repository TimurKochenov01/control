from django.db import models


class Direction(models.Model):
    title = models.CharField('Название', max_length=200)
    # ДОБАВЛЯЕМ blank=True:
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Картинка', upload_to='directions/', blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return self.title


    class Meta:
        ordering = ['order']
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return self.title