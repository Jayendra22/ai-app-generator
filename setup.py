import os

pipeline_code = '''import os
import re
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt, system_prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content

def extract_json(text):
    try:
        match = re.search(r\'{.*}\', text, re.DOTALL)
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
    system = "You are an expert code reviewer. Fix inconsistencies in app schemas. ALWAYS respond with valid JSON only. No explanation."
    prompt = f"""Review and fix this schema for consistency:
Intent: {json.dumps(intent, indent=2)}
Schema: {json.dumps(schema, indent=2)}
Return the FIXED schema in exact same JSON structure."""
    result = call_llm(prompt, system)
    return extract_json(result)

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
'''

validator_code = '''import json

def validate_schema(schema):
    errors = []
    warnings = []
    if not schema:
        errors.append("Schema is empty or None")
        return errors, warnings
    if "database" not in schema:
        errors.append("Missing: database section")
    else:
        tables = schema["database"].get("tables", [])
        if not tables:
            errors.append("Missing: no tables in database")
        for table in tables:
            if "name" not in table:
                errors.append("Missing: table has no name")
            if "fields" not in table or not table["fields"]:
                errors.append(f"Missing: table '{table.get('name', 'unknown')}' has no fields")
    if "api" not in schema:
        errors.append("Missing: api section")
    else:
        endpoints = schema["api"].get("endpoints", [])
        if not endpoints:
            errors.append("Missing: no endpoints in api")
        db_tables = []
        if "database" in schema:
            db_tables = [t["name"] for t in schema["database"].get("tables", [])]
        for endpoint in endpoints:
            if "path" not in endpoint:
                errors.append("Missing: endpoint has no path")
            if "method" not in endpoint:
                errors.append(f"Missing: endpoint has no method")
            if "table" in endpoint:
                if endpoint["table"] not in db_tables:
                    errors.append(f"Mismatch: API '{endpoint.get('path')}' references unknown table '{endpoint['table']}'")
    if "ui" not in schema:
        errors.append("Missing: ui section")
    else:
        pages = schema["ui"].get("pages", [])
        if not pages:
            warnings.append("Warning: no pages in ui")
        api_paths = []
        if "api" in schema:
            api_paths = [e["path"] for e in schema["api"].get("endpoints", [])]
        for page in pages:
            if "name" not in page:
                errors.append("Missing: page has no name")
            if "route" not in page:
                errors.append(f"Missing: page has no route")
            for api_call in page.get("api_calls", []):
                if api_call not in api_paths:
                    warnings.append(f"Warning: page '{page.get('name')}' calls unknown API '{api_call}'")
    if "auth" not in schema:
        errors.append("Missing: auth section")
    else:
        if "roles" not in schema["auth"]:
            errors.append("Missing: no roles in auth")
        if "permissions" not in schema["auth"]:
            errors.append("Missing: no permissions in auth")
        auth_roles = schema["auth"].get("roles", [])
        for endpoint in schema.get("api", {}).get("endpoints", []):
            for role in endpoint.get("roles", []):
                if role not in auth_roles:
                    errors.append(f"Mismatch: role '{role}' in API not defined in auth")
    return errors, warnings

def repair_report(errors, warnings):
    return {
        "is_valid": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "status": "Valid" if len(errors) == 0 else "Has Errors"
    }
'''

main_code = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pipeline import run_pipeline
from validator import validate_schema, repair_report

app = FastAPI(title="AI App Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r") as f:
        return f.read()

@app.post("/generate")
def generate(request: PromptRequest):
    results = run_pipeline(request.prompt)
    final_schema = results.get("final_output", {})
    errors, warnings = validate_schema(final_schema)
    validation = repair_report(errors, warnings)
    results["validation"] = validation
    return results
'''

with open("pipeline.py", "w") as f:
    f.write(pipeline_code)
print("pipeline.py created!")

with open("validator.py", "w") as f:
    f.write(validator_code)
print("validator.py created!")

with open("main.py", "w") as f:
    f.write(main_code)
print("main.py created!")

print("All files created successfully!")