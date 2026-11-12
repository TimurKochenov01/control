from django.shortcuts import render, redirect
from django.contrib import messages
from appeals.forms import AppealForm, CONSENT_VERSION
from appeals.services.email_sender import send_appeal_email
from appeals.services.google_sheets import append_appeal_to_sheet

from django.shortcuts import render, redirect
from django.contrib import messages
from appeals.forms import AppealForm, CONSENT_VERSION
from appeals.services.email_sender import send_appeal_email
from appeals.services.google_sheets import append_appeal_to_sheet


def index(request):
    if request.method == 'POST':
        # Передаем данные из POST и файлы из FILES
        form = AppealForm(request.POST, request.FILES)

        if form.is_valid():
            appeal = form.save(commit=False)
            appeal.consent_given = True
            appeal.consent_text_version = CONSENT_VERSION
            appeal.consent_ip = request.META.get('REMOTE_ADDR')
            appeal.consent_user_agent = request.META.get('HTTP_USER_AGENT', '')[:300]

            # Обработка множественных файлов
            uploaded_files = request.FILES.getlist('files')
            saved_paths = []

            if uploaded_files:
                import uuid, os
                from django.conf import settings

                # Папка media/appeals
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'appeals')
                os.makedirs(upload_dir, exist_ok=True)

                for f in uploaded_files:
                    ext = f.name.split('.')[-1].lower()
                    new_name = f"{uuid.uuid4().hex}.{ext}"
                    file_path = os.path.join(upload_dir, new_name)

                    with open(file_path, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)

                    saved_paths.append(f"appeals/{new_name}")

            import json
            appeal.files = json.dumps(saved_paths)
            appeal.save()

            # ... (дальше идет отправка email и google_sheets) ...

            try:
                send_appeal_email(appeal)
                appeal.email_sent = True
            except Exception:
                pass
            try:
                appeal.sheet_row_id = append_appeal_to_sheet(appeal) or ''
            except Exception:
                pass
            appeal.save(update_fields=['email_sent', 'sheet_row_id'])

            messages.success(request, 'Ваше обращение успешно принято! Мы свяжемся с вами.')
            return redirect('/#appeal')

        else:
            # ЕСЛИ ОШИБКА: мы НЕ делаем редирект, а рендерим страницу заново,
            # передавая туда форму с уже введенными данными и ошибками
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            return render(request, 'pages/index.html', {'form': form})

    else:
        form = AppealForm()

    return render(request, 'pages/index.html', {'form': form})


def privacy_policy(request):
    return render(request, 'pages/privacy.html')


def consent_full(request):
    return render(request, 'pages/consent_full.html')