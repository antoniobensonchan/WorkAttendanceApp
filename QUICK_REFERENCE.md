# ⚡ Quick Reference Card

## 🚀 Deploy to Web (3 Steps)

```bash
# 1. Initialize Git
setup_git.bat

# 2. Push to GitHub (replace URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main

# 3. Deploy at https://share.streamlit.io
```

---

## 💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run main.py
```

Access: http://localhost:8501

---

## 📦 Build Windows EXE

```bash
python build_exe.py
```

Output: `dist/WorkAttendanceApp/WorkAttendanceApp.exe`

---

## 🍎 Build Mac App (On Mac)

```bash
pip install pyinstaller
python build_exe_mac.py
```

Output: `dist/WorkAttendanceApp/WorkAttendanceApp.app`

---

## 🔄 Update Web App

```bash
git add .
git commit -m "Your changes"
git push
# Auto-deploys in 1-2 minutes!
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `main.py` | Main application |
| `database.py` | Database layer |
| `requirements.txt` | Dependencies |
| `.gitignore` | Git exclusions |
| `build_exe.py` | Windows build |
| `build_exe_mac.py` | Mac build |

---

## 📖 Documentation

- **Deployment Guide:** `DEPLOYMENT.md`
- **Cloud Setup:** `STREAMLIT_CLOUD_GUIDE.md`
- **Checklist:** `PREPARATION_CHECKLIST.md`
- **GitHub README:** `README_GITHUB.md`

---

## 🆘 Troubleshooting

**Port in use?** → Change port in `.streamlit/config.toml`

**Module error?** → `pip install -r requirements.txt`

**Database error?** → Delete `attendance.db`, restart app

**Git issues?** → Check GitHub Desktop or `git status`

---

## 🔗 Useful Links

- Streamlit Cloud: https://share.streamlit.io
- GitHub: https://github.com
- Streamlit Docs: https://docs.streamlit.io

---

**Need help?** Read the detailed guides! 📚
