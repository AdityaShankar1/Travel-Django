import random

def get_rule_based_response(prompt):
    """Provides a deterministic response based on rules if AI is unreachable."""
    text = prompt.lower()
    
    # 1. User asks anything irrelevant --> politely refuse
    # We define irrelevance as not containing mentions of Tamil Nadu, travel, packages, or specific cities.
    relevant_keywords = [
        "tamil nadu", "travel", "package", "trip", "holiday", "tour",
        "madurai", "trichy", "tanjore", "thanjavur", 
        "ooty", "nilgiris", "kodaikanal",
        "chennai", "kanchipuram", "rameshwaram", "rameswaram", "dhanushkodi"
    ]
    
    is_weather_query = any(kw in text for kw in ("weather", "rain", "temperature", "climate", "forecast"))
    is_relevant = any(kw in text for kw in relevant_keywords) or is_weather_query
    
    if not is_relevant:
        return "I am a travel assistant for Tamil Nadu. I can only help you with travel-related queries for this region. Please ask something about our packages or destinations in Tamil Nadu."

    # 2. User asks about weather --> tell them to check the Weather Alerts page 
    if is_weather_query:
        return "Please check our Weather Alerts page for the latest updates on weather conditions across Tamil Nadu: /weather/alerts/"

    # 3. User asks about specific regions
    heritage_cities = ["madurai", "trichy", "tanjore", "thanjavur"]
    nature_cities = ["ooty", "nilgiris", "kodaikanal"]
    coastal_cities = ["chennai", "kanchipuram", "rameshwaram", "rameswaram", "dhanushkodi"]
    
    packages = [
        "Tamil Nadu Heritage Package",
        "Nilgiris Nature Retreat Package",
        "Coastal Tamil Nadu package"
    ]

    if any(city in text for city in heritage_cities):
        return "Based on your interest in heritage sites, we suggest our 'Tamil Nadu Heritage Package'."
    
    if any(city in text for city in nature_cities):
        return "For a refreshing experience in the hills, we suggest our 'Nilgiris Nature Retreat Package'."
    
    if any(city in text for city in coastal_cities):
        return "If you love the sea and temples, we suggest our 'Coastal Tamil Nadu package'."

    # Any other place (assuming it's still TN relevant but not explicitly in our cities list)
    return f"Sorry that is not yet in our database, we'll make sure to add it soon. Until then we recommend you try some of our existing packages, such as the {random.choice(packages)}."


def get_ollama_response(prompt):
    """Encapsulates external API logic with a rule-based fallback."""
    try:
        # Rule-based filter: classify the user prompt and produce a
        # compact, factual summary for the LLM to repackage.
        text = prompt.lower()

        # Guardrail text used when calling the LLM to repackage filtered output.
        guardrail = (
            "You are a travel assistant for our website. Only provide travel-"
            "related information about locations inside the state of Tamil Nadu, India. "
            "If the user asks about a location outside Tamil Nadu, reply: 'Sorry, we don't "
            "have data for that location yet.'\n\n"
            "VALUATION RULES:\n"
            "1. Only use these exact package names: 'Coastal Tamil Nadu package', "
            "'Nilgiris Nature Retreat Package', 'Tamil Nadu Heritage Package'.\n"
            "2. If you are unsure if a location matches a package, or if it is not a major "
            "tourist spot in Tamil Nadu, reply: 'Sorry, we don't have specific data for "
            "that location in our current packages.'\n"
            "3. If coastal/sea/beach/bay in Tamil Nadu -> 'Coastal Tamil Nadu package'.\n"
            "4. If hill/mountain/ghat in Tamil Nadu -> 'Nilgiris Nature Retreat Package'.\n"
            "5. If a known heritage city (like Madurai, Tanjore) -> 'Tamil Nadu Heritage Package'.\n"
            "6. DO NOT invent justifications. Respond in one short sentence: "
            "'<Package name> — <short reason>'.\n"
            "7. If asked for homework or academic cheating, politely refuse."
        )

        # 1) Refuse academic cheating/homework requests outright.
        if any(k in text for k in ("homework", "exam", "cheat", "cheating", "assignment")):
            return (
                "Sorry, I can't help with homework solutions or exam answers. "
                "I can explain concepts or provide study guidance instead."
            )

        # Basic token sets for mapping
        tn_cities = {
            'madurai': ('Tamil Nadu Heritage Package', 'Madurai circuit'),
            'ooty': ('Nilgiris Nature Retreat Package', 'Ooty circuit'),
            'kodaikanal': ('Nilgiris Nature Retreat Package', 'Ooty circuit'),
            'chennai': ('Coastal Tamil Nadu package', 'Chennai circuit'),
            'rameshwaram': ('Coastal Tamil Nadu package', 'Rameshwaram circuit'),
            'rameswaram': ('Coastal Tamil Nadu package', 'Rameshwaram circuit'),
            'salem': ('Tamil Nadu Heritage Package', 'Salem circuit'),
            'thanjavur': ('Tamil Nadu Heritage Package', 'Heritage circuit'),
            'tanjore': ('Tamil Nadu Heritage Package', 'Heritage circuit'),
            'coimbatore': ('Tamil Nadu Heritage Package', 'Business/Heritage circuit'),
            'trichy': ('Tamil Nadu Heritage Package', 'Heritage circuit'),
            'tiruchirappalli': ('Tamil Nadu Heritage Package', 'Heritage circuit'),
        }

        non_tn_tokens = {"mysore", "bengaluru", "bangalore", "kerala", "goa", "mumbai", "delhi", "kolkata", "hyderabad", "mount abu"}

        coastal_kw = ("coast", "coastal", "sea", "beach", "bay", "pondicherry", "mahabalipuram", "kanyakumari")
        hill_kw = ("hill", "hills", "mountain", "ghat", "nilgiri", "ooty", "kodaikanal", "yercaud", "valparai")
        # If the user mentions a clear non-TN place and not a TN city, refuse.
        if any(tok in text for tok in non_tn_tokens) and not any(tok in text for tok in tn_cities):
            return "Sorry, we don't have data for that location yet."

        # Only trigger deterministic package mapping for package-intent prompts
        package_intent_keywords = (
            'package', 'packages', 'which package', 'is there any package',
            'match', 'matches', 'suggest package', 'map to', 'nearest match',
            'which circuit', 'circuit', 'recommend package'
        )
        package_intent = any(kw in text for kw in package_intent_keywords)

        # 1. Deterministic City Mapping
        if package_intent:
            for city, (pkg, circuit) in tn_cities.items():
                if city in text:
                    summary = {
                        'package': pkg,
                        'circuit': circuit,
                        'reason': f"Matched city {city.title()} to {circuit}."
                    }
                    filtered = (
                        f"FILTERED_SUMMARY:\npackage: {summary['package']}\n"
                        f"circuit: {summary['circuit']}\nreason: {summary['reason']}\n"
                        "Instruction: Reformat the above into a single concise user-facing sentence."
                    )
                    lml_prompt = f"{guardrail}\n\n{filtered}\nUser original prompt:\n{prompt}"
                    response = requests.post(
                        'http://localhost:11434/api/generate',
                        json={'model': 'phi3', 'prompt': lml_prompt, 'stream': False},
                        timeout=5
                    )
                    raw_text = _extract_model_response(response)
                    return _sanitize_model_output(raw_text, summary=summary, is_package_intent=True) or f"{summary['package']} — {summary['reason']}"

            # 2. Heuristic Keyword Mapping (only for Tamil Nadu or implicit TN)
            if "tamil nadu" in text or "tn" in text:
                summary = None
                if any(k in text for k in coastal_kw) and not any(k in text for k in hill_kw):
                    summary = {
                        'package': 'Coastal Tamil Nadu package',
                        'circuit': 'Chennai/Rameshwaram circuits',
                        'reason': 'Detected coastal keywords in Tamil Nadu.'
                    }
                elif any(k in text for k in hill_kw):
                    summary = {
                        'package': 'Nilgiris Nature Retreat Package',
                        'circuit': 'Ooty circuit',
                        'reason': 'Detected hillstation keywords in Tamil Nadu.'
                    }
                
                if summary:
                    filtered = (
                        f"FILTERED_SUMMARY:\npackage: {summary['package']}\n"
                        f"circuit: {summary['circuit']}\nreason: {summary['reason']}\n"
                        "Instruction: Reformat the above into a single concise user-facing sentence."
                    )
                    lml_prompt = f"{guardrail}\n\n{filtered}\nUser original prompt:\n{prompt}"
                    response = requests.post(
                        'http://localhost:11434/api/generate',
                        json={'model': 'phi3', 'prompt': lml_prompt, 'stream': False},
                        timeout=5
                    )
                    raw_text = _extract_model_response(response)
                    return _sanitize_model_output(raw_text, summary=summary, is_package_intent=True) or f"{summary['package']} — {summary['reason']}"

        # 3. General Question Fallthrough (with strict guardrails)
        full_prompt = f"{guardrail}\n\nUser prompt:\n{prompt}"
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': 'phi3', 'prompt': full_prompt, 'stream': False},
            timeout=5
        )
        raw_text = _extract_model_response(response)
        return _sanitize_model_output(raw_text, is_package_intent=package_intent) or "Sorry, I couldn't find a matching package for your request."
    except Exception:
        # Fallback to rule-based response if Ollama is unreachable
        return get_rule_based_response(prompt)


def _extract_model_response(response):
    """Try several common response shapes from local model servers.

    Returns a string if found, otherwise None.
    """
    try:
        payload = response.json()
    except Exception:
        return None

    # Direct 'response' key
    if isinstance(payload, dict):
        if 'response' in payload and payload['response']:
            return payload['response']

        # Some servers return results list
        if 'results' in payload and isinstance(payload['results'], list) and payload['results']:
            first = payload['results'][0]
            # try common keys
            for key in ('response', 'text', 'content', 'output'):
                if key in first and first[key]:
                    return first[key]

        # Other nested formats
        for key in ('text', 'output', 'content'):
            if key in payload and payload[key]:
                return payload[key]

    # As a last resort, try to stringify any textual fields
    try:
        # join any strings in the payload values
        if isinstance(payload, dict):
            texts = [str(v) for v in payload.values() if isinstance(v, (str,))]
            if texts:
                return ' '.join(texts)
    except Exception:
        pass

    return None


def _sanitize_model_output(text, allowed_packages=None, summary=None, is_package_intent=False):
    """Sanitize model output to prevent invented package names.

    - If `is_package_intent` is True, ensure the output mentions one of
      the allowed package names (or the package in `summary`). If not,
      return a deterministic fallback sentence.
    - If `is_package_intent` is False and the output mentions 'package'
      but no allowed package names, replace that fragment with a safe
      notice listing available packages.
    """
    if text is None:
        return None

    if allowed_packages is None:
        allowed_packages = {
            'Coastal Tamil Nadu package',
            'Nilgiris Nature Retreat Package',
            'Tamil Nadu Heritage Package',
        }

    # Normalize for matching
    lowered = text.lower()
    allowed_lower = {p.lower() for p in allowed_packages}

    # If package-intent, require an allowed package name in the model output.
    if is_package_intent:
        # If summary provided, ensure its package is represented
        if summary and summary.get('package'):
            pkg_lower = summary['package'].lower()
            if pkg_lower in lowered:
                return text
            # If model didn't include the expected package, ignore model output
            return f"{summary['package']} — {summary['reason']}"

        # Fallback: check any allowed package present
        if any(pkg in lowered for pkg in allowed_lower):
            return text
        # No allowed package found: return None so caller can fallback
        return None

    # For generic prompts: if model mentions 'package' but not allowed names,
    # replace package mentions with a safe clause listing available packages.
    if 'package' in lowered and not any(pkg in lowered for pkg in allowed_lower):
        available = ', '.join(sorted(allowed_packages))
        # Simple replacement: warn user instead of showing invented names.
        return text + f"\n\nNote: Available packages are: {available}."

    return text
