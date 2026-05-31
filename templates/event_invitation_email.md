# Template: Event Invitation Email

## Subject
`{{event_name}} – {{date_short}}`

## Body

```
Hi everyone,

You are invited to {{event_name}}!

📅 Date: {{date_full}}
🕐 Time: {{time_start}} – {{time_end}} ({{timezone}})
📍 Location: {{location}} ({{location_link}})
✅ Participation: {{participation_note}}

Agenda:
{{agenda_items}}

{{closing_note}}

For more information, please check our Slack channel or contact the CSEE team directly.

{{signature}}
```

> `{{signature}}` is the signature block loaded from `signature.txt` (see `signature.example.txt`).

## Variables
| Variable | Example |
|---|---|
| `{{event_name}}` | 🚀 JST & TPL - Demo Day |
| `{{date_short}}` | Feb 7 |
| `{{date_full}}` | Friday, February 7th, 2025 |
| `{{time_start}}` | 15:45 |
| `{{time_end}}` | 19:30 |
| `{{timezone}}` | UTC+1 |
| `{{location}}` | MI Hörsaal 3, Garching Forschungszentrum |
| `{{location_link}}` | https://maps.app.goo.gl/... |
| `{{participation_note}}` | on-site (mandatory) |
| `{{agenda_items}}` | bullet list of times + activities |
| `{{closing_note}}` | e.g. after-party info |
