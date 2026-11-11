# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 21:11
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `7def313e-002a-444d-b716-41f0f2dc5b37` | unsure | 0.375 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c1630f89-c8d0-4171-a9dd-b8f7338da719` | unsure | 0.468 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `10fe12ce-f1dc-4597-95fe-1d047cf09324` | unsure | 0.566 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `cc79e267-c26b-4723-89ff-d68254935aed` | unsure | 0.593 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `7fe88b0c-b5ec-441b-80d0-e075fe0fc5dd` | unsure | 0.357 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `00f2d9c5-9bfb-4075-9a8f-c7b1cf9805e9` | unsure | 0.469 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `37780f9c-5f94-4f3b-90ab-4e1f03f9b26a` | unsure | 0.600 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `51b5eeff-2d7e-494e-9d58-5bc87c7e200e` | human | 0.345 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `a97c93aa-0aac-4347-b604-8c2cb0c9e077` | unsure | 0.584 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `d05536b9-ca92-4456-92ed-8af3ff514984` | ai | 0.859 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `61f9cc71-cb42-4154-b428-ba542cfcc222` | unsure | 0.575 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `b34497b8-d8c6-4409-b206-8678df8b0ebf` | unsure | 0.676 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `40bcc283-3e36-4c55-b2b4-95c68d382394` | unsure | 0.693 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `37aa003e-e5ec-4f81-8aee-7c9980afa51d` | unsure | 0.678 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `27440753-1b5b-46b0-8055-d0d001111bdb` | unsure | 0.709 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `aaf6bf73-f44b-4ab8-8e27-c80afcc1d2cf` | unsure | 0.691 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `1c54b71a-b989-4b6c-a221-653013c02b4d` | unsure | 0.687 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `495f949d-0ab8-4d4b-b4a0-e25d92bffaf8` | human | 0.256 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `d7b5e1f2-5d1c-4a07-b9b1-ad301becba80` | unsure | 0.433 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `82108f04-9b5b-498e-b219-12bbb0ac090e` | human | 0.270 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a544b8d2-c84b-4395-a4eb-6413237d21b9` | unsure | 0.550 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `816eeb30-5c9d-4d20-b641-f7bcc36ecc80` | unsure | 0.411 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `fc312878-eb8c-4baa-bc1f-8fbf472e216e` | unsure | 0.414 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `5407cf44-7c79-4197-9205-21672e53981a` | unsure | 0.548 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `29fde15a-6669-4373-a1e4-cb6c28dc2494` | human | 0.167 |  |
| MF04 | malformed | text is only punctuation | 200 | `7ce5655e-7734-4035-a0bb-b88809511ec6` | human | 0.339 |  |
| MF05 | malformed | text is a very long single word | 200 | `c7a11c76-6607-48eb-950a-4029cf92c165` | ai | 0.832 |  |
| MF06 | malformed | text is emoji only | 200 | `1994707d-83e2-429f-a829-ae5f0c000038` | ai | 0.832 |  |
| MF07 | malformed | text is right-to-left script | 200 | `dbe39894-d0b1-4a15-a869-652858434070` | ai | 0.933 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `2b725c3a-3f13-4fa9-b1f8-467f1c6c3a89` | ai | 0.882 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `93905407-5337-4cf1-b3fe-6082dbf356b7` | human | 0.310 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `40e86ee2-ec9f-4762-a55a-bebfad200b21` | human | 0.310 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `94414a55-07ec-48a9-9cc3-72f504743291` | human | 0.310 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5f78502d-5f5a-42cb-8456-75d925e4bbfa` | human | 0.310 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `128c2e7d-22c5-4042-a4d3-9e02c600a7c8` | human | 0.310 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cf40f6de-6511-49e7-ab08-eacf179c2187` | human | 0.310 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2a08555c-e4e9-47d1-b385-b431b917c3ed` | human | 0.310 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9199d1d6-682d-4a1b-ab55-39c58a1a61af` | human | 0.310 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `87e0718e-2a88-4e30-a566-9feb8bc6bc3c` | human | 0.310 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dd970ae9-9f4b-41ac-bc78-318ecb592f14` | human | 0.310 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 1 | 19 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "7def313e-002a-444d-b716-41f0f2dc5b37",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.375,
  "model_score": 0.1635,
  "style_score": 0.5865,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c1630f89-c8d0-4171-a9dd-b8f7338da719",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4683,
  "model_score": 0.5943,
  "style_score": 0.3422,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "10fe12ce-f1dc-4597-95fe-1d047cf09324",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5655,
  "model_score": 0.6662,
  "style_score": 0.4648,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "cc79e267-c26b-4723-89ff-d68254935aed",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5934,
  "model_score": 0.6114,
  "style_score": 0.5753,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "7fe88b0c-b5ec-441b-80d0-e075fe0fc5dd",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3566,
  "model_score": 0.3212,
  "style_score": 0.392,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "00f2d9c5-9bfb-4075-9a8f-c7b1cf9805e9",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4687,
  "model_score": 0.5727,
  "style_score": 0.3646,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "37780f9c-5f94-4f3b-90ab-4e1f03f9b26a",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.6002,
  "model_score": 0.5862,
  "style_score": 0.6143,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "51b5eeff-2d7e-494e-9d58-5bc87c7e200e",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3447,
  "model_score": 0.2452,
  "style_score": 0.4442,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "a97c93aa-0aac-4347-b604-8c2cb0c9e077",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5838,
  "model_score": 0.7042,
  "style_score": 0.4635,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "d05536b9-ca92-4456-92ed-8af3ff514984",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.859,
  "model_score": 0.9792,
  "style_score": 0.7389,
  "label": "This writing shows strong signals commonly associated with AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "61f9cc71-cb42-4154-b428-ba542cfcc222",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5746,
  "model_score": 0.6175,
  "style_score": 0.5316,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "b34497b8-d8c6-4409-b206-8678df8b0ebf",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.676,
  "model_score": 0.7387,
  "style_score": 0.6132,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "40bcc283-3e36-4c55-b2b4-95c68d382394",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6925,
  "model_score": 0.8051,
  "style_score": 0.5799,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "37aa003e-e5ec-4f81-8aee-7c9980afa51d",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6782,
  "model_score": 0.8329,
  "style_score": 0.5235,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "27440753-1b5b-46b0-8055-d0d001111bdb",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.7087,
  "model_score": 0.8005,
  "style_score": 0.617,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "aaf6bf73-f44b-4ab8-8e27-c80afcc1d2cf",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6905,
  "model_score": 0.8814,
  "style_score": 0.4995,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "1c54b71a-b989-4b6c-a221-653013c02b4d",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6867,
  "model_score": 0.8816,
  "style_score": 0.4919,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "495f949d-0ab8-4d4b-b4a0-e25d92bffaf8",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2556,
  "model_score": 0.3223,
  "style_score": 0.189,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "d7b5e1f2-5d1c-4a07-b9b1-ad301becba80",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4327,
  "model_score": 0.4625,
  "style_score": 0.4029,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "82108f04-9b5b-498e-b219-12bbb0ac090e",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2696,
  "model_score": 0.2044,
  "style_score": 0.3348,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "a544b8d2-c84b-4395-a4eb-6413237d21b9",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5498,
  "model_score": 0.5943,
  "style_score": 0.5053,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "816eeb30-5c9d-4d20-b641-f7bcc36ecc80",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4112,
  "model_score": 0.4998,
  "style_score": 0.3226,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "fc312878-eb8c-4baa-bc1f-8fbf472e216e",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4137,
  "model_score": 0.6401,
  "style_score": 0.1873,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "5407cf44-7c79-4197-9205-21672e53981a",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5483,
  "model_score": 0.5583,
  "style_score": 0.5382,
  "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "29fde15a-6669-4373-a1e4-cb6c28dc2494",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.1666,
  "model_score": 0.0,
  "style_score": 0.3333,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "7ce5655e-7734-4035-a0bb-b88809511ec6",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.3389,
  "model_score": 0.0112,
  "style_score": 0.6667,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c7a11c76-6607-48eb-950a-4029cf92c165",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8321,
  "model_score": 0.9976,
  "style_score": 0.6667,
  "label": "This writing shows strong signals commonly associated with AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "1994707d-83e2-429f-a829-ae5f0c000038",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.8318,
  "model_score": 0.9969,
  "style_score": 0.6667,
  "label": "This writing shows strong signals commonly associated with AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "dbe39894-d0b1-4a15-a869-652858434070",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9334,
  "model_score": 0.9064,
  "style_score": 0.9603,
  "label": "This writing shows strong signals commonly associated with AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "2b725c3a-3f13-4fa9-b1f8-467f1c6c3a89",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.8816,
  "model_score": 0.9876,
  "style_score": 0.7756,
  "label": "This writing shows strong signals commonly associated with AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "93905407-5337-4cf1-b3fe-6082dbf356b7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "40e86ee2-ec9f-4762-a55a-bebfad200b21",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "94414a55-07ec-48a9-9cc3-72f504743291",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "5f78502d-5f5a-42cb-8456-75d925e4bbfa",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "128c2e7d-22c5-4042-a4d3-9e02c600a7c8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "cf40f6de-6511-49e7-ab08-eacf179c2187",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "2a08555c-e4e9-47d1-b385-b431b917c3ed",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "9199d1d6-682d-4a1b-ab55-39c58a1a61af",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "87e0718e-2a88-4e30-a566-9feb8bc6bc3c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "dd970ae9-9f4b-41ac-bc78-318ecb592f14",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3098,
  "model_score": 0.0287,
  "style_score": 0.5909,
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
