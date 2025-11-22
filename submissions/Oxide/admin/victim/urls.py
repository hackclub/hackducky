from django.urls import path
from . import views

app_name = 'victim'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profiles/', views.profiles_list, name='profiles_list'),
    path('profiles/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('passwords/', views.passwords_list, name='passwords_list'),
    path('cookies/', views.cookies_list, name='cookies_list'),
    path('history/', views.history_list, name='history_list'),
    path('import/', views.import_data, name='import_data'),
    path('export/', views.export_data, name='export_data'),
    path('export/<int:profile_id>/', views.export_data, name='export_profile_data'),
    path('api-docs/', views.api_docs, name='api_docs'),
]