# AI-Powered Course Announcement & Messaging Tool

Draft and send CSEE course announcements, emails, and Slack messages by simply describing them in plain English to Claude Code.

---

## Prerequisites

- [Claude Code](https://claude.ai/code)
- Python 3.9+
- A Gmail account with 2-Step Verification enabled (for sending email)

---

## Setup (one-time, ~5 minutes)

### 1. Clone and install

```bash
git clone https://github.com/Abdou030402/CSEE-Messaging.git
cd CSEE-Messaging
pip install -r requirements.txt
```

### 2. Add your Gmail credentials

Email is sent from your own Gmail using an **App Password** — a one-time token, no Google Cloud or OAuth setup:

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select **Mail**, click **Generate**, and copy the 16-character password.

Then create your `.env`:

```bash
cp .env.example .env
```

Edit it:

```
GMAIL_SENDER=you@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

### 3. Open in Claude Code

```bash
claude .
```

Click **Allow** when prompted to trust the project's MCP servers.

---

## Usage

Just describe what you want in plain English. Claude drafts the message, shows it to you, and sends it once you confirm:

```
draft an acceptance email for JST WS 2025/26, confirm by Oct 5th 23:59, drop by Oct 13th 23:59
```

```
post to #announcements that the JST kickoff is on June 3rd at 18:00 in room MI 01.09.014
```

The first time you ask Claude to send a **Slack** message, it walks you through a one-time browser login — just follow the steps it gives you. After that, it sends automatically.
