html = open("templates/index.html", "r", encoding="utf-8").read()

# Add download button and execution ready indicator to displayResults function
old_js = '''function displayResults(data) {
            const stages = data.stages || {};
            const validation = data.validation || {};
            const final = data.final_output || {};
            const isValid = validation.is_valid;
            document.getElementById('output').innerHTML =
                '<div class="stages">' +
                '<div class="stage-card"><h3>Stage 1 Intent Extraction</h3><pre>' + JSON.stringify(stages.stage1_intent, null, 2) + '</pre></div>' +
                '<div class="stage-card"><h3>Stage 2 System Design</h3><pre>' + JSON.stringify(stages.stage2_design, null, 2) + '</pre></div>' +
                '<div class="stage-card"><h3>Stage 3 Schema Generation</h3><pre>' + JSON.stringify(stages.stage3_schema, null, 2) + '</pre></div>' +
                '<div class="stage-card"><h3>Stage 4 Refined Schema</h3><pre>' + JSON.stringify(stages.stage4_refined, null, 2) + '</pre></div>' +
                '</div>' +
                '<div class="validation-box ' + (isValid ? 'valid' : 'invalid') + '">' +
                '<h2 style="margin-bottom:12px;">Validation Report</h2>' +
                '<span class="status-badge ' + (isValid ? 'status-valid' : 'status-invalid') + '">' + validation.status + '</span>' +
                '<p style="color:#6b6b8a;margin-bottom:10px;">Errors: ' + validation.error_count + ' | Warnings: ' + validation.warning_count + '</p>' +
                (validation.errors||[]).map(e => '<div class="error-item">' + e + '</div>').join('') +
                (validation.warnings||[]).map(w => '<div class="warning-item">' + w + '</div>').join('') +
                '</div>' +
                '<div class="final-output"><h2>Final Output Schema</h2><pre>' + JSON.stringify(final, null, 2) + '</pre></div>';
        }'''

new_js = '''function downloadJSON(data) {
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'app-schema.json';
            a.click();
        }

        function displayResults(data) {
            const stages = data.stages || {};
            const validation = data.validation || {};
            const final = data.final_output || {};
            const isValid = validation.is_valid;
            const errorsFixed = validation.repairs || [];
            const assumptions = stages.stage1_intent?.assumptions || [];

            // Execution ready check
            const hasDB = final && final.database && final.database.tables && final.database.tables.length > 0;
            const hasAPI = final && final.api && final.api.endpoints && final.api.endpoints.length > 0;
            const hasUI = final && final.ui && final.ui.pages && final.ui.pages.length > 0;
            const hasAuth = final && final.auth && final.auth.roles && final.auth.roles.length > 0;
            const executionReady = hasDB && hasAPI && hasUI && hasAuth;

            document.getElementById('output').innerHTML =
                // Execution Ready Banner
                '<div style="background:' + (executionReady ? '#052e16' : '#450a0a') + ';border:1px solid ' + (executionReady ? '#22c55e' : '#ef4444') + ';border-radius:12px;padding:20px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;">' +
                '<div>' +
                '<h2 style="color:' + (executionReady ? '#22c55e' : '#ef4444') + ';margin-bottom:5px;">' + (executionReady ? '✅ Execution Ready' : '❌ Not Execution Ready') + '</h2>' +
                '<p style="color:#6b6b8a;font-size:0.85rem;">DB: ' + (hasDB ? '✅' : '❌') + ' | API: ' + (hasAPI ? '✅' : '❌') + ' | UI: ' + (hasUI ? '✅' : '❌') + ' | Auth: ' + (hasAuth ? '✅' : '❌') + '</p>' +
                '</div>' +
                '<button onclick="downloadJSON(' + JSON.stringify(final) + ')" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;font-weight:bold;">⬇️ Download JSON</button>' +
                '</div>' +

                // Assumptions box (if any)
                (assumptions.length > 0 ?
                '<div style="background:#1a1a2e;border:1px solid #f59e0b;border-radius:12px;padding:20px;margin-bottom:20px;">' +
                '<h3 style="color:#f59e0b;margin-bottom:10px;">💡 Assumptions Made</h3>' +
                assumptions.map(a => '<div style="color:#f59e0b;margin:5px 0;font-size:0.9rem;">• ' + a + '</div>').join('') +
                '</div>' : '') +

                // 4 Stage Cards
                '<div class="stages">' +
                '<div class="stage-card"><h3>Stage 1 Intent Extraction</h3><pre>' + JSON.stringify(stages.stage1_intent, null, 2) + '</pre></div>' +
                '<div class="stage-card"><h3>Stage 2 System Design</h3><pre>' + JSON.stringify(stages.stage2_design, null, 2) + '</pre></div>' +
                '<div class="stage-card"><h3>Stage 3 Schema Generation</h3><pre>' + JSON.stringify(stages.stage3_schema, null, 2) + '</pre></div>' +
                '<div class="stage-card"><h3>Stage 4 Refined Schema</h3><pre>' + JSON.stringify(stages.stage4_refined, null, 2) + '</pre></div>' +
                '</div>' +

                // Validation Report
                '<div class="validation-box ' + (isValid ? 'valid' : 'invalid') + '">' +
                '<h2 style="margin-bottom:12px;">🛡️ Validation Report</h2>' +
                '<span class="status-badge ' + (isValid ? 'status-valid' : 'status-invalid') + '">' + validation.status + '</span>' +
                '<p style="color:#6b6b8a;margin-bottom:10px;">Errors: ' + validation.error_count + ' | Warnings: ' + validation.warning_count + '</p>' +
                (validation.errors||[]).map(e => '<div class="error-item">❌ ' + e + '</div>').join('') +
                (validation.warnings||[]).map(w => '<div class="warning-item">⚠️ ' + w + '</div>').join('') +
                '</div>' +

                // Final Output
                '<div class="final-output">' +
                '<h2 style="margin-bottom:15px;">🚀 Final Output Schema</h2>' +
                '<pre>' + JSON.stringify(final, null, 2) + '</pre>' +
                '</div>';
        }'''

html = html.replace(old_js, new_js)
open("templates/index.html", "w", encoding="utf-8").write(html)
print("UI upgraded successfully!")