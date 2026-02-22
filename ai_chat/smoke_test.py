# ai_chat/smoke_test.py
from ai_chat.services import get_ollama_response
import requests

captured = {}
class DummyResponse:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data


def fake_post(url, json=None, **kwargs):
    captured['url'] = url
    captured['json'] = json
    prompt = json.get('prompt','') if isinstance(json, dict) else ''
    # Basic guardrail checks
    if "Tamil Nadu" not in prompt:
        raise AssertionError("Guardrail missing 'Tamil Nadu'")
    if "homework" not in prompt and "academic cheating" not in prompt:
        raise AssertionError("Guardrail missing 'homework' refusal")
    # Ensure mapping instructions present
    if "Coastal Tamil Nadu package" not in prompt:
        raise AssertionError("Guardrail missing package mapping instructions")
    return DummyResponse({'response': 'SIMULATED_RESPONSE'})


# Patch requests.post
requests.post = fake_post


def run_cases():
    # 1) LLM path: no mapping tokens -> should call fake_post and return simulated response
    r1 = get_ollama_response("What's the square root of 4?")
    print('LLM path result:', r1)

    # 2) Mapping: Madurai (Tamil Nadu) with package-intent -> should map and then call LLM to reformat
    r2 = get_ollama_response("Is there any package that matches Madurai, Tamil Nadu?")
    print('Mapping Madurai (via LLM):', r2)

    # 3) Outside Tamil Nadu: Mysore -> missing data (direct refusal)
    r3 = get_ollama_response("I want to travel to Mysore")
    print('Non-TN place (refusal):', r3)

    # 4) Coastal mention with package intent -> Coastal package (should call LLM)
    r4 = get_ollama_response("Which package matches the beaches in Chennai, Tamil Nadu?")
    print('Coastal mapping (via LLM):', r4)

    # 5) Hill mention with package intent -> Nilgiris package (should call LLM)
    r5 = get_ollama_response("Is there a package for Ooty or Kodaikanal?")
    print('Hill mapping (via LLM):', r5)

    # 6) Generic prompt about places in Tamil Nadu -> should let LLM speak (LLM path)
    r6 = get_ollama_response("Places to see in Tamil Nadu?")
    print('Generic TN prompt (LLM):', r6)


if __name__ == '__main__':
    run_cases()
