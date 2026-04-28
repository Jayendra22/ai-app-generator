import json

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
