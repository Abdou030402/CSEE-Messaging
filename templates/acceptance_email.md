# Template: Acceptance Email

## Subject
`Acceptance – {{course_name}} Practical Course {{semester}}`

## Body

```
Congratulations!

We are very happy to inform you that you have been accepted as a Developer in the {{course_name}} Practical Course for the {{semester}}.

Your application stood out among over {{applicant_count}} other motivated students. You have shown the technical competency and motivation we were looking for. Well done!

IMPORTANT:
---------------------
Please confirm your participation in the practical course by joining our Slack space via the link below until **{{confirmation_deadline}}**. We will provide more info there after this deadline.

Join Slack: [here >]({{slack_invite_link}})

Furthermore, if you cannot join the course next semester, please inform us via mail ASAP so we can admit other students eagerly waiting to get a spot. If you want to drop the course, you must do this before **{{drop_deadline}}**. Students who decide to drop the practical course after this deadline receive a 5.0 as required by TUM.
---------------------

We look forward to working with you and hope you are as excited as we are!

{{signature}}
```

> `{{signature}}` is the signature block loaded from `signature.txt` (see `signature.example.txt`).

## Variables
| Variable | Example |
|---|---|
| `{{course_name}}` | JavaScript Technology (JST) |
| `{{semester}}` | winter semester 2025/26 |
| `{{applicant_count}}` | 500 |
| `{{confirmation_deadline}}` | Saturday, Aug 24th, 23:59 |
| `{{slack_invite_link}}` | https://join.slack.com/... |
| `{{drop_deadline}}` | Sunday, Sep 1st, 23:59 |
