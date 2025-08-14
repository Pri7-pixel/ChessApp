# 🚀 Deployment Guide

This guide will help you host your Chess Rating Calculator on GitHub and Streamlit Cloud.

## Option 1: Streamlit Cloud (Recommended)

### Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in to your account
2. **Click the "+" icon** in the top right corner and select "New repository"
3. **Name your repository** (e.g., `chess-rating-calculator`)
4. **Make it public** (required for free Streamlit Cloud)
5. **Don't initialize** with README, .gitignore, or license (we already have these)
6. **Click "Create repository"**

### Step 2: Upload Your Code

1. **Open your terminal/command prompt** in your project directory
2. **Initialize git repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Chess Rating Calculator"
   ```

3. **Add your GitHub repository as remote**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/chess-rating-calculator.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy on Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Select your repository**: `chess-rating-calculator`
5. **Set the main file path**: `chess_rating_calculator.py`
6. **Click "Deploy"**

Your app will be available at: `https://your-app-name.streamlit.app`

## Option 2: GitHub Pages (Static Version)

If you want to create a static version for GitHub Pages, you can create a simple HTML version of the app.

## Option 3: Heroku

### Step 1: Create Procfile
Create a file named `Procfile` (no extension):
```
web: streamlit run chess_rating_calculator.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 2: Create runtime.txt
Create a file named `runtime.txt`:
```
python-3.9.18
```

### Step 3: Deploy to Heroku
1. Install Heroku CLI
2. Run:
   ```bash
   heroku create your-app-name
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Option 4: Railway

1. **Go to [railway.app](https://railway.app)**
2. **Connect your GitHub account**
3. **Select your repository**
4. **Add environment variables** if needed
5. **Deploy**

## Important Notes

### Data Persistence
- **Streamlit Cloud**: Data is not persistent between sessions
- **Local deployment**: Data is saved in JSON files
- **For production**: Consider using a database (SQLite, PostgreSQL, etc.)

### Environment Variables
If you need to configure settings, you can add them in Streamlit Cloud:
- Go to your app settings
- Add environment variables as needed

### Custom Domain
- **Streamlit Cloud**: Not supported in free tier
- **Heroku**: Can add custom domain
- **Railway**: Can add custom domain

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are in `requirements.txt`
2. **Port issues**: The app should automatically handle port configuration
3. **Data not saving**: Cloud deployments don't persist data by default

### Performance Tips

1. **Optimize imports**: Only import what you need
2. **Use caching**: Add `@st.cache_data` to expensive operations
3. **Limit data size**: Don't load too much data at once

## Security Considerations

1. **Don't commit sensitive data**: Use environment variables
2. **Validate inputs**: Always validate user inputs
3. **Rate limiting**: Consider adding rate limiting for public apps

## Monitoring

- **Streamlit Cloud**: Built-in monitoring
- **Heroku**: Use Heroku logs
- **Railway**: Built-in monitoring

---

**Your app is now ready to be shared with the world! 🌍**
