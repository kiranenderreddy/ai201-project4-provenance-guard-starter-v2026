# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.**

---

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

1. A creator sends text and a `creator_id` to `POST /submit`.
2. The service validates the incoming request.
3. Signal one in `detector.py` reads the submitted text and produces an AI-detection score.
4. Signal two in `stylometry.py` measures properties of the writing itself, including sentence-length variation, vocabulary diversity, and punctuation density.
5. `scoring.py::combine_signals` combines the two signal scores into one overall confidence score.
6. `scoring.py::score_to_label` maps the combined score to one of three reader-facing labels.
7. The submission, both signal scores, combined score, label, creator ID, content ID, timestamp, and status are written to `logs/audit.jsonl`.
8. If the creator disagrees with the result, they can submit an appeal using the content ID. The status changes to `under_review`, and the appeal is recorded in the audit log.

### False-positive trace

A false positive happens when a real writer submits their own work but the system gives it a strong AI-generated score. The writer receives a `content_id`, the combined confidence score, and a reader-facing label.

If the writer believes the result is wrong, they can appeal using the `content_id` and explain their reasoning. The appeal changes the submission status to `under_review` and is recorded in the audit log.

This matters when choosing thresholds because a false accusation can negatively affect a legitimate writer. I therefore want the system to be cautious before showing its strongest AI-generated label.

### Endpoint contracts

#### POST /submit

**Input**

```json
{
  "text": "Text submitted by the creator",
  "creator_id": "creator123"
}
```

**Output**

```json
{
  "content_id": "unique-content-id",
  "guess": "human_or_unsure_or_ai",
  "confidence": 0.0,
  "label": "reader-facing label",
  "model_score": 0.0,
  "style_score": 0.0,
  "combined_score": 0.0,
  "status": "decided"
}
```

#### POST /appeal

**Input**

```json
{
  "content_id": "unique-content-id",
  "reasoning": "Why the creator believes the result should be reviewed"
}
```

**Output**

```json
{
  "content_id": "unique-content-id",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:**

The model signal in `detector.py` uses a local GPT-2 language model to measure how predictable the submitted text is. It produces a score between 0 and 1, where a higher score means the writing appears more AI-like to this detector.

**Why that might differ between human and AI writing:**

AI-generated text can contain statistical language patterns, word choices, and sentence structures that are especially predictable to a language model. Some naturally written human text may be less predictable.

**What it can't see:**

The detector cannot know who actually wrote the text. Human writing can resemble AI-generated writing, and AI-generated text can be edited enough to resemble human writing.

### Signal two — the style signal

**What it measures:**

The style signal in `stylometry.py` measures sentence-length variation, vocabulary diversity, and punctuation density. These measurements are combined into a score from 0 to 1, where a higher score means the text appears more AI-like according to the style rules.

**Why that might differ between human and AI writing:**

Human and AI writing may differ in how repetitive or varied their sentence lengths, vocabulary, and punctuation patterns are. These features provide a second signal that measures something different from the language-model detector.

**What it can't see:**

Stylometry cannot determine authorship or understand meaning. A human can intentionally write in a regular or formal style, while AI-generated text can be edited with different sentence lengths, vocabulary, punctuation, or typos to change the score.

### The combining rule

**The rule:**

The model signal and style signal are combined using an equal-weighted average. I chose equal weighting because the two signals measure different properties of the text. When they strongly disagree, the combined result moves toward the uncertain middle instead of allowing either signal alone to make a high-confidence accusation.

**The numbers:**

- Model signal weight = `0.50`
- Style signal weight = `0.50`

The calculation is:

```text
combined_score =
    (0.50 × model_score)
    +
    (0.50 × style_score)
```

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

One test produced a model score of `0.3636` and a style score of `0.2062`. The model signal was just outside the high-confidence human range, while the style signal was strongly human-like.

Because I weight both signals equally, the combined score became `0.2849`, which produced the high-confidence human label.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | This writing shows strong signals commonly associated with human-written text. |
| unsure | 0.35 – 0.65 | The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI. |
| high-confidence AI | 0.65 – 1.00 | This writing shows strong signals commonly associated with AI-generated text. |

**Why I worded the "unsure" one this way:**

The unsure label avoids accusing the writer when the signals do not agree strongly enough. It explains that the system is uncertain rather than claiming the text definitely came from either a person or AI.

### Label reachability tests

I deliberately tested examples that reached all three label variants.

**High-confidence human**

```text
model_score:    0.3636
style_score:    0.2062
combined_score: 0.2849
guess:          human
```

**Unsure**

```text
model_score:    0.5055
style_score:    0.5631
combined_score: 0.5343
guess:          unsure
```

**High-confidence AI**

```text
model_score:    0.9872
style_score:    0.7620
combined_score: 0.8746
guess:          ai
```

All three reader-facing labels were therefore reachable during testing.

---

## Sample Run

### A submission

```bash
curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{\"text\": \"Missed the bus again. Great. At 6:17 a.m. I was standing outside with one shoe half untied, coffee leaking through the lid, and my phone at 3% battery; somehow that felt like a summary of the whole morning. Then the driver actually stopped for me! I laughed, dropped a receipt, picked up the wrong one, and spent the ride wondering why I had written milk, batteries, coriander, and 27 on the back of it. Weird day.\", \"creator_id\": \"kiran\"}'
```

Response:

```json
{
  "combined_score": 0.2849,
  "confidence": 0.2849,
  "content_id": "97bdfa38-15a1-432e-8359-8cfa5216283d",
  "guess": "human",
  "label": "This writing shows strong signals commonly associated with human-written text.",
  "model_score": 0.3636,
  "status": "decided",
  "style_score": 0.2062
}
```

### An appeal

```bash
curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{\"content_id\": \"97bdfa38-15a1-432e-8359-8cfa5216283d\", \"reasoning\": \"I would like this automated decision reviewed because detector results can be uncertain.\"}'
```

Response:

```json
{
  "content_id": "97bdfa38-15a1-432e-8359-8cfa5216283d",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

### What the log shows afterwards

```bash
curl.exe "http://127.0.0.1:5000/log?limit=3"
```

Response:

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.4779,
      "content_id": "4eb95430-7d5b-4f9d-82cd-8c2c7dff6072",
      "creator_id": "kiran",
      "guess": "unsure",
      "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
      "model_score": 0.4692,
      "status": "decided",
      "style_score": 0.4866,
      "timestamp": "2026-11-04T01:27:25+00:00"
    },
    {
      "combined_score": 0.2849,
      "content_id": "97bdfa38-15a1-432e-8359-8cfa5216283d",
      "creator_id": "kiran",
      "guess": "human",
      "label": "This writing shows strong signals commonly associated with human-written text.",
      "model_score": 0.3636,
      "status": "decided",
      "style_score": 0.2062,
      "timestamp": "2026-11-04T01:28:21+00:00"
    },
    {
      "content_id": "97bdfa38-15a1-432e-8359-8cfa5216283d",
      "creator_id": "kiran",
      "event": "appeal",
      "reasoning": "I would like this automated decision reviewed because detector results can be uncertain.",
      "status": "under_review",
      "timestamp": "2026-11-04T01:30:16+00:00"
    }
  ]
}
```

---

## How I Used AI

### Moment 1

- **What I asked for:** I asked for help debugging and implementing the `/submit` endpoint after my first version had an indentation error and initially only returned a hardcoded response.
- **What came back:** AI explained the indentation issue and suggested a route structure that validates the request, creates a unique content ID, calls `detector.model_signal(text)`, and records the decision using `audit.log_decision(...)`.
- **What I changed:** I corrected the route structure, added input validation, connected the real detector signal, generated UUID content IDs, and verified that decisions appeared through `GET /log`.

### Moment 2

- **What I asked for:** I asked for help implementing the second stylometry signal and combining it with the model signal.
- **What came back:** AI suggested measuring sentence-length variation, vocabulary diversity, and punctuation density, then combining the resulting style score with the model score using an equal-weighted average.
- **What I changed:** I implemented and tested the three stylometry measures, kept the model and style weights at `0.50` each, connected `scoring.py::combine_signals`, added the three reader-facing labels, and tested inputs until all three labels were reachable.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**

I chose 10 submissions per minute because a normal writer is unlikely to need more than 10 submissions in one minute, while an automated script probing many variations can reach that limit quickly. I chose 200 submissions per day so legitimate repeated use is still possible without allowing unlimited automated testing.

**What a caller counts as:**

When a valid `creator_id` is provided, requests are counted against that creator. If a usable creator ID is missing, the service falls back to the caller's network address.

**The run of status codes when I pushed past it:**

```text
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429

```

---

## Attack Run — Before

<!--
Every attack with its outcome and a held-or-broke mark.
`run_attacks.py --label before` produces the table.
-->

**Ten audit log entries from the run**

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer whose work got caught by it:

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. | | | | | |
| 2. | | | | | |
| 3. | | | | | |
| 4. | | | | | |
| 5. | | | | | |

**Real output from one trial**, pasted as text, naming the file and function that produced it:

```json

```

**Diagnoses**

<!--
For each miss AND each broken attack: the stage and the mechanism.

Your service has five stages:
1. the route
2. signal one
3. signal two
4. the combining rule
5. the label mapping

Not a diagnosis:
"The evasion attacks got through."

A diagnosis:
"Four evasion inputs got through. All four had typos added to
AI-generated text. My second signal measures word variety, and typos
raise word variety — so it read them as more human. My combining rule
weights that signal at 0.6, so it dragged the whole score down."

Look for a pattern. Five failures on one signal is one problem, not five.
-->

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

**Did it help, and how do I know:**

<!--
Widening the unsure band usually fixes one problem and creates another.
Reporting that trade honestly is worth full credit.
-->

---

## What's Still Broken

<!--
For each attack still getting through and each criterion still missed:
what you'd do, and why you stopped.
-->

**The trade I'd make if this ran for real:**

<!--
Two sentences. Fewer wrong accusations means more AI text getting
through. Say which way you'd go and WHO PAYS FOR IT.
-->

<!-- ═════════════════════════════════════════════════════════════════════

SUBMISSION CHECKLIST — unit 7

[ ] criteria.md has five numbered criteria, each naming a target
[ ] Each has a reason underneath
[ ] POST /submit returns content_id, guess, confidence, label,
    model_score and style_score
[ ] Two signals that measure DIFFERENT things, each with a named blind spot
[ ] Three label variants, all reachable, written out in full
[ ] POST /appeal changes status and writes to the log
[ ] Signals and Scoring names scoring.py::combine_signals
[ ] Sample Run: a submission AND an appeal, as pasted text
[ ] At least four new commits
[ ] Repository URL submitted — WRITE IT DOWN

SUBMISSION CHECKLIST — unit 8

[ ] Rate limiting on /submit, with your numbers justified
[ ] The pasted run of status codes showing 429
[ ] Audit log with all nine fields, recording rejections too
[ ] The attack set run IN FULL, every input with an outcome
[ ] Ten audit log entries pasted as text
[ ] Five criteria across three trials
[ ] A diagnosis for every miss and every broken attack — stage AND mechanism
[ ] One improvement, with Attack Run — After
[ ] What's Still Broken, including the production trade
[ ] At least four new commits
[ ] The SAME repository URL as last unit

Do not delete and recreate this repository.

═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**