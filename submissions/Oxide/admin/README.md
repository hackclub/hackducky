# HackDucky - Admin Side

A Django web application for managing and viewing browser data extracted by the victim script.

## Features

- **Dashboard**: Overview of extracted data with statistics
- **Browser Profiles**: View and manage browser profiles
- **Passwords**: Browse and search extracted passwords with copy functionality
- **Cookies**: View and search browser cookies
- **History**: Browse browser history entries
- **Import/Export**: Import data from victim script and export as JSON
- **Search & Filter**: Advanced search and filtering capabilities
- **Responsive UI**: Modern Bootstrap-based interface

## Installation

1. Navigate to the admin directory:
```bash
cd admin
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

### Importing Data

1. First, run the victim script to extract browser data:
```bash
python main.py victim
```

2. In the admin interface, click "Import Data" to import the extracted data from `v/output.json`

### Viewing Data

- **Dashboard**: Overview of all extracted data
- **Browser Profiles**: View individual browser profiles with their associated data
- **Passwords**: Search and view extracted passwords with copy functionality
- **Cookies**: Browse browser cookies with security information
- **History**: View browser history entries

### Exporting Data

- Use the export buttons to download data as JSON
- Export all data or specific profile data

## Security Features

- Passwords are hidden by default with toggle visibility
- Copy-to-clipboard functionality for easy access
- Secure handling of sensitive data
- Admin interface for advanced management

## File Structure

```
admin/
├── admin/                 # Django project settings
├── victim/               # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── admin.py          # Django admin interface
│   ├── urls.py           # URL routing
│   └── templates/        # HTML templates
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Security Note

This tool is for educational and authorized testing purposes only. Always ensure you have proper authorization before extracting or viewing browser data. 