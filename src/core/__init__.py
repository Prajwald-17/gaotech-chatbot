"""
Core Chatbot Functionality
==========================

This module contains the core components of the chatbot system:
- ChatbotEngine: Main chatbot logic and response generation
- SimpleVectorStore: Lightweight vector search without ML dependencies
"""

from .chatbot_engine import ChatbotEngine
from .simple_vector_store import SimpleVectorStore

__all__ = ['ChatbotEngine', 'SimpleVectorStore']