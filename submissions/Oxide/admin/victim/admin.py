from django.contrib import admin
from .models import BrowserProfile, Password, Cookie, HistoryEntry

@admin.register(BrowserProfile)
class BrowserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'browser_type', 'created_at', 'updated_at']
    list_filter = ['browser_type', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ['username', 'url', 'browser_profile', 'created_at']
    list_filter = ['browser_profile__browser_type', 'created_at']
    search_fields = ['username', 'url']
    readonly_fields = ['created_at']
    list_select_related = ['browser_profile']

@admin.register(Cookie)
class CookieAdmin(admin.ModelAdmin):
    list_display = ['name', 'host_key', 'browser_profile', 'is_secure', 'is_httponly']
    list_filter = ['is_secure', 'is_httponly', 'browser_profile__browser_type']
    search_fields = ['name', 'host_key', 'value']
    readonly_fields = ['creation_utc', 'last_access_utc', 'last_update_utc']
    list_select_related = ['browser_profile']

@admin.register(HistoryEntry)
class HistoryEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'browser_profile', 'visit_count', 'last_visit_time']
    list_filter = ['browser_profile__browser_type']
    search_fields = ['title', 'url']
    readonly_fields = ['created_at']
    list_select_related = ['browser_profile']