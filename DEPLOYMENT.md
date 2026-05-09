# Work Attendance Management System - Deployment Guide

## 🚀 Quick Start

### Option 1: Deploy to Streamlit Cloud (Recommended for Web Access)

**Best for:** Team access from anywhere, no installation needed

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `main.py`
   - Click "Deploy!"

3. **Access Your App**
   - URL: `https://your-app-name.streamlit.app`
   - Works on Windows, Mac, Linux, mobile!

---

### Option 2: Build Windows EXE

**Best for:** Offline use, Windows-only environments

```bash
python build_exe.py
```

Output: `dist/WorkAttendanceApp/WorkAttendanceApp.exe`

---

### Option 3: Build macOS App (Requires Mac)

**Best for:** Mac users, offline use

1. **Transfer project to Mac**
2. **Install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. **Build:**
   ```bash
   python build_exe_mac.py
   ```

Output: `dist/WorkAttendanceApp/WorkAttendanceApp.app`

---

### Option 4: Run from Source (All Platforms)

**Best for:** Development, testing

```bash
pip install -r requirements.txt
streamlit run main.py
```

Access: http://localhost:8501

---

## 📁 Project Structure

```
WorkAttendanceApp/
├── main.py                 # Main application
├── database.py             # Database management
├── i18n.py                 # Internationalization
├── style.css               # Custom styles
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── build_exe.py           # Windows build script
├── build_exe_mac.py       # macOS build script
└── attendance.db          # SQLite database (auto-created)
```

---

## 🌐 Streamlit Cloud Deployment Details

### Database Considerations

- **Free tier:** Database persists but resets on redeployment
- **File uploads:** Max 200MB per file
- **Performance:** App sleeps after inactivity (~30s wake-up time)

### For Production Use

Consider upgrading to:
- **Streamlit Cloud Pro:** Persistent storage
- **External database:** PostgreSQL, MySQL
- **Self-hosted:** Docker + cloud server

---

## 🖥️ Local Development

### Prerequisites

- Python 3.8+
- pip

### Setup

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

# Run app
streamlit run main.py
```

---

## 🔧 Configuration

### Streamlit Settings (.streamlit/config.toml)

```toml
[theme]
base = "light"
primaryColor = "#14b8a6"

[server]
port = 8501
address = "0.0.0.0"  # Allow LAN access
```

### Multi-language Support

The app supports:
- Chinese (Simplified) - 简体中文
- English
- Add more in `i18n.py`

---

## 📊 Database Management

### Backup

```bash
# Copy attendance.db to backup location
cp attendance.db attendance_backup_$(date +%Y%m%d).db
```

### Reset Database

Delete `attendance.db` and restart the app to create fresh database.

---

## 🐛 Troubleshooting

### App Won't Start

1. Check Python version: `python --version` (need 3.8+)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check port 8501 is not in use

### Database Permission Errors (EXE)

- Move app to Documents folder
- Run as Administrator (Windows)
- Check folder permissions

### Streamlit Cloud Issues

1. Check logs in Streamlit Cloud dashboard
2. Verify all dependencies in requirements.txt
3. Ensure no local file paths are hardcoded

---

## 📞 Support

For issues or questions:
1. Check this guide
2. Review error messages in console
3. Open issue on GitHub

---

## 📝 License

This project is for internal company use.
