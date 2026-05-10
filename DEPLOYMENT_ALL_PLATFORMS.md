# 🚀 Deployment Guide - All Platforms

## ✅ Supported Platforms

This application now supports **three deployment modes**:
1. **Local Development** - Run from source code
2. **Standalone EXE** - Windows executable (offline)
3. **Streamlit Cloud** - Web-based access (online)

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:
- [ ] All dependencies in `requirements.txt`
- [ ] `style.css` file exists in project root
- [ ] `i18n.py` contains all translations
- [ ] Database schema is up to date
- [ ] No hardcoded local paths in code

---

## 1️⃣ Local Development (localhost)

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

### Access
- **Local:** http://localhost:8501
- **LAN:** http://YOUR_IP:8501

### Configuration
Settings are in `.streamlit/config.toml`:
```toml
[server]
port = 8501
address = "0.0.0.0"  # Allow LAN access
```

---

## 2️⃣ Build Windows EXE

### Prerequisites
```bash
pip install pyinstaller
```

### Build Command
```bash
python build_exe.py
```

### Output Location
```
dist/WorkAttendanceApp/WorkAttendanceApp.exe
```

### Important Notes
- **Database Location:** Stored in `C:\Users\[YourName]\Documents\WorkAttendanceApp\attendance.db`
- **First Run:** May take 10-30 seconds to extract files
- **Anti-virus:** May flag as false positive (safe to ignore)
- **Permissions:** Run as Administrator if database permission errors occur

### macOS Build (Requires Mac)
```bash
python build_exe_mac.py
```
Output: `dist/WorkAttendanceApp/WorkAttendanceApp.app`

---

## 3️⃣ Deploy to Streamlit Cloud

### Step 1: Push to GitHub

```bash
# Initialize Git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Deploy to Streamlit Cloud"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Visit:** https://share.streamlit.io
2. **Sign in** with GitHub account
3. **Click:** "New app"
4. **Fill in:**
   ```
   Repository: YOUR_USERNAME/YOUR_REPO
   Branch: main
   Main file path: main.py
   App URL: workattendanceapp (or custom name)
   ```
5. **Click:** "Deploy!"
6. **Wait:** 2-3 minutes for deployment

### Your App URL
```
https://workattendanceapp.streamlit.app
```

---

## 🔧 Multi-Platform Support Details

### Resource Path Handling

The application automatically detects the environment and loads resources correctly:

#### `main.py` - CSS Loading
```python
def get_resource_path(filename):
    # Streamlit Cloud detection
    if '/home/appuser' in os.getcwd() or '/mount/src' in os.getcwd():
        return os.path.join(os.getcwd(), filename)
    
    # Frozen EXE detection
    if getattr(sys, 'frozen', False):
        # Use _internal folder
        ...
    
    # Local development
    else:
        # Use script directory
        ...
```

#### `database.py` - Database Location
```python
def get_database_path():
    # Streamlit Cloud: Current directory
    if '/home/appuser' in os.getcwd() or '/mount/src' in os.getcwd():
        return os.path.join(os.getcwd(), "attendance.db")
    
    # Frozen EXE: User's Documents/AppData
    if getattr(sys, 'frozen', False):
        # Windows: ~/Documents/WorkAttendanceApp
        # macOS: ~/Library/Application Support/WorkAttendanceApp
        ...
    
    # Local development: Project directory
    else:
        return os.path.join(os.getcwd(), "attendance.db")
```

---

## 📊 Database Considerations

### Local & EXE
- ✅ Database persists between sessions
- ✅ Full read/write access
- ⚠️ Backup regularly: Copy `attendance.db` to safe location

### Streamlit Cloud (Free Tier)
- ✅ Database persists during session
- ⚠️ Database resets on redeployment
- ⚠️ Max file size: 200MB
- 💡 **Solution:** Use Excel import/export for data backup

### For Production (Streamlit Cloud)
Consider upgrading to:
1. **Streamlit Cloud Pro** - Persistent storage
2. **External Database** - PostgreSQL/MySQL
3. **Self-hosted** - Docker + cloud server

---

## 🐛 Troubleshooting

### Issue: Missing Buttons/UI on Streamlit Cloud

**Symptoms:**
- Page loads but buttons don't appear
- Styling looks broken
- No error messages

**Solution:**
✅ Already fixed! The `get_resource_path()` function now detects Streamlit Cloud.

If issue persists:
1. Check Streamlit Cloud logs
2. Verify `style.css` is in GitHub repository
3. Redeploy the app

### Issue: Database Permission Error (EXE)

**Error Message:**
```
資料庫資料夾沒有寫入權限！
```

**Solutions:**
1. Move app to Documents folder
2. Run as Administrator
3. Grant folder permissions manually

### Issue: App Won't Start (Local)

**Check:**
1. Python version: `python --version` (need 3.8+)
2. Dependencies: `pip install -r requirements.txt`
3. Port availability: Ensure port 8501 is free

### Issue: Streamlit Cloud Shows Empty Database

**This is NORMAL!** 
- Database auto-initializes on first run
- You need to add data manually or use Excel import
- Don't commit `attendance.db` to GitHub (it's gitignored)

---

## 📁 Project Structure

```
WorkAttendanceApp/
├── main.py                 # Main application (multi-platform)
├── database.py             # Database manager (auto-detects environment)
├── i18n.py                 # Internationalization
├── style.css               # Custom styles (loaded dynamically)
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── build_exe.py           # Windows build script
├── build_exe_mac.py       # macOS build script
└── attendance.db          # SQLite database (auto-created, gitignored)
```

---

## 🔄 Updating Deployments

### Update Local
```bash
git pull
streamlit run main.py
```

### Update EXE
```bash
git pull
python build_exe.py
# Distribute new EXE to users
```

### Update Streamlit Cloud
```bash
git add .
git commit -m "Update description"
git push
# Auto-deploys within 1-2 minutes!
```

---

## 📞 Support & Resources

- **Documentation:** See README.md
- **Issues:** Report on GitHub
- **Streamlit Docs:** https://docs.streamlit.io
- **Community:** https://discuss.streamlit.io

---

## ✅ Verification Checklist

After deployment, verify:

### Local/EXE
- [ ] App starts without errors
- [ ] All pages load correctly
- [ ] Can add/edit/delete companies
- [ ] Can add/edit/delete workers
- [ ] Can add/edit/delete sites
- [ ] Can record attendance
- [ ] Data persists after restart
- [ ] Excel import/export works

### Streamlit Cloud
- [ ] App loads at provided URL
- [ ] All buttons visible
- [ ] Styling appears correct
- [ ] Can navigate between pages
- [ ] Can add data (companies, workers, etc.)
- [ ] Data persists after page refresh
- [ ] Excel import/export works

---

**Last Updated:** 2026-05-10  
**Version:** 1.0.0
