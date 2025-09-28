"""
Vercel serverless function entry point.
This file is required for Vercel deployment.
"""

from main import app

# Export the FastAPI app for Vercel
handler = app
