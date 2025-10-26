# Deploying Gir Cow Farm Management to GitHub + Streamlit Cloud

This guide walks you through deploying your Streamlit app to GitHub and hosting it on Streamlit Community Cloud (free).

---

## 📋 Prerequisites

- **GitHub account** (free at [github.com](https://github.com))
- **Git installed** on your local machine
- **Streamlit Community Cloud account** (free at [share.streamlit.io](https://share.streamlit.io))

---

## 🚀 Deployment Steps

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right, then **"New repository"**
3. Enter repository details:
   - **Repository name**: `gir-cow-farm-management` (or your preferred name)
   - **Description**: "Dairy farm management system for Gir cows"
   - **Visibility**: Choose **Public** or **Private**
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

GitHub will show you commands to push your code. **Keep this page open**.

---

### Step 2: Prepare Your Local Project

#### A. Create requirements.txt

Since this project uses Replit's package management, you need to create a `requirements.txt` file for Streamlit Cloud.

Create a file named `requirements.txt` in your project root with this content:

```txt
streamlit
pandas
plotly
psycopg2-binary
sqlalchemy
openpyxl
pillow
```

**Note**: The `packages.txt` file has already been created for PostgreSQL system dependencies.

#### B. Download Your Code from Replit

1. In Replit, click the **three dots menu** (⋮) in the Files panel
2. Select **"Download as zip"**
3. Extract the zip file to a folder on your computer
4. Open a terminal/command prompt in that folder

---

### Step 3: Initialize Git and Push to GitHub

Run these commands in your terminal (replace `YOUR-USERNAME` and `YOUR-REPO-NAME` with your actual GitHub username and repository name):

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - Gir Cow Farm Management System"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example**:
```bash
git remote add origin https://github.com/johnsmith/gir-cow-farm-management.git
```

---

### Step 4: Set Up PostgreSQL Database

Your app needs a PostgreSQL database. Here are your options:

#### Option 1: Neon (Recommended - Free & Easy)

1. Go to [neon.tech](https://neon.tech) and create a free account
2. Create a new project
3. Copy the **connection string** (looks like: `postgresql://user:pass@ep-xyz.us-east-2.aws.neon.tech/neondb`)
4. **Save this connection string** - you'll need it in Step 5

#### Option 2: Supabase (Also Free)

1. Go to [supabase.com](https://supabase.com) and create account
2. Create new project
3. Go to **Settings** → **Database**
4. Copy the **Connection string** (under "Connection pooling")
5. **Save this connection string**

#### Option 3: Other PostgreSQL Providers

Any PostgreSQL hosting service will work:
- ElephantSQL
- Railway
- Heroku Postgres
- AWS RDS
- Google Cloud SQL

---

### Step 5: Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with your GitHub account
   - Click "Continue with GitHub"
   - Authorize Streamlit to access your repositories

3. **Create new app**:
   - Click **"Create app"** or **"New app"**
   - When asked "Do you already have an app?", click **"Yup, I have an app"**

4. **Configure deployment**:
   - **Repository**: Select your `gir-cow-farm-management` repo
   - **Branch**: `main` (or `master`)
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain like `gir-farm-yourname`

5. **Configure Secrets** (Important!):
   - Before clicking "Deploy", click **"Advanced settings"**
   - In the **Secrets** section, paste your database configuration:

   ```toml
   [connections.postgresql]
   url = "postgresql://your-username:your-password@your-host:5432/your-database"
   ```

   Replace with your actual database connection string from Step 4.

   **Example with Neon**:
   ```toml
   [connections.postgresql]
   url = "postgresql://user:AbcXyz123@ep-cool-sun-12345678.us-east-2.aws.neon.tech/neondb?sslmode=require"
   ```

6. **Deploy**:
   - Click **"Deploy!"**
   - Wait 2-5 minutes for deployment
   - Your app will be live at: `https://your-app-name.streamlit.app`

---

### Step 6: Initialize Your Database

After deployment, you need to set up your database tables:

1. Your app includes `init_db.py` which creates all necessary tables
2. You have two options:

#### Option A: Run Initialization Script Manually

If your deployment doesn't automatically create tables:

1. In Streamlit Cloud, go to your app's **"Manage app"** menu
2. Click **"Reboot app"** after ensuring your database connection works
3. Or run the init script from your local machine:
   ```bash
   # Install dependencies locally
   pip install psycopg2-binary sqlalchemy
   
   # Run initialization (use your database URL)
   DATABASE_URL="your-connection-string" python init_db.py
   ```

#### Option B: Modify app.py to Auto-Initialize

Add this code at the top of your `app.py` (after imports):

```python
# Auto-initialize database on first run
if 'db_initialized' not in st.session_state:
    try:
        from init_db import init_database
        init_database()
        st.session_state.db_initialized = True
    except Exception as e:
        st.error(f"Database initialization error: {e}")
```

---

## 🔄 Updating Your Deployed App

After initial deployment, any changes you push to GitHub will **automatically update** your live app:

```bash
# Make changes to your code
# Then commit and push:

git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will detect the changes and redeploy automatically (usually takes 1-2 minutes).

---

## 🐛 Troubleshooting

### App Won't Start

**Check the logs**:
1. In Streamlit Cloud, click your app
2. Click the **"≡"** menu (hamburger) → **"Manage app"**
3. View the **logs** on the right side

**Common issues**:

- **Missing dependencies**: Ensure all packages are in `requirements.txt`
- **Database connection**: Verify your connection string in Secrets
- **Import errors**: Check that all your files are in the GitHub repo

### Database Connection Errors

1. Verify your database connection string in **Secrets**
2. Ensure the database allows external connections
3. Check if your database provider requires SSL (`?sslmode=require` at the end of the URL)
4. For Neon/Supabase, make sure the database hasn't been paused (free tier may pause after inactivity)

### "No module named..." Error

Add the missing package to `requirements.txt` and push to GitHub:

```bash
echo "package-name" >> requirements.txt
git add requirements.txt
git commit -m "Add missing package"
git push origin main
```

### App is Slow or Times Out

- **Database location**: Choose a database server close to your users
- **Optimize queries**: Add indexes to frequently queried columns
- **Use caching**: Streamlit's `@st.cache_data` decorator for heavy operations

---

## 📚 Additional Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/deploy/streamlit-community-cloud)
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [GitHub Docs](https://docs.github.com/)

---

## ✅ Verification Checklist

Before deployment, ensure:

- [ ] `requirements.txt` created with all dependencies
- [ ] `packages.txt` exists (for PostgreSQL)
- [ ] `.gitignore` prevents sensitive files from being committed
- [ ] Database is set up and accessible
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] Database connection string configured in Secrets
- [ ] App deployed successfully
- [ ] Database tables initialized
- [ ] App is accessible via the Streamlit Cloud URL

---

## 🎉 You're Done!

Your Gir Cow Farm Management System is now live and accessible from anywhere!

**Share your app**: `https://your-app-name.streamlit.app`

**Next steps**:
- Test all features with live database
- Add sample data for demonstration
- Share the URL with stakeholders
- Monitor app usage in Streamlit Cloud dashboard
