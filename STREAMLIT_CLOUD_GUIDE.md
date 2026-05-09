# 🚀 Streamlit Cloud Deployment - Quick Guide

## Step-by-Step Instructions

### Step 1: Prepare Your GitHub Repository

#### Option A: Using the Setup Script (Easiest)
```bash
# Double-click this file in Windows Explorer
setup_git.bat
```

#### Option B: Manual Setup
```bash
# Navigate to project folder
cd C:\Users\Benson\PycharmProjects\WorkAttendanceApp

# Initialize Git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Work Attendance Management System"
```

---

### Step 2: Create GitHub Repository

1. **Go to:** https://github.com/new

2. **Fill in details:**
   - Repository name: `work-attendance-app` (or your preferred name)
   - Description: "Work Attendance Management System"
   - Choose: **Public** or **Private** (your choice)
   - **DO NOT** initialize with README, .gitignore, or license

3. **Click:** "Create repository"

4. **Copy the repository URL** (looks like):
   ```
   https://github.com/YOUR_USERNAME/work-attendance-app.git
   ```

---

### Step 3: Push Code to GitHub

```bash
# Replace YOUR_USERNAME and YOUR_REPO with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

**Note:** You may need to enter your GitHub username and password/token.

---

### Step 4: Deploy to Streamlit Cloud

1. **Visit:** https://share.streamlit.io

2. **Sign up/in** using your GitHub account

3. **Click:** "New app" button

4. **Fill in deployment form:**

   ```
   Repository: YOUR_USERNAME/work-attendance-app
   Branch: main
   Main file path: main.py
   App URL: work-attendance-app (or custom name)
   ```

5. **Click:** "Deploy!" button

6. **Wait 2-3 minutes** for deployment to complete

---

### Step 5: Access Your Live App

Your app will be available at:
```
https://work-attendance-app.streamlit.app
```

Share this URL with anyone - they can access it from any device!

---

## ⚙️ Post-Deployment Configuration

### Database Initialization

After first deployment, you need to create initial data:

1. **Access your live app**
2. **Add companies** via the Companies page
3. **Add workers** via the Workers page
4. **Add sites** via the Sites page
5. **Add absent reasons** via the Absent Reasons page

Or use Excel import feature to bulk upload data.

---

## 🔄 Updating Your App

Whenever you make changes:

```bash
# Make your code changes
# Then:

git add .
git commit -m "Description of your changes"
git push

# Streamlit Cloud auto-deploys within 1-2 minutes!
```

---

## 📊 Database Considerations

### Free Tier Limitations

✅ **What persists:**
- Database data between sessions
- Uploaded files (temporary)

❌ **What resets:**
- Database when you redeploy
- Temporary files after 24 hours

### For Production Use

Consider these options:

1. **Streamlit Cloud Pro** ($0-99/month)
   - Persistent storage
   - More resources

2. **External Database**
   - PostgreSQL/MySQL on cloud
   - Modify `database.py` to connect remotely

3. **Self-hosted**
   - Docker container
   - Cloud server (AWS, Azure, GCP)

---

## 🐛 Troubleshooting

### Deployment Fails

**Check:**
1. All dependencies in `requirements.txt`
2. No syntax errors in Python files
3. Review build logs in Streamlit Cloud dashboard

**Common errors:**
```
ModuleNotFoundError → Add missing package to requirements.txt
ImportError → Check import statements
FileNotFoundError → Use relative paths
```

### App Runs But Shows Errors

**Check browser console:**
- Press F12 → Console tab
- Look for error messages

**Check Streamlit logs:**
- Go to Streamlit Cloud dashboard
- Click your app → Logs

### Database Not Saving Data

This is normal on free tier between deployments. For persistent data:
- Upgrade to Pro plan
- Or use external database

---

## 💡 Tips & Best Practices

### 1. Keep Requirements Clean
Only include necessary packages in `requirements.txt`:
```txt
streamlit==1.31.0
pandas==2.2.0
openpyxl==3.1.2
```

### 2. Use Environment Variables
For sensitive data (API keys, etc.):
```python
import os
api_key = os.environ.get('API_KEY')
```

Set in Streamlit Cloud: Settings → Secrets

### 3. Optimize Performance
- Cache expensive computations: `@st.cache_data`
- Limit data loading
- Use pagination for large datasets

### 4. Monitor Usage
- Check Streamlit Cloud dashboard
- Watch memory usage
- Monitor active users

---

## 🎓 Next Steps

After successful deployment:

1. **Test thoroughly** - Try all features
2. **Share with team** - Get feedback
3. **Monitor performance** - Check logs regularly
4. **Plan upgrades** - Consider Pro plan if needed
5. **Backup data** - Export important data regularly

---

## 📞 Need Help?

- **Streamlit Docs:** https://docs.streamlit.io
- **Community Forum:** https://discuss.streamlit.io
- **GitHub Issues:** Report bugs in your repo

---

**Happy Deploying! 🎉**
