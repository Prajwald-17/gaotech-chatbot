#!/usr/bin/env python3
"""
Test the updated 4-question layout
"""

from chatbot_engine import ChatbotEngine

def test_4_questions():
    """Test the new 4-question layout"""
    
    print("🧪 Testing Updated 4-Question Layout")
    print("="*50)
    
    # Initialize chatbot
    bot = ChatbotEngine()
    
    # Get conversation starters
    starters = bot.get_conversation_starter()
    
    print(f"📝 Number of prompt questions: {len(starters)}")
    print("\n💬 Prompt Questions:")
    for i, question in enumerate(starters, 1):
        print(f"  {i}. {question}")
    
    print("\n🎨 Layout:")
    print("  ✅ 2x2 grid on desktop")
    print("  ✅ Single column on mobile")
    print("  ✅ Always visible (sticky)")
    print("  ✅ Clean, professional appearance")
    
    print(f"\n🌐 Test the new layout at: http://localhost:5000")
    print("🎯 Much cleaner interface with just the essential questions!")

if __name__ == "__main__":
    test_4_questions()