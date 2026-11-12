from django.urls import path
from . import views

app_name = 'appeals'

urlpatterns = [
    path('submit/', views.submit_appeal, name='submit'),
]