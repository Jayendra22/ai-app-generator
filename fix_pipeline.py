content = open("pipeline.py", "r").read()

old_stage4 = '''def stage4_refinement(intent, design, schema):
    system = "You are an expert code reviewer. Fix inconsistencies in app schemas. ALWAYS respond with valid JSON only. No explanation."
    prompt = f"""Review and fix this schema for consistency:
Intent: {json.dumps(intent, indent=2)}
Schema: {json.dumps(schema, indent=2)}
Return the FIXED schema in exact same JSON structure."""
    result = call_llm(prompt, system)
    return extract_json(result)'''

new_stage4 = '''def stage4_refinement(intent, design, schema):
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
    return schema'''

content = content.replace(old_stage4, new_stage4)
open("pipeline.py", "w").write(content)
print("Stage 4 fixed!")
