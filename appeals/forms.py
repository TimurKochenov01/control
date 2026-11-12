from django import forms
from django.core.exceptions import ValidationError
from .models import Appeal

CONSENT_VERSION = '1.0'


from django import forms
from django.core.exceptions import ValidationError
from .models import Appeal

CONSENT_VERSION = '1.0'

# 1. Создаем виджет, который разрешает выбор нескольких файлов
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# 2. Создаем поле, которое умеет обрабатывать список файлов
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class AppealForm(forms.ModelForm):
    # 3. Используем наше новое поле вместо стандартного
    files = MultipleFileField(
        required=False,
        label='Прикрепить файлы'
    )

    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True,
        error_messages={'required': 'Необходимо дать согласие на обработку ПДн'},
    )

    class Meta:
        model = Appeal
        fields = ['full_name', 'phone', 'email', 'address', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@mail.ru'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес места жительства'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Опишите суть обращения'}),
        }

    # ... (ваши методы clean_phone и clean_files оставьте без изменений) ...

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if phone.startswith('+7') and len(digits) != 11:
            raise ValidationError('Номер в формате +7 должен содержать 11 цифр')
        elif phone.startswith('8') and len(digits) != 11:
            raise ValidationError('Номер в формате 8 должен содержать 11 цифр')
        elif not phone.startswith(('+7', '8')) and len(digits) != 11:
            raise ValidationError('Укажите корректный номер телефона (11 цифр)')
        return phone

    # Валидация файлов
    def clean_files(self):
        files = self.files.getlist('files')
        if not files:
            return []

        allowed_types = ('image/jpeg', 'image/png', 'image/webp', 'video/mp4', 'video/quicktime')

        for f in files:
            if f.content_type not in allowed_types:
                raise ValidationError(f'Файл "{f.name}" имеет недопустимый формат.')
            if f.size > 50 * 1024 * 1024:
                raise ValidationError(f'Файл "{f.name}" превышает 50 МБ.')

        return files