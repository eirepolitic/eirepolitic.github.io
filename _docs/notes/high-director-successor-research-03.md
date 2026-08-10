---
title: High Director Successor Research 03 — Mobile, Notifications, Authentication, and Voice
summary: Current-market research for the successor phone experience, covering PWA versus native delivery, Web Push notifications, passkey authentication, microphone capture, and provider-neutral speech-to-text/text-to-speech.
section: notes
doc_type: note
status: active
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
owner: High Director
order: 118
permalink: /projects/notes/high-director-successor-research-03/
tags:
  - high-director
  - successor
  - research
  - pwa
  - mobile
  - notifications
  - passkeys
  - voice
  - speech-to-text
  - text-to-speech
---

# High Director Successor Research 03 — Mobile, Notifications, Authentication, and Voice

## Purpose

This is the third current-market research pass for the High Director successor. It evaluates how the owner should interact with the Manager Agent from a phone through text and optional voice, while keeping the client simple and avoiding unnecessary native-app/platform lock-in.

The key question is whether a Progressive Web App (PWA) is sufficient for the initial product or whether a native/cross-platform mobile shell is required from the beginning.

## Current Working Recommendation

The strongest MVP client architecture found is:

```text
Installable PWA on phone
      |
      +--> text chat
      +--> task/progress views
      +--> push-to-talk microphone recording
      +--> audio playback
      +--> Web Push notifications
      +--> passkey authentication
      |
      v
owner-controlled HTTPS backend
      |
      +--> persistent Manager conversation
      +--> STT adapter
      +--> TTS adapter
      +--> notification/Web Push service
      +--> Manager/developer orchestration
```

**Working recommendation:** build the first phone client as a standards-based PWA. Do not build a native application until a concrete PWA limitation is demonstrated by prototype testing.

If native capabilities later become necessary, wrap/reuse the web client with **Capacitor** or build a dedicated mobile client against the same backend API. The backend/conversation model should not depend on the client implementation.

## Why a PWA Currently Fits the Requirement

The phone does not need to run the Manager or Developer Agents while the application is closed. All autonomous work occurs on the server-side control plane and Developer Agent workers.

The phone only needs to:

- send owner messages;
- capture optional voice input;
- display Manager responses;
- play optional spoken summaries;
- receive notifications;
- allow the owner to answer decisions/questions;
- display task/developer status;
- authenticate securely.

Those capabilities are now available through modern web-platform APIs.

## iPhone/iPad Web Push Support

Apple supports Web Push for Home Screen web apps on iOS/iPadOS 16.4 and later.

Apple explicitly describes this as standards-based Web Push. Home Screen web apps can receive notifications and badge updates. The application should use a standalone web-app manifest so the installed Home Screen application behaves as a web app rather than merely opening as a normal browser shortcut.

Sources:

- https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers
- https://developer.apple.com/videos/play/wwdc2023/10120/
- https://developer.apple.com/safari/

Apple's Safari documentation also states that standards-based Web Push does not require Apple Developer Program membership. This is a meaningful advantage over a native iOS push implementation for the first version.

## Notification Architecture

The Manager should send notifications only for events important enough to require or deserve owner attention.

Examples:

- owner decision required;
- agent blocked in a way the Manager cannot resolve;
- validation/deployment failure requiring a decision;
- major milestone completed;
- task completed;
- budget/security guardrail triggered.

Routine Developer Agent chatter must not produce phone notifications.

### Proposed Web Push model

```text
PWA requests notification permission
       |
       v
browser creates PushSubscription
       |
       v
subscription stored in control-plane DB
       |
       v
Manager creates notification event
       |
       v
server sends standards-based Web Push
       |
       v
phone OS/browser push infrastructure
       |
       v
notification opens relevant conversation/task
```

The application should store standard push subscription data rather than binding its database schema to a commercial notification provider.

This lets the server implement standards-based Web Push directly. A managed notification service could still be introduced later behind the same internal notification interface if operational convenience warrants it.

## PWA Background Limitation Is Not a Major Problem Here

Mobile browsers constrain arbitrary background JavaScript execution. That would be a major limitation for an application that expected the phone itself to continue processing a long-running task.

The successor does not have that architecture.

The Manager workflow, Developer Agents, task queues, validation monitoring, and notifications run on the server. The phone can be entirely asleep/closed between interactions. Web Push is the mechanism that brings the owner back when required.

This server-side architecture therefore turns one of the main PWA limitations into a non-issue for the core product.

## Microphone Capture

Modern PWAs can capture microphone input using the Media Capture and Streams APIs.

`getUserMedia()` requires HTTPS/secure context and explicit user permission before the microphone can be opened.

Sources:

- https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
- https://web.dev/learn/pwa/capabilities

The intended interaction is **push-to-talk**, not an always-open voice call:

```text
Owner presses microphone button
       |
       v
PWA begins local audio capture
       |
       v
Owner speaks
       |
       v
Owner releases/stops recording
       |
       v
audio uploaded to backend
       |
       v
STT adapter returns transcript
       |
       v
transcript becomes normal Manager message
```

The transcript should be shown to the owner and retained as the canonical text message. Raw audio retention should be configurable and should default to deletion after successful transcription unless a later product requirement justifies long-term retention.

## Why Push-to-Talk Is Better Than Realtime Voice for v1

The described use case is naturally turn-based: press a button, say the request/answer, receive a Manager response.

A realtime bidirectional audio session would add:

- persistent WebRTC/WebSocket session management;
- voice activity detection;
- interruption/barge-in behavior;
- more complicated mobile background/foreground handling;
- more expensive realtime audio-model usage in some services;
- tighter coupling between speech and LLM providers.

Push-to-talk keeps voice as an adapter around the existing text conversation. It can later be upgraded to realtime voice without changing the Manager/developer architecture.

## Speakable Manager Responses

The Manager should always create a normal technical text response first.

When voice output is enabled, a separate **speakable summary** should then be produced, for example:

```text
Full text response:
- technical progress
- exact PR/test/deployment information
- decisions and alternatives

Speakable summary:
"The developer finished the API change and tests passed. I need you to choose whether the new endpoint should be public or authenticated before I continue. I recommend authenticated."
```

Only the short summary should be synthesized to audio by default. This reduces listening time and TTS cost while preserving full detail in the chat.

## Speech Provider Abstraction

Speech should use its own provider-neutral interfaces rather than being hardwired to the selected Manager LLM provider.

Suggested internal contracts:

```text
SpeechToText.transcribe(audio, language?, hints?) -> transcript
TextToSpeech.synthesize(text, voice_profile?) -> audio
```

Provider adapters can then implement AWS, Google, OpenAI, or future/local speech engines without changing the chat, persistence, Manager, or mobile application.

The system should persist provider/model identifiers and usage/cost metadata with each speech operation for later comparison.

## Speech-to-Text Cost Is Small for This Use Case

Current official API pricing demonstrates that push-to-talk transcription is inexpensive relative to LLM reasoning/developer usage.

Examples from currently available services include:

- OpenAI `gpt-4o-mini-transcribe`: estimated **$0.003/minute**;
- OpenAI `gpt-transcribe`: estimated **$0.0045/minute**;
- AWS standard batch transcription example: **$0.006/minute**;
- Google Speech-to-Text V2 standard recognition: **$0.016/minute** at the first usage tier;
- Google V2 dynamic batch: **$0.003/minute**, with lower urgency.

Sources:

- https://developers.openai.com/api/docs/pricing
- https://aws.amazon.com/transcribe/pricing/
- https://cloud.google.com/speech-to-text/pricing

Illustrative monthly transcription cost at $0.003/minute:

| Recorded owner speech/month | Approx. cost |
| ---: | ---: |
| 300 minutes | $0.90 |
| 500 minutes | $1.50 |
| 1,000 minutes | $3.00 |

Actual provider selection must be based on transcription quality, latency, language/accent handling, privacy, and operational fit—not price alone.

## Text-to-Speech Cost Is Also Likely Minor

Because only short Manager summaries need to be spoken, monthly TTS volume should be low.

For reference, current Amazon Polly pricing is:

- Standard voices: **$4 per 1 million characters**;
- Neural voices: **$16 per 1 million characters**;
- Generative voices: **$30 per 1 million characters**.

Source: https://aws.amazon.com/polly/pricing/

At 100,000 synthesized characters/month, this is approximately:

- $0.40 Standard;
- $1.60 Neural;
- $3.00 Generative.

Google also offers multiple TTS models with character/token-based pricing and free usage allowances for several voice families.

Source: https://cloud.google.com/text-to-speech/pricing

The voice layer therefore appears unlikely to dominate operating cost if the system synthesizes concise summaries rather than every raw Developer Agent response.

## Initial Speech Provider Decision

No speech provider should be selected solely from desk research.

The prototype should benchmark at least two STT providers and two TTS providers using the owner's actual phone recordings and preferred output style.

Evaluation criteria:

- transcription accuracy;
- punctuation and technical vocabulary;
- latency after releasing the microphone button;
- audio upload size/format support;
- voice naturalness;
- response-start latency;
- cost;
- privacy/data-retention controls;
- API simplicity;
- provider independence from the selected Manager LLM.

The system architecture should allow STT and TTS to use different providers.

## Authentication — Passkeys Are the Current Front-Runner

The application will control powerful GitHub/infrastructure agents, so phone authentication must be stronger than a simple persistent password.

WebAuthn provides public-key authentication for web applications. Passkeys are implemented through WebAuthn and can use platform authenticators such as Face ID, Touch ID, fingerprints, device PINs, or hardware security keys.

Sources:

- https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API
- https://developer.apple.com/passkeys/
- https://developer.apple.com/videos/play/wwdc2022/10092/

### Proposed owner-only authentication model

For the initial single-owner system:

1. bootstrap the first owner account through a controlled setup procedure;
2. register one or more passkeys;
3. use short-lived authenticated web sessions after successful WebAuthn verification;
4. require recent/re-authentication for sensitive approvals where appropriate;
5. retain offline recovery codes or another deliberately designed recovery mechanism;
6. do not make Google/GitHub/social login the only route into the control plane.

This keeps the application's identity boundary under owner control while still taking advantage of secure device authenticators.

The exact WebAuthn server library and recovery procedure remain implementation decisions.

## Native App / Capacitor Fallback

Capacitor provides native iOS/Android access around a web application and has a native Push Notifications API.

Source: https://capacitorjs.com/docs/apis/push-notifications

A Capacitor wrapper becomes attractive if testing shows a requirement for:

- more reliable native notification behavior;
- native share-sheet integrations;
- Siri/Shortcuts-style entry points;
- deeper background audio/session integration;
- native widgets;
- app-store distribution;
- device APIs unavailable or inconsistent in the PWA.

However, native iOS push setup requires Apple push capabilities and the Capacitor/Firebase documentation notes that testing iOS push requires a paid Apple Developer account.

Source: https://capacitorjs.com/docs/guides/push-notifications-firebase

None of these native-only capabilities are currently required for the core successor workflow.

## Recommended First Phone Prototype

The minimum useful client should have five screens/states rather than attempting to recreate a full desktop IDE.

### 1. Manager Chat

- persistent chronological Manager conversation;
- text input;
- push-to-talk button;
- optional play-speakable-summary button;
- streaming text updates where useful.

### 2. Active Work

- active tasks;
- repository;
- current phase;
- Developer Agent status;
- latest Manager summary;
- whether owner input is required.

### 3. Decision Required

A focused decision card containing:

- what happened;
- why owner input is needed;
- available choices;
- Manager recommendation;
- text/voice response controls.

### 4. Completed Work

- result summary;
- repository/PR/workflow/deployment references;
- final cost/usage summary;
- link back to the Manager conversation.

### 5. Settings

- notification preferences;
- voice on/off and voice choice;
- passkey/security settings;
- model/provider preferences at a high level;
- cost/budget limits;
- active device/session management.

## Notification UX Rule

The Manager should distinguish **conversation updates** from **interruptions**.

Messages can accumulate silently in the chat while the owner is away. Push notifications should be reserved for meaningful events.

Suggested severity levels:

```text
INFO
  visible in chat/task timeline only

MILESTONE
  optional push notification

OWNER_INPUT_REQUIRED
  push notification + badge

SECURITY_OR_COST_ALERT
  high-priority push + explicit acknowledgement

TASK_COMPLETE
  push notification unless disabled
```

This policy should be deterministic application logic, not an unstructured decision made independently by the LLM for every message.

## Offline and Reconnection Behavior

The PWA should cache the application shell and recent conversation/task metadata for usability, but the server remains authoritative.

Owner messages should receive a client-generated idempotency key before submission so reconnect/retry does not create duplicate Manager messages or approvals.

Voice recordings awaiting upload should visibly remain pending rather than being silently discarded.

## Security and Privacy

The mobile/voice layer should follow these principles:

- HTTPS only;
- passkey/WebAuthn authentication;
- secure, HTTP-only session cookies where applicable;
- CSRF protections appropriate to the API/session design;
- short session lifetime for high-value operations;
- optional re-authentication before sensitive approvals;
- microphone access only during explicit owner action;
- clear recording indicator;
- raw audio deleted after transcription by default;
- transcripts retained as normal owner messages under owner-controlled storage;
- Web Push subscription endpoints treated as sensitive application data;
- no GitHub/cloud credentials stored in the PWA;
- no direct phone-to-Developer-Worker access.

## Current Ranking

| Approach | Current status | Reason |
| --- | --- | --- |
| Installable PWA | **Front-runner** | One client, no app-store dependency, iOS Web Push, microphone/WebAuthn support, matches server-side background architecture |
| PWA later wrapped with Capacitor | **Primary fallback** | Reuses web UI while gaining native notifications/device APIs if needed |
| React Native/native app from day one | Not justified yet | Higher implementation/deployment overhead without a verified required native capability |
| Continuous realtime voice session | Not justified for v1 | More cost/complexity; push-to-talk directly matches requested interaction style |
| Push-to-talk STT + optional TTS | **Front-runner** | Cheap, simple, provider-neutral, preserves text as canonical conversation |
| Social/OAuth-only login | Not preferred | Adds unnecessary identity-provider dependency for a single-owner control plane |
| Passkey/WebAuthn login | **Front-runner** | Strong standards-based authentication using device biometrics/security authenticators |

## Prototype Tests Required

Before finalizing PWA as the mobile architecture, build a small test client and verify on the owner's actual phone:

1. Add to Home Screen/install experience.
2. Receive Web Push while the PWA is closed.
3. Tap notification and deep-link to the correct task/conversation.
4. Record microphone audio reliably.
5. Upload and transcribe a multi-minute spoken request.
6. Play synthesized Manager audio.
7. Create/login with passkey.
8. Recover cleanly after network loss.
9. Verify session handling when moving between browser and installed PWA.
10. Measure perceived end-to-end latency for text and push-to-talk interactions.

If these tests pass, a native application is unnecessary for the MVP.

## Next Research Pass

The next architecture-critical research pass should focus on **LLM providers, coding models, context/caching behavior, and realistic API cost**.

It should answer:

- which current model(s) are suitable for the Manager role;
- which current model(s) work well through OpenHands for Developer Agents;
- whether Manager and Developer should use different models/providers;
- input/output/cached-token pricing;
- provider prompt-caching behavior;
- context-window implications;
- tool-use/structured-output support;
- model switching/fallback strategy;
- monthly cost scenarios for light, normal, and heavy development usage;
- which model-specific features must stay outside the provider-neutral core contract.

That pass should combine current API pricing with realistic token measurements from a later prototype rather than assuming ChatGPT subscription economics translate directly to API usage.

## Related Documents

- [High Director Successor — Initial System Concept](/projects/notes/high-director-successor-concept/)
- [Research 01 — Agent Runtime and Control Plane](/projects/notes/high-director-successor-research-01/)
- [Research 02 — Hosting and Cost Architecture](/projects/notes/high-director-successor-research-02/)

## Verification Record

- Last verified: `2026-08-09`
- Verified against: current Apple Safari/Web Push/passkey documentation, web.dev/MDN PWA and MediaDevices/WebAuthn documentation, Capacitor push documentation, and current official OpenAI/AWS/Google speech API/pricing documentation.
- Verified by: High Director
- Verification scope: PWA feasibility, iOS Web Push, microphone capture, passkey authentication, native-wrapper fallback, push-to-talk architecture, speech-provider abstraction, and first-pass speech cost.
- Unverified areas: actual behavior on the owner's phone, browser-specific recording formats, real push delivery latency, speech quality for the owner's voice, passkey recovery UX, and whether any future desired mobile feature requires native APIs.
