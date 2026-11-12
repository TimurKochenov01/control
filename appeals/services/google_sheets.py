import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def append_appeal_to_sheet(appeal):
    if not settings.GOOGLE_SHEETS_ID:
        return None
    creds = Credentials.from_service_account_file(
        str(settings.GOOGLE_CREDENTIALS_FILE), scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(settings.GOOGLE_SHEETS_ID).sheet1
    row = [
        appeal.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        appeal.full_name, appeal.phone, appeal.email, appeal.address,
        appeal.message, appeal.file.url if appeal.file else '',
        'да' if appeal.consent_given else 'нет',
        appeal.consent_text_version, appeal.consent_ip or '',
    ]
    result = sheet.append_row(row)
    return str(result.get('updates', {}).get('updatedRange', ''))