from django.urls import path
from .api_views import (
    DataUploadView, ProfileListView, ProfileDetailView,
    PasswordListView, CookieListView, HistoryListView, api_status
)

app_name = 'api'

urlpatterns = [
    path('upload/', DataUploadView.as_view(), name='upload'),
    
    path('profiles/', ProfileListView.as_view(), name='profiles'),
    path('profiles/<int:profile_id>/', ProfileDetailView.as_view(), name='profile_detail'),
    
    path('passwords/', PasswordListView.as_view(), name='passwords'),
    path('cookies/', CookieListView.as_view(), name='cookies'),
    path('history/', HistoryListView.as_view(), name='history'),
    
    path('status/', api_status, name='status'),
]