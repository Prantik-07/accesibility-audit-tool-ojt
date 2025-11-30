# Accessibility CMS - Web Accessibility Auditing Tool

A comprehensive Django-based web accessibility auditing tool designed to help teams track, manage, and improve website accessibility compliance. Features include automated auditing with pa11y integration, manual audit tracking, detailed reporting, and PDF export capabilities.

## ✨ Features

- **📊 Dashboard Overview** - Real-time statistics showing total pages, audits, and issues
- **📝 Pages Management** - Track and manage all pages under accessibility review
- **🔍 Manual & Automated Audits** - Support for both manual audits and automated pa11y integration
- **📈 Audit History** - Complete history of all accessibility audits with detailed issue tracking
- **📄 PDF Reports** - Generate professional PDF reports for audit results
- **🎨 Modern UI** - Clean, responsive interface built with Tailwind CSS
- **🔐 Secure Configuration** - Environment-based configuration for sensitive data

## 🛠️ Tech Stack

- **Backend**: Django 5.2.8
- **Frontend**: HTML Templates with Tailwind CSS
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **PDF Generation**: xhtml2pdf & ReportLab
- **Testing**: Selenium for automated testing
- **Accessibility Tools**: pa11y integration for automated audits

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Prantik-07/accesibility-audit-tool-ojt.git
cd accesibility-audit-tool-ojt
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root directory:

```bash
# Copy the example file
cp .env.example .env
```

Edit the `.env` file and set your configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Generate a new SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to access the application.

## 📁 Project Structure

```
accessibility_cms_completed/
├── accessibility_cms/      # Main project settings
│   ├── settings.py        # Django settings with environment variables
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI configuration
├── audit/                 # Main application
│   ├── models.py         # Database models (WebPage, AuditRecord, WCAGIssue)
│   ├── views.py          # View functions
│   ├── forms.py          # Django forms
│   ├── services.py       # Business logic and pa11y integration
│   ├── urls.py           # App URL patterns
│   └── management/       # Custom management commands
├── templates/            # HTML templates
│   └── audit/           # Audit app templates
│       ├── base.html    # Base template
│       ├── dashboard.html
│       ├── pages.html
│       ├── history.html
│       └── ...
├── static/              # Static files (CSS, JS, images)
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── manage.py           # Django management script
```

## 🎯 Usage

### Adding a New Page

1. Navigate to "Pages" from the dashboard
2. Click "Add New Page"
3. Enter page name and URL
4. Submit the form

### Running an Audit

1. Go to "New Audit" from the navigation
2. Select the page to audit
3. Choose audit type (Manual or pa11y)
4. For manual audits, enter issue count and notes
5. For automated audits, the system will run pa11y and capture results
6. Submit to save the audit

### Viewing Audit History

- Access "History" to see all past audits
- Click on any audit to view detailed WCAG issues
- Generate PDF reports for any audit

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test audit
```

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Always use environment variables for sensitive data
- Generate a unique SECRET_KEY for production
- Set `DEBUG=False` in production
- Configure proper `ALLOWED_HOSTS` for production deployment

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for better web accessibility**