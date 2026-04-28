import os
from fastapi import FastAPI
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
    html_path = os.path.join(os.getcwd(), "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/generate")
def generate(request: PromptRequest):
    results = run_pipeline(request.prompt)
    final_schema = results.get("final_output", {})
    errors, warnings = validate_schema(final_schema)
    validation = repair_report(errors, warnings)
    results["validation"] = validation
    return results
