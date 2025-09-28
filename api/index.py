"""
Vercel serverless function entry point.
This file is required for Vercel deployment.
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Export the FastAPI app for Vercel
handler = app
