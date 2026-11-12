from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AppealForm, CONSENT_VERSION
from .services.email_sender import send_appeal_email
from .services.google_sheets import append_appeal_to_sheet

def submit_appeal(request):
    if request.method == 'POST':
        form = AppealForm(request.POST, request.FILES)
        if form.is_valid():
            appeal = form.save(commit=False)
            appeal.consent_given = True
            appeal.consent_text_version = CONSENT_VERSION
            appeal.consent_ip = request.META.get('REMOTE_ADDR')
            appeal.consent_user_agent = request.META.get('HTTP_USER_AGENT', '')[:300]
            appeal.save()

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

            messages.success(request, 'Ваше обращение принято.')
            return redirect('pages:index')
        messages.error(request, 'Проверьте форму.')
    else:
        form = AppealForm()

    # ВАЖНО: передаем форму в контекст!
    return render(request, 'appeals/form_appeal.html', {'form': form})