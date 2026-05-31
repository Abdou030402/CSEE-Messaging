#!/usr/bin/env python3
"""
AI-Powered Course Announcement & Messaging Tool — MCP Server
Exposes draft_message, send_email, send_slack as tools for Claude Code.
Run via: claude mcp add csee-messaging python path/to/mcp_server.py
"""

import sys
import io
import json
import os

# Force UTF-8 on stdin/stdout so emoji and non-ASCII characters
# are not mangled into surrogate pairs on Windows.
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

TOOLS = [
    {
        "name": "draft_message",
        "description": "Draft a CSEE message (email or Slack) from a plain English request. Returns the full draft with channel, subject, and message body.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "request": {
                    "type": "string",
                    "description": "Plain English description of the message to draft, including all known details (deadlines, names, links, etc.)"
                },
                "phase": {
                    "type": "string",
                    "description": "Optional. The practical-course phase this message belongs to, matching a folder under .claude/skills/ (e.g. 'phase-01-acceptance', 'phase-02-events'). When set, only that phase's templates are loaded. Omit to consider all phases."
                }
            },
            "required": ["request"]
        }
    },
    {
        "name": "send_email",
        "description": "Send an email to all recipients listed in recipients_email.txt",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "Email subject line"},
                "message": {"type": "string", "description": "Full email body"}
            },
            "required": ["subject", "message"]
        }
    }
]


def handle_tool(name: str, arguments: dict) -> str:
    if name == "draft_message":
        from draft_message import _run_claude, build_system_prompt
        system = build_system_prompt(arguments.get("phase"))
        return _run_claude(arguments["request"], system=system)

    elif name == "send_email":
        from send_email import send_email as _send_email
        from draft_message import _load_recipients
        recipients = _load_recipients("recipients_email.txt")
        failed = _send_email(arguments["subject"], arguments["message"], recipients)
        if failed:
            return f"Sent, but failed for: {', '.join(failed)}"
        return f"Email sent successfully to {len(recipients)} recipient(s)."

    return f"Unknown tool: {name}"


def write(obj: dict):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = req.get("method", "")
        req_id = req.get("id")

        if method == "initialize":
            write({
                "jsonrpc": "2.0", "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "csee-messaging", "version": "1.0.0"}
                }
            })

        elif method == "tools/list":
            write({"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}})

        elif method == "tools/call":
            params = req.get("params", {})
            try:
                result = handle_tool(params.get("name"), params.get("arguments", {}))
                write({
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {"content": [{"type": "text", "text": result}]}
                })
            except Exception as e:
                write({
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True}
                })

        elif method == "notifications/initialized":
            pass

        elif req_id is not None:
            write({"jsonrpc": "2.0", "id": req_id,
                   "error": {"code": -32601, "message": f"Method not found: {method}"}})


if __name__ == "__main__":
    main()
