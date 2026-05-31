# AI-Powered Course Announcement & Messaging Tool

## Purpose
Draft course-related announcements, emails, and Slack messages for the Center for Software Engineering Excellence (CSEE), on behalf of the CSEE team.

## Sender Identity
- **Organization:** Center for Software Engineering Excellence gGmbH (CSEE)
- **Email signature block:** every email ends with the signature loaded from `signature.txt` (gitignored; falls back to `signature.example.txt`). It is injected into the system prompt at runtime — use it verbatim. To set yours: `cp signature.example.txt signature.txt` and edit.

## Courses
- **JST** — JavaScript Technology Practical Course
- **TPL** — (Template/other practical course)
- Courses run on semester cycles: Winter Semester (WS) and Summer Semester (SS)

## Tone & Style Rules
- Warm but professional. Celebratory when appropriate (acceptances, welcomes).
- Always include a clear deadline with exact date and time (e.g. `Saturday, Aug 24th, 23:59`).
- Consequences of missing deadlines must be stated clearly but not harshly.
- Never use jargon. Audience is university students (mostly non-native English speakers).

## Formatting by Channel

### Email (plain text — no markdown)
- Emails are sent as plain text. Do NOT use markdown syntax (*bold*, **bold**, _italic_, etc.).
- Use ALL CAPS sparingly for emphasis on critical deadlines (e.g. BEFORE Sunday, Oct 5th, 23:59).
- Use dashes (-) for bullet points, blank lines between paragraphs.
- Use numbered lists (1. 2. 3.) for multi-step instructions.
- Start with a formal greeting: "Dear [Name]," or "Dear participants,"
- End with the full signature block (the exact text is provided in the system prompt, loaded from `signature.txt`).
- Subject line is always required.

### Slack (Slack markdown)
- Use Slack's native markdown: *bold* for emphasis, _italic_ if needed, `code` for links or short strings.
- Use bullet points with - or • for lists.
- Keep it conversational and shorter than the equivalent email.
- Start with a casual greeting: "Hey team 👋" or "Hi everyone,"
- No signature block.
- Emojis are appropriate — use them to highlight key items (e.g. ⚠️ for deadlines, ✅ for actions).
- Bold deadlines and action items: *Sunday, Oct 5th, 23:59*

## Message Types

### 1. Acceptance Email
Sent to students accepted into a practical course.
Required inputs: `course_name`, `semester`, `slack_invite_link`, `confirmation_deadline`, `drop_deadline`
See: `examples/acceptance_email.md`

### 2. Event Invitation Email
Sent to all participants for demos, workshops, kickoffs.
Required inputs: `event_name`, `date`, `time`, `location`, `location_link`, `agenda_items[]`
See: `examples/event_invitation_email.md`

### 3. Slack Welcome + Contract Message
Sent to new fellows/team members on Slack.
Required inputs: `recipient_first_name`, `batch_name`, `folder_link`, `translation_link`, `payment_note`
See: `examples/slack_welcome_contract.md`

### 4. Reminder Message (email or Slack)
Sent before a deadline or event.
Required inputs: `what`, `deadline`, `action_required`, `channel` (email or slack)

### 5. General Announcement
Flexible. Used for updates, changes, info drops.
Required inputs: `topic`, `body_points[]`, `channel`, `urgency` (normal / important / urgent)

## How to Use This Skill

When asked to draft a message, Claude should:
1. Identify the message type from the request
2. Ask for any missing required inputs before drafting
3. Draft the message using the correct tone, format, and signature for the channel
4. Output: subject line (if email) + full message body, ready to copy-paste
5. Optionally suggest a send date/time if scheduling context is provided

## Sending Integration
- Email: Gmail SMTP via `send_email.py` (uses app password from `.env`)
- Slack: Official Slack MCP connector (remote, OAuth — authenticate once with `/mcp`; posts as the signed-in user)
