# 🤖 AI App Generator

A multi-stage AI pipeline that converts natural language descriptions into complete, validated, executable app schemas — like a compiler for software generation.

## 🌐 Live Demo
[https://ai-app-generator-bchg.onrender.com/](https://ai-app-generator-bchg.onrender.com/)

## 🎯 What It Does
Type a natural language description like:
> "Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments"

And get a complete structured JSON output including:
- ✅ Database schema (tables, fields, relations)
- ✅ API schema (endpoints, methods, auth rules)
- ✅ UI schema (pages, components, routes)
- ✅ Auth system (roles, permissions)

---

## 🏗️ Architecture — 4 Stage Pipeline
User Prompt
↓
Stage 1: Intent Extraction
↓
Stage 2: System Design
↓
Stage 3: Schema Generation
↓
Stage 4: Refinement + Validation
↓
Final JSON Output

### Stage 1 — Intent Extraction
Parses user input into structured intermediate form:
- Entities
- Features
- Roles
- Business Rules

### Stage 2 — System Design
Converts intent into app architecture:
- Architecture type
- Components needed
- Auth strategy
- Third party integrations

### Stage 3 — Schema Generation
Generates complete schemas:
- Database tables and fields
- API endpoints with auth rules
- UI pages with routes
- Auth roles and permissions

### Stage 4 — Refinement
Resolves inconsistencies across all layers:
- API endpoints match DB tables
- UI pages reference valid APIs
- Roles are consistent everywhere

---

## 🛡️ Validation + Repair Engine

After pipeline runs, a separate validator checks:

| Check | Description |
|-------|-------------|
| DB Validation | Tables exist with proper fields |
| API-DB Consistency | Every endpoint references valid table |
| UI-API Consistency | Every page calls valid endpoint |
| Auth Consistency | All roles defined and consistent |

Repair strategy is intelligent — fixes only broken parts, not full retry.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python FastAPI |
| LLM | Groq (Llama 3.3 70B) |
| Validation | Custom Python engine |
| Frontend | HTML + CSS + JavaScript |
| Deployment | Render |

---

## 📦 Installation

### 1. Clone the repo:
```bash
git clone https://github.com/Jayendra22/ai-app-generator.git
cd ai-app-generator
```

### 2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Add your API key:
Create `.env` file:
GROQ_API_KEY=your_groq_api_key_here

### 5. Run the server:
```bash
uvicorn main:app --reload
```

### 6. Open browser:
http://127.0.0.1:8000

---

## 📁 Project Structure
ai-app-generator/
│
├── main.py          # FastAPI server + routes
├── pipeline.py      # 4-stage LLM pipeline
├── validator.py     # Validation + repair engine
├── requirements.txt # Dependencies
├── Procfile         # Deployment config
├── runtime.txt      # Python version
└── templates/
└── index.html   # Frontend UI

---

## 🧪 Example Output

Input:
Build a CRM with login, contacts, dashboard and role-based access

Output:
```json
{
  "database": {
    "tables": [
      {
        "name": "users",
        "fields": [
          {"name": "id", "type": "integer", "required": true},
          {"name": "email", "type": "string", "required": true},
          {"name": "role", "type": "string", "required": true}
        ]
      }
    ]
  },
  "api": {
    "endpoints": [
      {
        "path": "/users",
        "method": "GET",
        "auth_required": true,
        "roles": ["admin"],
        "table": "users"
      }
    ]
  },
  "ui": {
    "pages": [
      {
        "name": "Dashboard",
        "route": "/dashboard",
        "components": ["StatsCard", "Chart"],
        "api_calls": ["/users"]
      }
    ]
  },
  "auth": {
    "roles": ["admin", "user"],
    "permissions": {
      "admin": ["read", "write", "delete"],
      "user": ["read"]
    }
  }
}
```

---

## ⚖️ Tradeoffs

| Factor | Decision | Reason |
|--------|----------|--------|
| Cost vs Quality | Groq free tier | Zero cost with good quality |
| Latency vs Reliability | 4 stage pipeline | More reliable output |
| Repair Strategy | Fix specific parts | Saves cost vs full retry |
| Temperature | 0.3 | Balances creativity + consistency |

---

## 👨‍💻 Built By
JAY — Built for Base44 AI Platform Engineer Internship Task
