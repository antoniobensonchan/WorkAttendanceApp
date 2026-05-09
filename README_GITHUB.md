# Work Attendance Management System 📋

A modern, multi-language work attendance management system built with Streamlit. Track employee attendance across multiple construction sites with an intuitive, Apple-inspired interface.

![License](https://img.shields.io/badge/license-Internal-use-orange)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red)

## ✨ Features

- **Multi-company Management**: Manage multiple companies and their employees
- **Site Tracking**: Track attendance across multiple construction sites
- **Flexible Scheduling**: Morning, afternoon, and evening shifts with overtime tracking
- **Absent Reasons**: Customizable absence reason categories
- **Statistics & Reports**: Comprehensive worker and site statistics
- **Excel Import/Export**: Bulk data import and export functionality
- **Multi-language Support**: Currently supports Chinese (Simplified) and English
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Option 1: Web Deployment (Recommended)

Deploy to Streamlit Cloud for instant web access:

```bash
# Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# Then deploy at: https://share.streamlit.io
```

**Live Demo:** [Your App URL will appear here]

### Option 2: Run Locally

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd WorkAttendanceApp

# Create virtual environment
python -m venv .venv

# Activate
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run main.py
```

Access at: http://localhost:8501

### Option 3: Build Desktop App

**Windows:**
```bash
python build_exe.py
```

**macOS:**
```bash
python build_exe_mac.py
```

## 📸 Screenshots

*Add screenshots here after deployment*

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.8+
- **Database:** SQLite
- **Data Processing:** Pandas, OpenPyXL
- **Styling:** Custom CSS with Material Design principles

## 📁 Project Structure

```
WorkAttendanceApp/
├── main.py                 # Main application entry point
├── database.py             # Database management layer
├── i18n.py                 # Internationalization support
├── style.css               # Custom styling
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── build_exe.py           # Windows build script
├── build_exe_mac.py       # macOS build script
└── DEPLOYMENT.md          # Detailed deployment guide
```

## 🌍 Multi-language Support

The application currently supports:
- 🇨🇳 Chinese (Simplified) - 简体中文
- 🇬🇧 English

To add more languages, edit `i18n.py`.

## 📊 Database

The application uses SQLite for data storage. The database file (`attendance.db`) is automatically created on first run.

### Tables:
- `companies` - Company information
- `workers` - Employee records
- `sites` - Construction sites
- `absent_reasons` - Absence categories
- `attendance` - Daily attendance records

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server port
- Browser settings

## 📝 Usage Guide

### Adding Companies
1. Navigate to "Companies" in sidebar
2. Click "Add Company"
3. Enter company name

### Managing Workers
1. Go to "Workers" section
2. Add workers and assign to companies
3. Edit or delete as needed

### Recording Attendance
1. Select "Attendance" from menu
2. Choose date and worker
3. Assign sites for morning/afternoon/evening shifts
4. Record overtime hours if applicable

### Viewing Statistics
- **Worker Stats:** Overall attendance by worker
- **Site Stats:** Daily worker counts per site
- **Individual Worker:** Detailed calendar view

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Change port in .streamlit/config.toml
[server]
port = 8502
```

**Database permission errors (EXE):**
- Move application to Documents folder
- Run as Administrator (Windows)

**App won't start:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for more troubleshooting tips.

## 🤝 Contributing

This is an internal company project. For questions or issues, contact the development team.

## 📄 License

Internal use only - Not for public distribution.

## 📞 Support

For technical support or feature requests, please contact:
- Development Team
- IT Department

---

**Built with ❤️ using Streamlit**
