from django.db import models
import json

# Create your models here.

class BrowserProfile(models.Model):
    name = models.CharField(max_length=150)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    browser_type = models.CharField(max_length=50, default='Chrome')  # Chrome or Edge
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.browser_type} - {self.name}"

    class Meta:
        ordering = ['-created_at']

class Password(models.Model):
    browser_profile = models.ForeignKey(BrowserProfile, on_delete=models.CASCADE, related_name='passwords')
    url = models.URLField(max_length=500)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}@{self.url}"

    class Meta:
        ordering = ['-created_at']

class Cookie(models.Model):
    browser_profile = models.ForeignKey(BrowserProfile, on_delete=models.CASCADE, related_name='cookies')
    creation_utc = models.BigIntegerField()
    host_key = models.CharField(max_length=100)
    top_frame_site_key = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=1000)
    encrypted_value = models.CharField(max_length=1000, blank=True)
    path = models.CharField(max_length=100)
    expires_utc = models.BigIntegerField()
    is_secure = models.BooleanField()
    is_httponly = models.BooleanField()
    last_access_utc = models.BigIntegerField()
    has_expires = models.BooleanField()
    is_persistent = models.BooleanField()
    priority = models.IntegerField()
    samesite = models.IntegerField()
    source_scheme = models.IntegerField()
    source_port = models.IntegerField()
    is_same_party = models.BooleanField()
    last_update_utc = models.BigIntegerField()
    is_edgelegacycookie = models.BooleanField()
    browser_provenance = models.IntegerField()

    def __str__(self):
        return f"{self.name}@{self.host_key}"

    class Meta:
        ordering = ['-last_access_utc']

class HistoryEntry(models.Model):
    browser_profile = models.ForeignKey(BrowserProfile, on_delete=models.CASCADE, related_name='history')
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=500)
    visit_count = models.IntegerField(default=1)
    last_visit_time = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_visit_time']
        verbose_name_plural = "History entries"