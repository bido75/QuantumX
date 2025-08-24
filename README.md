# QuantumX Backend (Deployable Version)

This version is pre-structured for deployment to [Render](https://render.com).

## 🚀 How to Deploy

1. Push these files to your GitHub repo
2. Go to Render > New Web Service
3. Select your repo, use defaults:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
4. Set your environment variable in Render:
   - `API_KEY=your_actual_api_key_here`

Done!

## ⚠️ Note
- This version places backend files in the root directory.
- Ideal for Render, Railway, and Replit deployment.
