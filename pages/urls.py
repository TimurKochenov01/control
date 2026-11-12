from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('policy/privacy/', views.privacy_policy, name='privacy'),
    path('policy/consent/', views.consent_full, name='consent_full'),
]