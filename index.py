#!/usr/bin/env python3
"""
Vercel Entry Point
==================

Simple entry point for Vercel deployment.
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.web.web_interface import app

# Vercel expects the app to be available at module level
app = app