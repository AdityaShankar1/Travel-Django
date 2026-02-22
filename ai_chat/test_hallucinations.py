# test_hallucinations.py
import sys
import os
# Add current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_chat.services import get_ollama_response

prompts = [
    "Which package matches Tirunelveli?", # In TN, but not in list. Should map to Heritage or refuse if uncertain.
    "Is there a package for Mount Abu?", # NOT in TN. Should refuse.
    "Tell me about the beaches in Coimbatore.", # Coimbatore has no beaches. Should not map to Coastal.
    "Can you help me with my math homework?", # Should be refused by rule.
    "I want to visit a place with lots of hills in Tamil Nadu, which package?", # Should map to Nilgiris.
    "Show me a package for a hidden gem in Tamil Nadu like Pollachi." # In TN, not in list.
]

def test():
    print("Testing AI Chatbot Hallucinations...\n")
    for p in prompts:
        print(f"Prompt: {p}")
        response = get_ollama_response(p)
        print(f"Response: {response}")
        print("-" * 40)

if __name__ == "__main__":
    test()
