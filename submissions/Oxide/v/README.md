# HackDucky - Victim Side

This component extracts browser data from Chrome and Edge browsers on Windows systems.

## Features

- Extracts passwords from Chrome/Edge browsers
- Extracts cookies from browser databases
- Extracts browser history
- Extracts profile pictures
- Supports multiple browser profiles
- Runs with elevated privileges for database access

## Requirements

- Windows OS
- Python 3.7+
- Chrome or Edge browser installed
- Administrator privileges

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The script will:
1. Request administrator privileges if not already running as admin
2. Close Chrome and Edge browsers to unlock databases
3. Extract data from all available browser profiles
4. Save results to `output.json`

## Output Format

The script generates a JSON file with the following structure:

```json
[
  [
    {
      "name": "Profile 1",
      "profile_pic": "base64_encoded_image",
      "passwords": [
        {
          "index": 0,
          "url": "https://example.com",
          "username": "user@example.com",
          "password": "decrypted_password"
        }
      ],
      "cookies": [...],
      "history": [...]
    }
  ]
]
```

## Security Note

This tool is for educational and authorized testing purposes only. Always ensure you have proper authorization before extracting browser data. 