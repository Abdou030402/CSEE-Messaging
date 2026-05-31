#!/usr/bin/env python3
"""
CSEE Messaging — minimal prototype frontend.

A tiny local web UI: type a plain-English request, and Claude (headless) runs the
exact same workflow as in the terminal — picks the right phase skill, drafts via
the csee-messaging MCP server, and (optionally) sends email / Slack — then the
page shows the result.

Run:  python app.py     then open  http://localhost:5000
"""

import os
import subprocess
from flask import Flask, request, jsonify, render_template_string

from draft_message import _find_claude

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CSEE Messaging</title>
  <style>
    :root { --bg:#0f1221; --card:#1a1f36; --accent:#5b8cff; --ok:#36c98e; --txt:#e8ecf6; --muted:#9aa3c0; }
    * { box-sizing: border-box; }
    body { margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
           background: var(--bg); color: var(--txt); min-height:100vh; display:flex;
           align-items:center; justify-content:center; padding:24px; }
    .card { background: var(--card); width:100%; max-width:720px; border-radius:16px;
            padding:28px 28px 24px; box-shadow:0 12px 40px rgba(0,0,0,.45); }
    h1 { margin:0 0 4px; font-size:22px; }
    .sub { color: var(--muted); margin:0 0 20px; font-size:14px; }
    textarea { width:100%; min-height:120px; resize:vertical; border-radius:10px;
               border:1px solid #2b3358; background:#0e1226;
               color:var(--txt); padding:14px; font-size:15px; line-height:1.5; }
    textarea:focus { outline:none; border-color: var(--accent); }
    .row { display:flex; align-items:center; justify-content:space-between; margin-top:14px; gap:12px; }
    label.toggle { display:flex; align-items:center; gap:8px; color:var(--muted); font-size:14px; cursor:pointer; }
    button { background: var(--accent); color:white; border:none; padding:12px 22px;
             border-radius:10px; font-size:15px; font-weight:600; cursor:pointer; }
    button:disabled { opacity:.5; cursor:not-allowed; }
    .out { margin-top:20px; background:#0e1226; border:1px solid #2b3358; border-radius:10px;
           padding:16px; white-space:pre-wrap; font-size:14px; line-height:1.55; min-height:40px;
           color:var(--txt); display:none; }
    .out.show { display:block; }
    .badge { display:inline-block; font-weight:700; margin-bottom:10px; }
    .badge.ok { color: var(--ok); }
    .badge.err { color:#ff6b6b; }
    .examples { margin-top:16px; font-size:13px; color:var(--muted); }
    .examples code { background:#0e1226; padding:2px 6px; border-radius:6px; cursor:pointer; }
    .spinner { width:16px; height:16px; border:2px solid #ffffff55; border-top-color:#fff;
               border-radius:50%; display:inline-block; vertical-align:-3px; margin-right:8px;
               animation:spin .8s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div class="card">
    <h1>CSEE Messaging</h1>
    <p class="sub">Describe the message in plain English. Claude picks the right course phase, drafts it, and sends it.</p>

    <textarea id="prompt" placeholder="e.g. send the acceptance email for JST WS 2025/26, confirm by Oct 5th 23:59, drop by Oct 13th 23:59"></textarea>

    <div class="row">
      <label class="toggle"><input type="checkbox" id="send"> Actually send it (otherwise draft only)</label>
      <button id="go" onclick="run()">Run</button>
    </div>

    <div class="examples">
      Try:
      <code onclick="fill(this)">send the acceptance email for JST WS 2025/26, confirm by Oct 5th 23:59, drop by Oct 13th 23:59</code>
    </div>

    <div id="out" class="out"></div>
  </div>

<script>
function fill(el){ document.getElementById('prompt').value = el.textContent; }
async function run(){
  const prompt = document.getElementById('prompt').value.trim();
  const send = document.getElementById('send').checked;
  const out = document.getElementById('out');
  const btn = document.getElementById('go');
  if(!prompt){ out.className='out show'; out.innerHTML='<span class="badge err">Enter a request first.</span>'; return; }
  btn.disabled = true;
  out.className='out show';
  out.innerHTML = '<span class="spinner"></span>' + (send ? 'Drafting and sending…' : 'Drafting…') + ' (this can take ~30–60s)';
  try {
    const r = await fetch('/run', {method:'POST', headers:{'Content-Type':'application/json'},
                                   body: JSON.stringify({prompt, send})});
    const data = await r.json();
    const badge = data.ok ? '<span class="badge ok">✅ Done</span>' : '<span class="badge err">⚠️ Error</span>';
    out.innerHTML = badge + '\\n\\n' + (data.output || '(no output)');
  } catch(e){
    out.innerHTML = '<span class="badge err">⚠️ Request failed</span>\\n\\n' + e;
  } finally {
    btn.disabled = false;
  }
}
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json(force=True) or {}
    prompt = (data.get("prompt") or "").strip()
    do_send = bool(data.get("send"))
    if not prompt:
        return jsonify({"ok": False, "output": "Please enter a request."})

    # This is a one-shot, non-conversational UI, so tell Claude not to ask
    # clarifying questions — draft with whatever was provided and omit the rest.
    no_questions = ("Do NOT ask me any clarifying questions — use only the details I "
                    "provided and naturally omit anything missing (never use placeholders).")
    instruction = (
        f"\n\n{no_questions} Now actually SEND this message directly without asking for "
        "confirmation, then reply with a one-line confirmation of what was sent and to whom."
        if do_send else
        f"\n\n{no_questions} Draft it and show me the full draft. Do NOT send anything."
    )

    args = [_find_claude(), "-p", prompt + instruction, "--dangerously-skip-permissions"]
    try:
        res = subprocess.run(args, cwd=PROJECT_DIR, capture_output=True,
                             text=True, encoding="utf-8", timeout=300)
        out = (res.stdout or "").strip() or (res.stderr or "").strip()
        return jsonify({"ok": res.returncode == 0, "output": out or "(no output)"})
    except subprocess.TimeoutExpired:
        return jsonify({"ok": False, "output": "Timed out after 5 minutes."})
    except Exception as e:
        return jsonify({"ok": False, "output": f"Error: {e}"})


if __name__ == "__main__":
    print("CSEE Messaging frontend → http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
