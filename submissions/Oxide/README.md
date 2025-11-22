# HackDucky - Browser Data Extraction Tool

A comprehensive browser data extraction and management tool with two main components: a victim-side data extractor and an admin-side web interface.

## 🚨 Security Notice

**This tool is for educational and authorized testing purposes only.** Always ensure you have proper authorization before extracting or viewing browser data. Unauthorized use may violate privacy laws and regulations.

## 📋 Overview

HackDucky consists of two main components:

1. **Victim Side (V)**: Python script that extracts browser data from Chrome and Edge browsers
2. **Admin Side**: Django web application for managing and viewing extracted data

## 🏗️ Project Structure

```
hackducky/
├── main.py                 # Main entry point
├── interactive-script.txt  # Rubber Ducky script
├── v/                      # Victim side (data extraction)
│   ├── main.py            # Victim script
│   ├── models.py          # Data models
│   ├── utils.py           # Utility functions
│   ├── requirements.txt   # Victim dependencies
│   └── README.md          # Victim documentation
└── admin/                  # Admin side (web interface)
    ├── admin/             # Django project
    ├── victim/            # Django app
    ├── manage.py          # Django management
    ├── requirements.txt   # Admin dependencies
    └── README.md          # Admin documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Windows OS (for victim script)
- Chrome or Edge browser installed
- Administrator privileges (for victim script)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd hackducky
```

2. **Install victim dependencies:**
```bash
cd v
pip install -r requirements.txt
cd ..
```

3. **Install admin dependencies:**
```bash
cd admin
pip install -r requirements.txt
cd ..
```

### Usage

#### Running the Victim Script

```bash
# Extract browser data
python main.py victim
```

The victim script will:
- Request administrator privileges
- Close Chrome and Edge browsers
- Extract passwords, cookies, and history
- Save results to `v/output.json`

#### Running the Admin Interface

```bash
# Start the web interface
python main.py admin
```

Or manually:
```bash
cd admin
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

The admin interface will be available at `http://localhost:8000`

## 🔧 Features

### Victim Side Features

- **Multi-browser Support**: Chrome and Edge
- **Data Extraction**:
  - Passwords (decrypted)
  - Cookies (with security flags)
  - Browser history
  - Profile pictures
- **Multi-profile Support**: Extracts from all browser profiles
- **Automatic Privilege Escalation**: Requests admin rights when needed
- **Secure Decryption**: Uses proper AES decryption for passwords
- **Automatic API Upload**: Automatically uploads data to admin interface when done

### Admin Side Features

- **Modern Web Interface**: Bootstrap-based responsive design
- **Dashboard**: Overview with statistics
- **Data Management**:
  - Browser profiles
  - Passwords with copy functionality
  - Cookies with security information
  - Browser history
- **Search & Filter**: Advanced search capabilities
- **Import/Export**: JSON data import/export
- **REST API**: Full API for programmatic access
- **Security Features**:
  - Password visibility toggle
  - Copy-to-clipboard functionality
  - Secure data handling

## 📊 Data Types Extracted

### Passwords
- URL
- Username
- Decrypted password
- Creation timestamp

### Cookies
- Name and value
- Host domain
- Security flags (Secure, HttpOnly)
- Expiration information
- Path and domain settings

### Browser History
- Page title
- URL
- Visit count
- Last visit timestamp

### Profile Information
- Profile name
- Browser type
- Profile picture (if available)

## 🔒 Security Considerations

### Data Protection
- Passwords are decrypted using proper AES algorithms
- Sensitive data is handled securely in the web interface
- Copy functionality prevents accidental exposure

### Access Control
- Admin interface provides controlled access to extracted data
- Search and filter capabilities for efficient data management
- Export functionality for authorized data sharing

### Legal Compliance
- Always obtain proper authorization before use
- Respect privacy laws and regulations
- Use only for educational or authorized testing purposes

## 🛠️ Technical Details

### Victim Script Dependencies
- `pycryptodomex`: For AES decryption
- `pywin32`: For Windows API access
- `pyuac`: For privilege escalation

### Admin Interface Dependencies
- `Django`: Web framework
- `Django REST Framework`: API framework
- `Pillow`: Image processing

### Browser Compatibility
- **Chrome**: Versions 80+ (AES encryption)
- **Edge**: Chromium-based versions
- **Windows**: All supported versions

## 📝 Usage Examples

### Basic Data Extraction
```bash
# Extract all browser data
python main.py victim
```

### View Extracted Data
```bash
# Start admin interface
python main.py admin
# Navigate to http://localhost:8000
```

### Import Data to Admin Interface
1. Run victim script to extract data (automatically uploads to API)
2. Open admin interface
3. View and manage extracted data
4. Or manually import using "Import Data" button

## 🐛 Troubleshooting

### Common Issues

1. **Permission Denied**: Run as administrator
2. **Browser in Use**: Close Chrome/Edge before running
3. **No Data Found**: Ensure browsers have saved data
4. **Import Failed**: Check if `v/output.json` exists

### Debug Mode
```bash
# Run with verbose output
cd v
python main.py --verbose
```

## 📄 License

This project is for educational purposes only. Users are responsible for ensuring compliance with applicable laws and regulations.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## ⚠️ Disclaimer

This tool is provided for educational and authorized testing purposes only. The authors are not responsible for any misuse or illegal activities. Users must ensure they have proper authorization before using this tool.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the individual component READMEs
3. Ensure you have proper authorization for use 