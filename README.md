# Heep App

A simple FastAPI-based application with SQLModel.

## Features
- FastAPI backend
- SQLModel database
- Models and database management
- Ready to deploy

## How to Run Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Project Structure:**
```
app/
├── database.py
├── models.py
├── main.py
requirements.txt
README.md
```

## Deployment
You can deploy this app to platforms like:
- **Railway** (easy and free to start)
- **Render**
- **Vercel** (via serverless functions)

**Deployment Steps:**
1. Push your code to GitHub.
2. Connect your GitHub repository to the chosen platform.
3. Set the **start command** as:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
4. Ensure `requirements.txt` is in the root folder.
5. Deploy and access your app via the provided URL.
