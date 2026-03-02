import sys
import os

# Set PYTHONPATH to the project root
sys.path.append(os.getcwd())

from ai_chat.services import get_rule_based_response, get_ollama_response
import requests

def test_hill_station_fallback():
    print("Testing Rule-Based Fallback for Hill Stations:")
    prompt = "Suggest some places to see in Tamil Nadu if I like hill stations"
    response = get_rule_based_response(prompt)
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    
    expected = "For a refreshing experience in the hills, we suggest our 'Nilgiris Nature Retreat Package'."
    if response == expected:
        print("✅ Rule-based fallback for hill stations is WORKING.")
    else:
        print(f"❌ Rule-based fallback failed. Expected: {expected}")

def test_phi3_connection():
    print("\nTesting Phi3 Connection (via get_ollama_response):")
    prompt = "Hi"
    try:
        response = get_ollama_response(prompt)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        print("✅ Phi3 connection seems to be working (or correctly falling back without crashing).")
    except Exception as e:
        print(f"❌ Phi3 connection crashed: {e}")

if __name__ == "__main__":
    test_hill_station_fallback()
    test_phi3_connection()
