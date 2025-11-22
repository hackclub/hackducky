from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import BrowserProfile, Password, Cookie, HistoryEntry
from .serializers import (
    BrowserProfileSerializer, PasswordSerializer, 
    CookieSerializer, HistoryEntrySerializer, DataUploadSerializer
)

class DataUploadView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = DataUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                result = serializer.create(serializer.validated_data)
                return Response({
                    'status': 'success',
                    'message': f'Successfully imported {result["count"]} profiles',
                    'profiles_imported': result['count']
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'status': 'error',
                    'message': f'Error processing data: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid data format',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ProfileListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        profiles = BrowserProfile.objects.all()
        serializer = BrowserProfileSerializer(profiles, many=True)
        return Response({
            'status': 'success',
            'profiles': serializer.data,
            'count': len(serializer.data)
        })

class ProfileDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, profile_id):
        profile = get_object_or_404(BrowserProfile, id=profile_id)
        serializer = BrowserProfileSerializer(profile)
        return Response({
            'status': 'success',
            'profile': serializer.data
        })

class PasswordListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        passwords = Password.objects.select_related('browser_profile').all()
        
        profile_id = request.query_params.get('profile_id')
        if profile_id:
            passwords = passwords.filter(browser_profile_id=profile_id)
        
        browser_type = request.query_params.get('browser_type')
        if browser_type:
            passwords = passwords.filter(browser_profile__browser_type=browser_type)
        
        serializer = PasswordSerializer(passwords, many=True)
        return Response({
            'status': 'success',
            'passwords': serializer.data,
            'count': len(serializer.data)
        })

class CookieListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        cookies = Cookie.objects.select_related('browser_profile').all()
        
        profile_id = request.query_params.get('profile_id')
        if profile_id:
            cookies = cookies.filter(browser_profile_id=profile_id)
        
        serializer = CookieSerializer(cookies, many=True)
        return Response({
            'status': 'success',
            'cookies': serializer.data,
            'count': len(serializer.data)
        })

class HistoryListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        history = HistoryEntry.objects.select_related('browser_profile').all()
        
        profile_id = request.query_params.get('profile_id')
        if profile_id:
            history = history.filter(browser_profile_id=profile_id)
        
        serializer = HistoryEntrySerializer(history, many=True)
        return Response({
            'status': 'success',
            'history': serializer.data,
            'count': len(serializer.data)
        })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    total_profiles = BrowserProfile.objects.count()
    total_passwords = Password.objects.count()
    total_cookies = Cookie.objects.count()
    total_history = HistoryEntry.objects.count()
    
    return Response({
        'status': 'success',
        'data': {
            'total_profiles': total_profiles,
            'total_passwords': total_passwords,
            'total_cookies': total_cookies,
            'total_history': total_history,
        }
    })