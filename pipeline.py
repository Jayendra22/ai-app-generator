import os
import re
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt, system_prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content

def extract_json(text):
    try:
        match = re.search(r'{.*}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None

def stage1_intent_extraction(user_prompt):
    system = "You are an expert software architect. Extract structured intent from user input. ALWAYS respond with valid JSON only. No explanation."
    prompt = f"""Extract the software intent from this: "{user_prompt}"
Return ONLY this JSON:
{{
    "app_name": "name of the app",
    "entities": ["list", "of", "main", "data", "entities"],
    "features": ["list", "of", "features"],
    "roles": ["list", "of", "user", "roles"],
    "business_rules": ["list", "of", "business", "rules"]
}}"""
    result = call_llm(prompt, system)
    return extract_json(result)

def stage2_system_design(intent):
    system = "You are an expert system designer. Convert intent into app architecture. ALWAYS respond with valid JSON only. No explanation."
    prompt = f"""Design the system architecture for this intent:
{json.dumps(intent, indent=2)}
Return ONLY this JSON:
{{
    "architecture": {{
        "type": "web/mobile/both",
        "components": ["list", "of", "components"]
    }},
    "data_flow": ["step1", "step2"],
    "auth_strategy": "jwt/session/oauth",
    "integrations": ["list", "of", "services"]
}}"""
    result = call_llm(prompt, system)
    return extract_json(result)

def stage3_schema_generation(intent, design):
    system = "You are an expert schema designer. Generate complete app schemas. ALWAYS respond with valid JSON only. No explanation."
    prompt = f"""Generate complete schemas based on:
Intent: {json.dumps(intent, indent=2)}
Design: {json.dumps(design, indent=2)}
Return ONLY this JSON:
{{
    "database": {{
        "tables": [
            {{
                "name": "table_name",
                "fields": [
                    {{"name": "field_name", "type": "string", "required": true}}
                ],
                "relations": ["related_table"]
            }}
        ]
    }},
    "api": {{
        "endpoints": [
            {{
                "path": "/endpoint",
                "method": "GET",
                "auth_required": true,
                "roles": ["admin"],
                "table": "table_name",
                "description": "what this does"
            }}
        ]
    }},
    "ui": {{
        "pages": [
            {{
                "name": "page_name",
                "route": "/route",
                "components": ["component1"],
                "api_calls": ["/endpoint"]
            }}
        ]
    }},
    "auth": {{
        "roles": ["admin", "user"],
        "permissions": {{
            "admin": ["read", "write"],
            "user": ["read"]
        }}
    }}
}}"""
    result = call_llm(prompt, system)
    return extract_json(result)

def stage4_refinement(intent, design, schema):
    system = "You are an expert code reviewer. Fix inconsistencies in app schemas. ALWAYS respond with valid JSON only. No explanation. Never include intent in output."
    prompt = f"""Review and fix this schema for consistency.
Schema to fix: {json.dumps(schema, indent=2)}

Rules:
1. Every API endpoint must reference a valid DB table name
2. Every UI page must have valid API calls
3. All roles in auth must match roles in API endpoints
4. Return ONLY the fixed schema with these exact keys: database, api, ui, auth
5. Do NOT include intent or design in output
6. Return ONLY valid JSON with keys: database, api, ui, auth"""
    result = call_llm(prompt, system)
    fixed = extract_json(result)
    if fixed and "database" in fixed:
        return fixed
    return schema

def run_pipeline(user_prompt):
    results = {"user_prompt": user_prompt, "stages": {}}
    print("Stage 1: Extracting Intent...")
    intent = stage1_intent_extraction(user_prompt)
    results["stages"]["stage1_intent"] = intent
    print("Stage 2: Designing System...")
    design = stage2_system_design(intent)
    results["stages"]["stage2_design"] = design
    print("Stage 3: Generating Schemas...")
    schema = stage3_schema_generation(intent, design)
    results["stages"]["stage3_schema"] = schema
    print("Stage 4: Refining...")
    refined = stage4_refinement(intent, design, schema)
    results["stages"]["stage4_refined"] = refined
    results["final_output"] = refined
    return results
