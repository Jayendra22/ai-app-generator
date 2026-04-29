new_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI App Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #0f0f1a; color: #ffffff; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #6366f1, #8b5cf6); padding: 30px; text-align: center; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header p { opacity: 0.8; font-size: 1.1rem; }
        .container { max-width: 1000px; margin: 40px auto; padding: 0 20px; }
        .input-section { background: #1a1a2e; border-radius: 16px; padding: 30px; margin-bottom: 30px; border: 1px solid #2d2d44; }
        textarea { width: 100%; height: 120px; background: #0f0f1a; border: 1px solid #3d3d5c; border-radius: 10px; color: white; padding: 15px; font-size: 1rem; resize: vertical; margin-bottom: 15px; }
        textarea:focus { outline: none; border-color: #6366f1; }
        button { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; border: none; padding: 14px 40px; border-radius: 10px; font-size: 1rem; cursor: pointer; width: 100%; font-weight: bold; }
        button:hover { opacity: 0.9; }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        .stages { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 30px; }
        .stage-card { background: #1a1a2e; border-radius: 12px; padding: 20px; border: 1px solid #2d2d44; }
        .stage-card h3 { color: #8b5cf6; margin-bottom: 10px; font-size: 0.9rem; text-transform: uppercase; }
        .stage-card pre { font-size: 0.75rem; overflow-x: auto; color: #a0a0c0; white-space: pre-wrap; max-height: 200px; overflow-y: auto; }
        .validation-box { background: #1a1a2e; border-radius: 12px; padding: 20px; margin-bottom: 30px; border: 1px solid #2d2d44; }
        .valid { border-color: #22c55e; }
        .invalid { border-color: #ef4444; }
        .status-badge { display: inline-block; padding: 6px 16px; border-radius: 20px; font-weight: bold; margin-bottom: 15px; }
        .status-valid { background: #14532d; color: #22c55e; }
        .status-invalid { background: #450a0a; color: #ef4444; }
        .error-item { color: #ef4444; margin: 5px 0; font-size: 0.9rem; }
        .warning-item { color: #f59e0b; margin: 5px 0; font-size: 0.9rem; }
        .final-output { background: #1a1a2e; border-radius: 12px; padding: 20px; border: 1px solid #6366f1; margin-bottom: 30px; }
        .final-output h2 { color: #6366f1; margin-bottom: 15px; }
        .final-output pre { font-size: 0.8rem; overflow-x: auto; color: #a0a0c0; white-space: pre-wrap; max-height: 400px; overflow-y: auto; }
        .loading { text-align: center; padding: 30px; color: #8b5cf6; font-size: 1.1rem; }
        .spinner { border: 3px solid #2d2d44; border-top: 3px solid #8b5cf6; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .pipeline-steps { display: flex; justify-content: space-between; margin-bottom: 30px; gap: 10px; }
        .step { flex: 1; text-align: center; padding: 12px; background: #1a1a2e; border-radius: 10px; border: 1px solid #2d2d44; font-size: 0.8rem; color: #6b6b8a; }
        .step.active { border-color: #8b5cf6; color: #8b5cf6; background: #1e1b4b; }
        .step.done { border-color: #22c55e; color: #22c55e; background: #052e16; }
        .example-chip { display: inline-block; background: #2d2d44; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; margin: 4px; cursor: pointer; color: #a0a0c0; }
        .example-chip:hover { background: #6366f1; color: white; }
        .exec-banner { border-radius: 12px; padding: 20px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; }
        .exec-ready { background: #052e16; border: 1px solid #22c55e; }
        .exec-not-ready { background: #450a0a; border: 1px solid #ef4444; }
        .download-btn { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; width: auto; }
        .assumption-box { background: #1a1a2e; border: 1px solid #f59e0b; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI App Generator</h1>
        <p>Natural Language to Complete App Schema in 4 Stages</p>
    </div>
    <div class="container">
        <div class="input-section">
            <h2 style="margin-bottom:15px; color:#8b5cf6;">Describe Your App</h2>
            <div style="margin-bottom:15px;">
                <span style="font-size:0.85rem; color:#6b6b8a;">Try: </span>
                <span class="example-chip" onclick="setPrompt(this)">Build a CRM with login, contacts, dashboard and role-based access</span>
                <span class="example-chip" onclick="setPrompt(this)">Create an e-commerce store with products, cart and payments</span>
                <span class="example-chip" onclick="setPrompt(this)">Make a project management tool with teams and tasks</span>
            </div>
            <textarea id="promptInput" placeholder="Describe your app here..."></textarea>
            <button id="generateBtn" onclick="generate()">Generate App Schema</button>
        </div>
        <div class="pipeline-steps">
            <div class="step" id="step1">Stage 1 Intent</div>
            <div class="step" id="step2">Stage 2 Design</div>
            <div class="step" id="step3">Stage 3 Schema</div>
            <div class="step" id="step4">Stage 4 Refine</div>
        </div>
        <div id="output"></div>
    </div>
    <script>
        function setPrompt(el) {
            document.getElementById('promptInput').value = el.innerText;
        }

        function downloadJSON(data) {
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'app-schema.json';
            a.click();
            URL.revokeObjectURL(url);
        }

        async function generate() {
            const prompt = document.getElementById('promptInput').value.trim();
            if (!prompt) { alert('Please enter a prompt!'); return; }
            const btn = document.getElementById('generateBtn');
            btn.disabled = true;
            btn.innerText = 'Generating...';
            ['step1','step2','step3','step4'].forEach(s => {
                document.getElementById(s).className = 'step';
            });
            document.getElementById('output').innerHTML = '<div class="loading"><div class="spinner"></div><p>Running 4-stage pipeline...</p><p style="font-size:0.85rem;color:#6b6b8a;margin-top:8px;">This takes 20-30 seconds</p></div>';
            const steps = ['step1','step2','step3','step4'];
            let i = 0;
            const interval = setInterval(() => {
                if (i > 0) document.getElementById(steps[i-1]).className = 'step done';
                if (i < steps.length) document.getElementById(steps[i]).className = 'step active';
                i++;
                if (i > steps.length) clearInterval(interval);
            }, 6000);
            try {
                const res = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt })
                });
                const data = await res.json();
                clearInterval(interval);
                steps.forEach(s => document.getElementById(s).className = 'step done');
                displayResults(data);
            } catch(err) {
                document.getElementById('output').innerHTML = '<div style="color:#ef4444;padding:20px;background:#1a1a2e;border-radius:12px;">Error: ' + err.message + '</div>';
            }
            btn.disabled = false;
            btn.innerText = 'Generate App Schema';
        }

        function displayResults(data) {
            const stages = data.stages || {};
            const validation = data.validation || {};
            const final = data.final_output || {};

            const hasDB = final && final.database && final.database.tables && final.database.tables.length > 0;
            const hasAPI = final && final.api && final.api.endpoints && final.api.endpoints.length > 0;
            const hasUI = final && final.ui && final.ui.pages && final.ui.pages.length > 0;
            const hasAuth = final && final.auth && final.auth.roles && final.auth.roles.length > 0;
            const executionReady = hasDB && hasAPI && hasUI && hasAuth;
            const isValid = validation.is_valid;

            let html = '';

            html += '<div class="exec-banner ' + (executionReady ? 'exec-ready' : 'exec-not-ready') + '">';
            html += '<div>';
            html += '<h2 style="color:' + (executionReady ? '#22c55e' : '#ef4444') + ';margin-bottom:5px;">' + (executionReady ? 'Execution Ready' : 'Not Execution Ready') + '</h2>';
            html += '<p style="color:#6b6b8a;font-size:0.85rem;">DB: ' + (hasDB ? 'OK' : 'Missing') + ' | API: ' + (hasAPI ? 'OK' : 'Missing') + ' | UI: ' + (hasUI ? 'OK' : 'Missing') + ' | Auth: ' + (hasAuth ? 'OK' : 'Missing') + '</p>';
            html += '</div>';
            html += '<button class="download-btn" onclick=\'downloadJSON(' + JSON.stringify(final) + ')\'>Download JSON</button>';
            html += '</div>';

            const assumptions = (stages.stage1_intent && stages.stage1_intent.assumptions) ? stages.stage1_intent.assumptions : [];
            if (assumptions.length > 0) {
                html += '<div class="assumption-box">';
                html += '<h3 style="color:#f59e0b;margin-bottom:10px;">Assumptions Made</h3>';
                assumptions.forEach(function(a) {
                    html += '<div style="color:#f59e0b;margin:5px 0;font-size:0.9rem;">- ' + a + '</div>';
                });
                html += '</div>';
            }

            html += '<div class="stages">';
            html += '<div class="stage-card"><h3>Stage 1 Intent Extraction</h3><pre>' + JSON.stringify(stages.stage1_intent, null, 2) + '</pre></div>';
            html += '<div class="stage-card"><h3>Stage 2 System Design</h3><pre>' + JSON.stringify(stages.stage2_design, null, 2) + '</pre></div>';
            html += '<div class="stage-card"><h3>Stage 3 Schema Generation</h3><pre>' + JSON.stringify(stages.stage3_schema, null, 2) + '</pre></div>';
            html += '<div class="stage-card"><h3>Stage 4 Refined Schema</h3><pre>' + JSON.stringify(stages.stage4_refined, null, 2) + '</pre></div>';
            html += '</div>';

            html += '<div class="validation-box ' + (isValid ? 'valid' : 'invalid') + '">';
            html += '<h2 style="margin-bottom:12px;">Validation Report</h2>';
            html += '<span class="status-badge ' + (isValid ? 'status-valid' : 'status-invalid') + '">' + validation.status + '</span>';
            html += '<p style="color:#6b6b8a;margin-bottom:10px;">Errors: ' + validation.error_count + ' | Warnings: ' + validation.warning_count + '</p>';
            (validation.errors||[]).forEach(function(e) { html += '<div class="error-item">Error: ' + e + '</div>'; });
            (validation.warnings||[]).forEach(function(w) { html += '<div class="warning-item">Warning: ' + w + '</div>'; });
            html += '</div>';

            html += '<div class="final-output">';
            html += '<h2>Final Output Schema</h2>';
            html += '<pre>' + JSON.stringify(final, null, 2) + '</pre>';
            html += '</div>';

            document.getElementById('output').innerHTML = html;
        }
    </script>
</body>
</html>"""

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(new_html)
print("HTML upgraded successfully!")