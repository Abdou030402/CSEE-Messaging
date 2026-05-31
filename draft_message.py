#!/usr/bin/env python3
"""
CSEE Messaging Tool
Usage: python draft_message.py
"""

import re
import glob
import json
import subprocess
import sys
import os
import shutil
from typing import Optional, Tuple

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(SKILL_DIR, ".claude", "skills")


def _load_recipients(filename: str) -> list:
    path = os.path.join(SKILL_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def _read_first_existing(*filenames: str) -> str:
    """Return the contents of the first file that exists, else ''.
    Lets a gitignored local file (real data) override a committed example."""
    for name in filenames:
        path = os.path.join(SKILL_DIR, name)
        if os.path.exists(path):
            return open(path, encoding="utf-8").read()
    return ""


_SIGNATURE = _read_first_existing("signature.txt", "signature.example.txt").strip()


def _load_templates(phase: Optional[str] = None) -> str:
    """Concatenate template .md files. If `phase` is given (a folder name under
    .claude/skills/, e.g. 'phase-01-acceptance'), load only that phase's
    templates; otherwise load every phase's templates. Falls back to a legacy
    top-level templates/ dir if no skill templates are found."""
    if phase:
        roots = [os.path.join(SKILLS_DIR, phase, "templates")]
    else:
        roots = sorted(glob.glob(os.path.join(SKILLS_DIR, "*", "templates")))

    if not any(os.path.isdir(r) for r in roots):
        legacy = os.path.join(SKILL_DIR, "templates")
        if os.path.isdir(legacy):
            roots = [legacy]

    chunks = []
    for root in roots:
        for path in sorted(glob.glob(os.path.join(root, "*.md"))):
            chunks.append(open(path, encoding="utf-8").read())
    return "\n\n".join(chunks)


def build_system_prompt(phase: Optional[str] = None) -> str:
    """Build the drafting system prompt: shared CSEE style guide + signature +
    the relevant phase's templates + real examples."""
    style_guide = open(f"{SKILL_DIR}/style_guide.md", encoding="utf-8").read()
    examples = _read_first_existing("examples/historical_messages.md",
                                    "examples/historical_messages.example.md")
    return f"""
You are a messaging assistant for the Center for Software Engineering Excellence (CSEE), drafting communications on behalf of the CSEE team.

Read the style guide and examples below, then draft the requested message.

--- EMAIL SIGNATURE (end EVERY email with this EXACT block, verbatim) ---
{_SIGNATURE}

--- CSEE STYLE GUIDE ---
{style_guide}

--- TEMPLATES ---
{_load_templates(phase)}

--- REAL EXAMPLES ---
{examples}

Always output EXACTLY in this format (no extra text before or after):
CHANNEL: Email|Slack
SUBJECT: <subject line or N/A>
MESSAGE:
<full ready-to-send message body>

IMPORTANT RULES:
- NEVER use placeholders like [PLACEHOLDER] or [FIELD_NAME]. Only write what you actually know.
- If a detail is missing, omit that section or sentence entirely. Write naturally around what you have.
- NEVER ask clarifying questions. Always draft immediately.
- Do not add any text outside the CHANNEL/SUBJECT/MESSAGE block.
- If CHANNEL is Email: write plain text only — no markdown, no asterisks, no underscores.
- If CHANNEL is Slack: use Slack markdown (*bold*, _italic_, bullet points, emojis) as specified in the formatting rules above.
"""


# Default prompt (all phases) for the interactive CLI / backward compatibility.
SYSTEM_PROMPT = build_system_prompt()

MISSING_FIELDS_PROMPT = """
The user wants to draft this message: "{request}"

Identify the message type and list ONLY the fields that are missing from the request but would make the message noticeably better or more complete.
Do not list optional or nice-to-have fields — only genuinely important missing info.

Output a JSON array of short human-readable field names, or an empty array [] if nothing important is missing.
Examples: ["end time", "location", "agenda items"] or []
Output ONLY the JSON array, nothing else.
"""


def _find_claude() -> str:
    cmd = shutil.which("claude")
    if cmd and os.name == "nt" and cmd.lower().endswith(".cmd"):
        exe = os.path.join(os.path.dirname(cmd),
                           "node_modules", "@anthropic-ai", "claude-code", "bin", "claude.exe")
        if os.path.exists(exe):
            return exe
    return cmd or "claude"


def _run_claude(prompt: str, system: Optional[str] = None) -> str:
    args = [_find_claude(), "-p", prompt,
            "--strict-mcp-config", "--no-session-persistence", "--tools", ""]
    if system:
        args += ["--system-prompt", system]
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    return result.stdout.strip()


def collect_missing_fields(user_input: str) -> str:
    """Ask Claude what's missing, prompt the user, return enriched input."""
    raw = _run_claude(MISSING_FIELDS_PROMPT.format(request=user_input))
    try:
        missing = json.loads(raw)
    except Exception:
        return user_input

    if not missing:
        return user_input

    print("\nA few details are missing. Press Enter to skip any:")
    extras = []
    for field in missing:
        val = input(f"  {field}: ").strip()
        if val:
            extras.append(f"{field}: {val}")

    if extras:
        return user_input + "\nAdditional details: " + ", ".join(extras)
    return user_input


def parse_draft(output: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    channel_match = re.search(r"^CHANNEL:\s*(.+)", output, re.IGNORECASE | re.MULTILINE)
    subject_match = re.search(r"^SUBJECT:\s*(.+)", output, re.IGNORECASE | re.MULTILINE)
    message_match = re.search(r"^MESSAGE:\s*\n([\s\S]+)", output, re.IGNORECASE | re.MULTILINE)

    channel = channel_match.group(1).strip() if channel_match else None
    subject = subject_match.group(1).strip() if subject_match else None
    message = message_match.group(1).strip() if message_match else None
    return channel, subject, message


def main():
    print("\n=== CSEE Messaging Tool ===")
    print("Describe the message you want to draft.")
    print("Example: 'Draft an acceptance email for JST WS 2025/26, confirmation deadline Oct 5th 23:59, drop deadline Oct 13th 23:59'\n")

    user_input = input("Your request: ").strip()
    if not user_input:
        print("No input provided.")
        sys.exit(1)

    user_input = collect_missing_fields(user_input)

    print("\nDrafting your message...\n")

    output = _run_claude(user_input, system=SYSTEM_PROMPT)

    if not output:
        print("Error: no response from Claude.")
        sys.exit(1)

    print("=" * 50)
    print(output)
    print("=" * 50)

    channel, subject, message = parse_draft(output)

    if not channel or not message:
        print("\nCould not parse channel/message from output. Nothing sent.")
        return

    print(f"\nChannel detected: {channel}")

    if "email" in channel.lower():
        recipients = _load_recipients("recipients_email.txt")
        recipients_str = ", ".join(recipients)
        confirm = input(f"\nSend to [{recipients_str}]? (y/n): ").strip().lower()
        if confirm != "y":
            print("Not sent.")
            return
        if not subject or subject.upper() == "N/A":
            subject = input("Enter subject line: ").strip()
        from send_email import send_email
        failed = send_email(subject, message, recipients)
        if failed:
            print(f"\nFailed recipients: {', '.join(failed)}")
        else:
            print("\nAll messages sent successfully.")
    elif "slack" in channel.lower():
        print("\nSlack sending is handled via the official Slack MCP server in Claude Code.")
        print("Open this folder in Claude Code and ask Claude to send the message above.")
    else:
        print(f"Unknown channel '{channel}'. Nothing sent.")


if __name__ == "__main__":
    main()
