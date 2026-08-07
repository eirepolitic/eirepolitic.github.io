---
title: High Director Google Workspace Action
summary: Authoritative Google Workspace GPT Action contract for Gmail and Google Calendar, including OAuth authentication state, operation catalogue, confirmation rules, and data/security boundaries.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 23
permalink: /projects/high-director/google-workspace-action/
---

# High Director Google Workspace Action

## Purpose

This page documents the user-supplied authoritative GPT Action configuration for the High Director Google Workspace integration.

## Evidence classification

**User-supplied authoritative source**, supplied on 2026-08-06.

The source consisted of:

- GPT Action authentication selection: `OAuth`;
- complete pasted OpenAPI schema titled `Google Workspace API`, version `1.2.0`.

The pasted text contained Markdown escaping/link formatting around YAML list markers and server URLs. The technical schema is normalized below for documentation; operation IDs, paths, fields, enums, constraints, descriptions, and response structures are preserved.

## Action identity

| Field | Authoritative value |
|---|---|
| OpenAPI version | `3.1.0` |
| API title | `Google Workspace API` |
| API version | `1.2.0` |
| GPT authentication selection | `OAuth` |
| Primary server | `https://www.googleapis.com` |
| Gmail operation server | `https://gmail.googleapis.com` |
| Operation count | `12` |
| Google services verified | Google Calendar API and Gmail API |

The schema description states that the Action can read Gmail, send email, and manage Google Calendar events for the authenticated Google account.

## Operation catalogue

### Google Calendar

| Operation ID | Method | Path | Capability |
|---|---|---|---|
| `listGoogleCalendars` | `GET` | `/calendar/v3/users/me/calendarList` | List calendars available to the authenticated account |
| `listCalendarEvents` | `GET` | `/calendar/v3/calendars/{calendarId}/events` | Search/list calendar events |
| `createCalendarEvent` | `POST` | `/calendar/v3/calendars/{calendarId}/events` | Create a calendar event |
| `getCalendarEvent` | `GET` | `/calendar/v3/calendars/{calendarId}/events/{eventId}` | Retrieve one event |
| `updateCalendarEvent` | `PATCH` | `/calendar/v3/calendars/{calendarId}/events/{eventId}` | Update selected event fields |
| `deleteCalendarEvent` | `DELETE` | `/calendar/v3/calendars/{calendarId}/events/{eventId}` | Delete an event |
| `moveCalendarEvent` | `POST` | `/calendar/v3/calendars/{calendarId}/events/{eventId}/move` | Move an event to another calendar |

### Gmail

| Operation ID | Method | Path | Capability |
|---|---|---|---|
| `getGmailProfile` | `GET` | `/gmail/v1/users/me/profile` | Return authenticated Gmail profile/mailbox totals |
| `searchGmailMessages` | `GET` | `/gmail/v1/users/me/messages` | Search/list matching Gmail message IDs |
| `getGmailMessage` | `GET` | `/gmail/v1/users/me/messages/{messageId}` | Retrieve message headers/body parts/attachment references |
| `getGmailAttachment` | `GET` | `/gmail/v1/users/me/messages/{messageId}/attachments/{attachmentId}` | Retrieve base64url-encoded attachment data |
| `sendGmailMessage` | `POST` | `/gmail/v1/users/me/messages/send` | Send an RFC 2822 MIME message encoded as base64url |

## OAuth boundary

The GPT Action authentication type is authoritatively verified as **OAuth**.

The supplied OpenAPI schema does not include OAuth `securitySchemes`, scope names, authorization URL, token URL, client ID, or client secret. Those values are configured outside this schema in the GPT Action authentication settings and remain **unknown / unverified**.

No OAuth client secret, access token, refresh token, authorization code, or authenticated-account identifier was supplied or published.

## Calendar data model

The schema supports calendar-list metadata including:

- calendar ID;
- summary/description/location;
- time zone;
- primary/selected flags;
- access role.

Event reads can return:

- event ID/status/link;
- summary, description, and location;
- start/end date or date-time/time zone;
- attendees and response status;
- recurrence data;
- organizer information;
- conference/Google Meet entry-point metadata.

Event creation/update supports:

- title/description/location;
- all-day or timed start/end;
- attendee arrays;
- recurrence rules;
- reminders;
- color/visibility/transparency;
- guest permissions;
- Google Meet creation via `conferenceDataVersion=1` and `conferenceData.createRequest`.

`sendUpdates` supports `all`, `externalOnly`, or `none`, defaulting to `all` on create/update/delete/move operations where defined.

## Calendar safety/confirmation rules in the schema

The authoritative operation descriptions explicitly require user confirmation for write-sensitive calendar actions:

- `createCalendarEvent`: confirm calendar, title, date, time, guests, and notification behavior before creation;
- `updateCalendarEvent`: retrieve the event first when needed and obtain confirmation before applying changes;
- `deleteCalendarEvent`: delete only after explicit user confirmation;
- `moveCalendarEvent`: move/change organizer only after explicit user confirmation.

These are part of the Action contract's descriptive operating model. They are not Google API-enforced transactional controls by themselves.

## Gmail data model

### Profile

`getGmailProfile` can return:

- authenticated email address;
- total message count;
- total thread count;
- history ID.

### Search/list

`searchGmailMessages` supports:

- Gmail search query `q`;
- repeated `labelIds`;
- optional spam/trash inclusion;
- pagination and maximum result count.

It returns message/thread IDs rather than full message bodies.

### Message retrieval

`getGmailMessage` supports formats:

- `full`;
- `metadata`;
- `minimal`;
- `raw`.

The response can expose labels, snippet, history/internal-date metadata, raw data, MIME headers, MIME body data, nested parts, filenames, and attachment IDs.

### Attachments

`getGmailAttachment` returns attachment metadata plus base64url-encoded attachment data.

### Sending mail

`sendGmailMessage` accepts:

- `raw`: a complete RFC 2822 MIME message encoded as base64url without line breaks;
- optional `threadId` when replying in an existing thread.

The authoritative operation description requires the assistant to show **To, Cc, Bcc, Subject, and body and obtain explicit confirmation immediately before sending**.

## Security and privacy boundaries

Verified from this source:

- the integration acts on the authenticated Google account;
- authentication is OAuth-based;
- Gmail operations can expose email address, message metadata/content, raw MIME data, and attachments;
- Calendar operations can expose event descriptions, attendees, organizer addresses, locations, recurrence, and meeting links;
- the Action includes write capabilities for sending email and creating/updating/deleting/moving calendar events;
- confirmation requirements are embedded in descriptions for sensitive write actions.

Still unverified:

- OAuth scopes;
- OAuth authorization/token endpoint configuration;
- OAuth client identity and secret handling;
- token storage/refresh behavior;
- exact Google account connected at runtime;
- whether domain-wide delegation or Workspace administrator controls are involved;
- audit/logging configuration;
- revocation/reconnect procedure.

## Normalized authoritative OpenAPI source

The full user-supplied schema is preserved conceptually by this page and its exact operation/field catalogue. Because the pasted transport added Markdown escaping and hyperlink syntax that is not valid YAML, it is documented as a normalized transcription rather than a byte-for-byte source snapshot.

Key normalized server declarations are:

```yaml
servers:
  - url: https://www.googleapis.com
```

Gmail operations override the server with:

```yaml
servers:
  - url: https://gmail.googleapis.com
```

## Sanitization record

No secret values were present in the supplied schema. Publication retains the public Google API hostnames and all technically necessary operation/schema names.

No OAuth client secret, token, authenticated Gmail address, calendar ID, event ID, message ID, attachment data, or personal account identifier is published.

## Verification record

- Verified: `2026-08-06`
- Source: user-supplied GPT Action authentication selection and full OpenAPI schema text
- Authentication: OAuth
- Schema title/version: `Google Workspace API` / `1.2.0`
- Operations verified: 12
- Secret values published: none

## Related Documents

- [High Director GPT Configuration]({{ '/projects/high-director/gpt-configuration/' | relative_url }})
- [High Director Capability and Component Inventory]({{ '/docs/high-director/capability-component-inventory/' | relative_url }})
- [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }})
