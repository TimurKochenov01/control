from django.conf import settings
from directions.models import Direction
from requisites.models import Requisites, Document
from contacts.models import ContactInfo

def site_settings(request):
    return {
        'ORG': Requisites.load(),
        'CONTACTS': ContactInfo.load(),
        'DOCUMENTS': Document.objects.filter(is_active=True),
        'DIRECTIONS': Direction.objects.filter(is_active=True),
        'YM_ID': settings.YANDEX_METRIKA_ID,
    }