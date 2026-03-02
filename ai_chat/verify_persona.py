import sys
import os

# Set PYTHONPATH to the project root
sys.path.append(os.getcwd())

from ai_chat.services import get_rule_based_response, get_ollama_response
import requests

def test_softened_fallbacks():
    print("Testing Softened Rule-Based Fallbacks:")
    cases = [
        ("Suggest some places to see in Tamil Nadu if I like hill stations", "Nilgiris Nature Retreat Package"),
        ("I'm interested in temples and history", "Tamil Nadu Heritage Package"),
        ("I love the beach", "Coastal Tamil Nadu package"),
        ("What's interesting about Salem?", "Tamil Nadu Heritage Package"),
        ("How's the weather?", "/weather/alerts/"),
        ("Tell me about something else", "specialized in travel across Tamil Nadu")
    ]
    
    for prompt, expected_fragment in cases:
        response = get_rule_based_response(prompt)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        if expected_fragment in response:
            print(f"✅ Correctly matched {expected_fragment}")
        else:
            print(f"❌ Failed to match {expected_fragment}")
        print("-" * 20)

def test_phi3_tone():
    print("\nTesting Phi3 Persona (via get_ollama_response):")
    # This will hit the actual local Phi3 if it's running
    prompt = "Hi, I'm looking for a nice trip in TN"
    try:
        response = get_ollama_response(prompt)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print("✅ Received response from Phi3.")
    except Exception as e:
        print(f"❌ Phi3 connection error: {e}")

if __name__ == "__main__":
    test_softened_fallbacks()
    test_phi3_tone()
