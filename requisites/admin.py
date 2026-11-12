from django.contrib import admin
from .models import Requisites, Document

@admin.register(Requisites)
class RequisitesAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not Requisites.objects.exists()

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
