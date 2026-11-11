Provenance Guard
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
> Everything in this project fills in the middle.
>
> **The rest of this file is the submission.**
---
<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->
What This Does
A creator sends text and a `creator_id` to `POST /submit`.
The service validates the incoming request.
Signal one in `detector.py` reads the submitted text and produces an AI-detection score.
Signal two in `stylometry.py` measures properties of the writing itself, including sentence-length variation, vocabulary diversity, and punctuation density.
`scoring.py::combine_signals` combines the two signal scores into one overall confidence score.
`scoring.py::score_to_label` maps the combined score to one of three reader-facing labels.
The submission, both signal scores, combined score, label, creator ID, content ID, timestamp, and status are written to `logs/audit.jsonl`.
If the creator disagrees with the result, they can submit an appeal using the content ID. The status changes to `under_review`, and the appeal is recorded in the audit log.
False-positive trace
A false positive happens when a real writer submits their own work but the system gives it a strong AI-generated score. The writer receives a `content_id`, the combined confidence score, and a reader-facing label.
If the writer believes the result is wrong, they can appeal using the `content_id` and explain their reasoning. The appeal changes the submission status to `under_review` and is recorded in the audit log.
This matters when choosing thresholds because a false accusation can negatively affect a legitimate writer. I therefore want the system to be cautious before showing its strongest AI-generated label.
Endpoint contracts
POST /submit
Input
```json
{
  "text": "Text submitted by the creator",
  "creator_id": "creator123"
}
```
Output
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
POST /appeal
Input
```json
{
  "content_id": "unique-content-id",
  "reasoning": "Why the creator believes the result should be reviewed"
}
```
Output
```json
{
  "content_id": "unique-content-id",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```
---
Signals and Scoring
Signal one — the model signal
What it measures:
The model signal in `detector.py` uses a local GPT-2 language model to measure how predictable the submitted text is. It produces a score between 0 and 1, where a higher score means the writing appears more AI-like to this detector.
Why that might differ between human and AI writing:
AI-generated text can contain statistical language patterns, word choices, and sentence structures that are especially predictable to a language model. Some naturally written human text may be less predictable.
What it can't see:
The detector cannot know who actually wrote the text. Human writing can resemble AI-generated writing, and AI-generated text can be edited enough to resemble human writing.
Signal two — the style signal
What it measures:
The style signal in `stylometry.py` measures sentence-length variation, vocabulary diversity, and punctuation density. These measurements are combined into a score from 0 to 1, where a higher score means the text appears more AI-like according to the style rules.
Why that might differ between human and AI writing:
Human and AI writing may differ in how repetitive or varied their sentence lengths, vocabulary, and punctuation patterns are. These features provide a second signal that measures something different from the language-model detector.
What it can't see:
Stylometry cannot determine authorship or understand meaning. A human can intentionally write in a regular or formal style, while AI-generated text can be edited with different sentence lengths, vocabulary, punctuation, or typos to change the score.
The combining rule
The rule:
The model signal and style signal are combined using an equal-weighted average. I chose equal weighting because the two signals measure different properties of the text. When they strongly disagree, the combined result moves toward the uncertain middle instead of allowing either signal alone to make a high-confidence accusation.
The numbers:
Model signal weight = `0.50`
Style signal weight = `0.50`
```text
combined_score =
    (0.50 × model_score)
    +
    (0.50 × style_score)
```
Where it lives: `scoring.py::combine_signals`
A case where my two signals split, and what my rule does with it:
One test produced a model score of `0.3636` and a style score of `0.2062`. The model signal was just outside the high-confidence human range, while the style signal was strongly human-like.
Because I weight both signals equally, the combined score became `0.2849`, which produced the high-confidence human label.
---
Label Variants
Label	Score range	The exact text a reader sees
high-confidence human	0.00–0.35	This writing shows strong signals commonly associated with human-written text.
unsure	>0.35–<0.65	The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.
high-confidence AI	0.65–1.00	This writing shows strong signals commonly associated with AI-generated text.
Why I worded the "unsure" one this way:
The unsure label avoids accusing the writer when the signals do not agree strongly enough. It explains that the system is uncertain rather than claiming the text definitely came from either a person or AI.
Label reachability tests
I deliberately tested examples that reached all three label variants.
High-confidence human
```text
model_score:    0.3636
style_score:    0.2062
combined_score: 0.2849
guess:          human
```
Unsure
```text
model_score:    0.5055
style_score:    0.5631
combined_score: 0.5343
guess:          unsure
```
High-confidence AI
```text
model_score:    0.9872
style_score:    0.7620
combined_score: 0.8746
guess:          ai
```
All three reader-facing labels were therefore reachable during testing.
---
Sample Run
A submission
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
An appeal
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
What the log shows afterwards
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
How I Used AI
Moment 1
What I asked for: I asked for help debugging and implementing the `/submit` endpoint after my first version had an indentation error and initially only returned a hardcoded response.
What came back: AI explained the indentation issue and suggested a route structure that validates the request, creates a unique content ID, calls `detector.model_signal(text)`, and records the decision using `audit.log_decision(...)`.
What I changed: I corrected the route structure, added input validation, connected the real detector signal, generated UUID content IDs, and verified that decisions appeared through `GET /log`.
Moment 2
What I asked for: I asked for help implementing the second stylometry signal and combining it with the model signal.
What came back: AI suggested measuring sentence-length variation, vocabulary diversity, and punctuation density, then combining the resulting style score with the model score using an equal-weighted average.
What I changed: I implemented and tested the three stylometry measures, kept the model and style weights at `0.50` each, connected `scoring.py::combine_signals`, added the three reader-facing labels, and tested inputs until all three labels were reachable.
Moment 3 — Unit 8
What I asked for: I asked for help extending the evaluation runner so the appeal criterion could be tested automatically across three trials.
What came back: AI suggested submitting content first, capturing the returned `content_id`, calling `/appeal`, and then checking `/log` for an appeal entry with status `under_review`.
What I changed: I added the appeal scenario to `scenarios.py` and extended `run_eval.py` so the complete submit → appeal → audit-log path runs three times.
Moment 4 — Unit 8
What I asked for: I asked for help interpreting my score-spread results and identifying possible failure stages.
What came back: AI calculated the AI and human group averages and pointed out that the human group actually scored higher. It suggested checking signal one and the combining rule.
What I changed: I compared that suggestion against the real signal values in the run and used the observed scores in my diagnosis below.
<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->
---
Rate Limiting
My limits: 10 per minute, 200 per day
Why those numbers and not others:
I chose 10 submissions per minute because a normal writer is unlikely to need more than 10 submissions in one minute, while an automated script probing many variations can reach that limit quickly. I chose 200 submissions per day so legitimate repeated use is still possible without allowing unlimited automated testing.
What a caller counts as:
When a valid `creator_id` is provided, requests are counted against that creator. If a usable creator ID is missing, the service falls back to the caller's network address.
The run of status codes when I pushed past it:
```text
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```
5 of 15 submissions were rate limited.
A rate-limit rejection was also written to the audit log:
```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "10 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected"
}
```
A route-level invalid request was also logged:
```json
{
  "creator_id": "bad_input_test",
  "event": "rejected",
  "reason": "invalid_text",
  "status": "rejected"
}
```
---
Attack Run — Before
Baseline attack file: `results/attack_run_2026-11-10_2041.md`
ID	Family	Result	Verdict
EV01	evasion	unsure	BROKE
EV02	evasion	unsure	BROKE
EV03	evasion	unsure	BROKE
EV04	evasion	unsure	BROKE
EV05	evasion	unsure	BROKE
EV06	evasion	unsure	BROKE
EV07	evasion	unsure	BROKE
EV08	evasion	human	BROKE
EV09	evasion	unsure	BROKE
EV10	evasion	ai	HELD
FP01	false_positive	unsure	HELD
FP02	false_positive	ai	BROKE
FP03	false_positive	ai	BROKE
FP04	false_positive	ai	BROKE
FP05	false_positive	ai	BROKE
FP06	false_positive	ai	BROKE
FP07	false_positive	ai	BROKE
FP08	false_positive	human	HELD
PI01	prompt_injection	unsure	HELD
PI02	prompt_injection	human	HELD
PI03	prompt_injection	unsure	HELD
PI04	prompt_injection	unsure	HELD
PI05	prompt_injection	unsure	HELD
PI06	prompt_injection	unsure	HELD
MF01	malformed	400	HELD
MF02	malformed	500 crash	BROKE
MF03	malformed	accepted / human	BROKE
MF04	malformed	accepted / human	BROKE
MF05	malformed	accepted / ai	BROKE
MF06	malformed	accepted / ai	BROKE
MF07	malformed	accepted / ai	BROKE
MF08	malformed	accepted / ai	BROKE
RQ01	malformed request	400	HELD
RQ02	malformed request	400	HELD
RQ03	malformed request	400	HELD
RQ04	malformed request	400	HELD
RQ05	malformed request	400	HELD
RQ06	malformed request	400	HELD
RQ07	malformed request	400	HELD
RQ08	malformed request	400	HELD
RQ09	malformed request	400	HELD
RQ10	malformed request	400	HELD
RQ11	malformed request	400	HELD
RQ12	malformed request	400	HELD
FL01_01	flood_same_creator	200	HELD
FL01_02	flood_same_creator	200	HELD
FL01_03	flood_same_creator	200	HELD
FL01_04	flood_same_creator	200	HELD
FL01_05	flood_same_creator	200	HELD
FL01_06	flood_same_creator	200	HELD
FL01_07	flood_same_creator	200	HELD
FL01_08	flood_same_creator	200	HELD
FL01_09	flood_same_creator	200	HELD
FL01_10	flood_same_creator	200	HELD
FL01_11	flood_same_creator	429	HELD
FL01_12	flood_same_creator	429	HELD
Baseline count: 34 HELD, 22 BROKE.
Ten audit log entries from the run
```json
[
  {
    "combined_score": 0.3447,
    "content_id": "f28ca1b6-1284-4409-bb6b-4fb0231e25d9",
    "creator_id": "attacker_EV08",
    "guess": "human",
    "label": "This writing shows strong signals commonly associated with human-written text.",
    "model_score": 0.2452,
    "status": "decided",
    "style_score": 0.4442,
    "timestamp": "2026-11-11T01:40:49+00:00"
  },
  {
    "combined_score": 0.6925,
    "content_id": "3de7521b-10b2-4531-89a3-a026ad511cf8",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "label": "This writing shows strong signals commonly associated with AI-generated text.",
    "model_score": 0.8051,
    "status": "decided",
    "style_score": 0.5799,
    "timestamp": "2026-11-11T01:40:51+00:00"
  },
  {
    "combined_score": 0.7087,
    "content_id": "656b5c73-fd65-46bf-b18f-ccc552516edc",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "label": "This writing shows strong signals commonly associated with AI-generated text.",
    "model_score": 0.8005,
    "status": "decided",
    "style_score": 0.617,
    "timestamp": "2026-11-11T01:40:52+00:00"
  },
  {
    "combined_score": 0.4137,
    "content_id": "03cf37a0-35f6-4bec-a3fc-a9e22fbacbbd",
    "creator_id": "attacker_PI05",
    "guess": "unsure",
    "label": "The signals are mixed, so we cannot confidently determine whether this writing was produced by a person or by AI.",
    "model_score": 0.6401,
    "status": "decided",
    "style_score": 0.1873,
    "timestamp": "2026-11-11T01:40:54+00:00"
  },
  {
    "creator_id": "attacker_MF01",
    "event": "rejected",
    "reason": "invalid_text",
    "status": "rejected",
    "timestamp": "2026-11-11T01:40:55+00:00"
  },
  {
    "combined_score": 0.1666,
    "content_id": "18131b5f-7833-407c-ba9b-11710c927d9e",
    "creator_id": "attacker_MF03",
    "guess": "human",
    "label": "This writing shows strong signals commonly associated with human-written text.",
    "model_score": 0.0,
    "status": "decided",
    "style_score": 0.3333,
    "timestamp": "2026-11-11T01:40:55+00:00"
  },
  {
    "combined_score": 0.8318,
    "content_id": "c21ba6be-31b6-4225-8919-4d96a7c11d60",
    "creator_id": "attacker_MF06",
    "guess": "ai",
    "label": "This writing shows strong signals commonly associated with AI-generated text.",
    "model_score": 0.9969,
    "status": "decided",
    "style_score": 0.6667,
    "timestamp": "2026-11-11T01:40:57+00:00"
  },
  {
    "combined_score": 0.8816,
    "content_id": "ec72b834-6043-422e-bf91-6d86b914fe29",
    "creator_id": "attacker_MF08",
    "guess": "ai",
    "label": "This writing shows strong signals commonly associated with AI-generated text.",
    "model_score": 0.9876,
    "status": "decided",
    "style_score": 0.7756,
    "timestamp": "2026-11-11T01:40:59+00:00"
  },
  {
    "creator_id": "unknown",
    "event": "rejected",
    "reason": "invalid_json",
    "status": "rejected",
    "timestamp": "2026-11-11T01:40:59+00:00"
  },
  {
    "creator_id": "attacker_flood",
    "event": "rejected",
    "limit": "10 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-11T01:41:01+00:00"
  }
]
```
The single worst outcome
The worst outcome was FP03. The attack set identified it as genuine human writing from a non-native English speaker, but the system labeled it as AI with a combined score of `0.6925`. Signal one was especially high at `0.8051`, while signal two was `0.5799`.
I consider this worse than simply missing AI-generated text because a false positive could wrongly accuse a real writer of using AI.
---
Run Log and Verdicts
Baseline evaluation file: `results/run_2026-11-10_2101_before.md`  
Produced by: `run_eval.py::main`
Criterion	Target	Run 1	Run 2	Run 3	Verdict
1. False positives	At most 1 of 10 human samples labeled AI	1/10	1/10	1/10	MET numerically*
2. Score spread	AI average at least 0.20 higher than human average	-0.054 gap	-0.054 gap	-0.054 gap	MISSED
3. Label coverage	All 3 labels reachable within ≤6 inputs	3/3	3/3	3/3	MET
4. Appeal path	3/3 appeals become `under_review` and are logged	3/3	3/3	3/3	MET
5. Bad input	3/3 invalid requests return controlled 4xx	3/3	3/3	3/3	MET
*The current Criterion 1 run used neutral stand-in samples in `scenarios.py` because of time constraints. The numeric result is recorded honestly, but these samples should be replaced with personally authored human writing before treating the result as conclusive evidence about my own false-positive rate.
Real output from one trial
Criterion 1 — false positives
```json
[
  {"status": 200, "guess": "ai", "confidence": 0.7171, "model_score": 0.7985, "style_score": 0.6358},
  {"status": 200, "guess": "unsure", "confidence": 0.5617, "model_score": 0.7478, "style_score": 0.3757},
  {"status": 200, "guess": "unsure", "confidence": 0.6425, "model_score": 0.6905, "style_score": 0.5945},
  {"status": 200, "guess": "unsure", "confidence": 0.4636, "model_score": 0.3781, "style_score": 0.5491},
  {"status": 200, "guess": "unsure", "confidence": 0.6171, "model_score": 0.6686, "style_score": 0.5657},
  {"status": 200, "guess": "unsure", "confidence": 0.5725, "model_score": 0.6907, "style_score": 0.4542},
  {"status": 200, "guess": "unsure", "confidence": 0.5640, "model_score": 0.7161, "style_score": 0.4120},
  {"status": 200, "guess": "unsure", "confidence": 0.6474, "model_score": 0.6495, "style_score": 0.6453},
  {"status": 200, "guess": "unsure", "confidence": 0.5903, "model_score": 0.7666, "style_score": 0.4140},
  {"status": 200, "guess": "unsure", "confidence": 0.6487, "model_score": 0.7268, "style_score": 0.5707}
]
```
Criterion 2 — score spread
```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.6282, "model_score": 0.6929, "style_score": 0.5636, "expected_group": "ai"},
  {"status": 200, "guess": "unsure", "confidence": 0.4388, "model_score": 0.3367, "style_score": 0.5409, "expected_group": "ai"},
  {"status": 200, "guess": "unsure", "confidence": 0.6040, "model_score": 0.7204, "style_score": 0.4877, "expected_group": "ai"},
  {"status": 200, "guess": "ai", "confidence": 0.6880, "model_score": 0.7352, "style_score": 0.6408, "expected_group": "human"},
  {"status": 200, "guess": "unsure", "confidence": 0.6310, "model_score": 0.7011, "style_score": 0.5609, "expected_group": "human"},
  {"status": 200, "guess": "unsure", "confidence": 0.5141, "model_score": 0.6285, "style_score": 0.3998, "expected_group": "human"}
]
```
AI average combined score:
```text
(0.6282 + 0.4388 + 0.6040) / 3 = 0.5570
```
Human average combined score:
```text
(0.6880 + 0.6310 + 0.5141) / 3 = 0.6110
```
Observed gap:
```text
0.5570 - 0.6110 = -0.0540
```
Required gap:
```text
>= +0.20
```
Criterion 3 — label coverage
```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8839,
    "model_score": 0.9916,
    "style_score": 0.7762
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5750,
    "model_score": 0.5992,
    "style_score": 0.5509
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3072,
    "model_score": 0.3723,
    "style_score": 0.2420
  }
]
```
Criterion 4 — appeal path
```json
[
  {
    "submit_status": 200,
    "appeal_http_status": 200,
    "final_status": "under_review",
    "appeal_logged": true
  },
  {
    "submit_status": 200,
    "appeal_http_status": 200,
    "final_status": "under_review",
    "appeal_logged": true
  },
  {
    "submit_status": 200,
    "appeal_http_status": 200,
    "final_status": "under_review",
    "appeal_logged": true
  }
]
```
Criterion 5 — bad input
```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "   "
  }
]
```
Diagnoses
Criterion 2 — score spread — MISSED
Stage: signal one and the combining rule.
Mechanism: The detector did not separate the deliberately AI-style and human-style samples in the expected direction. The three AI-style texts averaged `0.5570`, while the three human-style texts averaged `0.6110`, producing a gap of `-0.0540` instead of the required `+0.20`.
The largest problem appears in signal one. One AI-style sample received a model score of only `0.3367`, while one human-style sample received `0.7352`. Because the combining rule gives signal one 50% of the final score, those incorrect model scores carried directly into the combined result. The label mapping is not the cause of this criterion miss because this criterion is measured using combined scores before labels are assigned.
Evasion attacks EV01–EV09 — BROKE
Stages: signal one, signal two, and the combining rule.
Mechanism: The evasion attacks changed surface properties that the two signals rely on. Typos, broken sentence structure, quotations, unusual vocabulary, punctuation changes, short text, and human editing reduced one or both signal scores enough to move the final result into the `unsure` or `human` ranges.
Examples:
EV01 produced model `0.1635`, style `0.5865`, combined `0.3750`.
EV05 produced model `0.3212`, style `0.3920`, combined `0.3566`.
EV08 produced model `0.2452`, style `0.4442`, combined `0.3447`, which was labeled human.
EV09 still had a relatively high model score of `0.7042`, but style fell to `0.4635`; equal weighting pulled the combined result to `0.5838`, which was unsure.
The system therefore does not have a signal that is robust to edited or intentionally distorted AI text.
False positives FP02–FP07 — BROKE
Stages: signal one and the combining rule.
Mechanism: Formal, careful, technical, templated, and deliberately repetitive human writing produced very high model scores. Signal one gave FP02–FP07 model scores from approximately `0.7387` to `0.8816`. Signal two was mostly moderate rather than strongly human.
With equal 50/50 weighting, those model scores pushed the combined result above the `0.65` AI threshold. This created high-confidence AI labels for genuine human writing.
This is particularly harmful because the system's strongest label becomes a false accusation rather than merely an uncertain result.
MF02 — one-character input — BROKE
Stages: route and signal one.
Mechanism: The route validated that `text` was a non-empty string but did not validate that it contained enough usable text for the detector. Signal one then raised:
```text
ValueError: Text is too short to score — a few sentences at least.
```
The exception was not converted to a controlled 4xx response, so Flask returned `500`.
MF03–MF06 and MF08 — malformed content accepted — BROKE
Stage: route validation.
Mechanism: The route checks that `text` is a non-empty string, but it does not validate whether the string contains meaningful language or whether its length is reasonable.
As a result:
control characters were accepted,
punctuation-only text was accepted,
one extremely long word was accepted,
emoji-only text was accepted,
60,000 characters were accepted.
Those inputs then reached the detector and received misleading human/AI labels instead of being rejected as unsupported input.
MF07 — right-to-left script — BROKE
Stages: route, signal one, and signal two.
Mechanism: The route accepts the text without checking whether the detector and stylometry signal support that script. Both signals then produced very high AI-like scores, resulting in a combined score of `0.9334`.
The system therefore treated unsupported-language behavior as evidence of AI authorship.
---
The Improvement
What I changed:
I made one change in `config.py`.
Before:
```python
AI_THRESHOLD = 0.65
```
After:
```python
AI_THRESHOLD = 0.72
```
I did not change signal one, signal two, the 0.50/0.50 combining weights, the human threshold, or the input-validation rules.
Which diagnosis pointed at it:
The baseline attack run showed a serious false-positive problem. FP02 through FP07 were genuine human-writing examples, but all six received the high-confidence AI label.
Their combined scores were approximately between `0.676` and `0.709`. Because my original AI threshold was `0.65`, those human-writing examples crossed directly into the strongest AI label.
I therefore raised the AI threshold from `0.65` to `0.72`. This widens the unsure range so the system requires stronger evidence before making a high-confidence AI claim.
The tradeoff is intentional: some AI-generated writing between `0.65` and `0.72` may now receive `unsure`, but reducing false accusations against real writers is more important for this system.
Attack Run — After
Result file:
`results/attack_run_2026-11-10_2111_after.md`
ID	Family	Result	Verdict
EV01	evasion	unsure	BROKE
EV02	evasion	unsure	BROKE
EV03	evasion	unsure	BROKE
EV04	evasion	unsure	BROKE
EV05	evasion	unsure	BROKE
EV06	evasion	unsure	BROKE
EV07	evasion	unsure	BROKE
EV08	evasion	human	BROKE
EV09	evasion	unsure	BROKE
EV10	evasion	ai	HELD
FP01	false_positive	unsure	HELD
FP02	false_positive	unsure	HELD
FP03	false_positive	unsure	HELD
FP04	false_positive	unsure	HELD
FP05	false_positive	unsure	HELD
FP06	false_positive	unsure	HELD
FP07	false_positive	unsure	HELD
FP08	false_positive	human	HELD
PI01	prompt_injection	unsure	HELD
PI02	prompt_injection	human	HELD
PI03	prompt_injection	unsure	HELD
PI04	prompt_injection	unsure	HELD
PI05	prompt_injection	unsure	HELD
PI06	prompt_injection	unsure	HELD
MF01	malformed	400	HELD
MF02	malformed	500 crash	BROKE
MF03	malformed	accepted / human	BROKE
MF04	malformed	accepted / human	BROKE
MF05	malformed	accepted / ai	BROKE
MF06	malformed	accepted / ai	BROKE
MF07	malformed	accepted / ai	BROKE
MF08	malformed	accepted / ai	BROKE
RQ01	malformed request	400	HELD
RQ02	malformed request	400	HELD
RQ03	malformed request	400	HELD
RQ04	malformed request	400	HELD
RQ05	malformed request	400	HELD
RQ06	malformed request	400	HELD
RQ07	malformed request	400	HELD
RQ08	malformed request	400	HELD
RQ09	malformed request	400	HELD
RQ10	malformed request	400	HELD
RQ11	malformed request	400	HELD
RQ12	malformed request	400	HELD
FL01_01	flood_same_creator	200	HELD
FL01_02	flood_same_creator	200	HELD
FL01_03	flood_same_creator	200	HELD
FL01_04	flood_same_creator	200	HELD
FL01_05	flood_same_creator	200	HELD
FL01_06	flood_same_creator	200	HELD
FL01_07	flood_same_creator	200	HELD
FL01_08	flood_same_creator	200	HELD
FL01_09	flood_same_creator	200	HELD
FL01_10	flood_same_creator	200	HELD
FL01_11	flood_same_creator	429	HELD
FL01_12	flood_same_creator	429	HELD
Before: 34 HELD, 22 BROKE  
After: 40 HELD, 16 BROKE
The improvement fixed six staff false-positive attacks: FP02, FP03, FP04, FP05, FP06, and FP07 all changed from the high-confidence `ai` label to `unsure`.
The strong AI case EV10 still remained `ai`, so increasing the threshold did not make every AI-like case disappear into the unsure range.
Acceptance Criteria — After
Result file:
`results/run_2026-11-10_2112_after.md`
Criterion	Target	Run 1	Run 2	Run 3	Verdict
1. False positives	At most 1 of 10 human samples labeled AI	0/10	0/10	0/10	MET
2. Score spread	AI average at least 0.20 higher than human average	-0.054 gap	-0.054 gap	-0.054 gap	MISSED
3. Label coverage	All 3 labels reachable within ≤6 inputs	3/3	3/3	3/3	MET
4. Appeal path	3/3 appeals become `under_review` and are logged	3/3	3/3	3/3	MET
5. Bad input	3/3 invalid requests return controlled 4xx	3/3	3/3	3/3	MET
Did it help, and how do I know:
Yes.
Before the threshold change, six staff false-positive cases, FP02 through FP07, received the high-confidence AI label. After increasing the AI threshold to `0.72`, all six moved into the `unsure` range.
My false-positive evaluation also improved from `1/10` high-confidence AI labels to `0/10`.
The total staff attack result improved from `34 HELD / 22 BROKE` to `40 HELD / 16 BROKE`.
Criterion 3 still reached all three labels, Criterion 4 still passed every appeal test, and Criterion 5 still returned controlled `400` responses for all three invalid inputs.
Criterion 2 did not improve. That is expected because changing the AI threshold only changes the final label mapping. It does not change `model_score`, `style_score`, or `combined_score`.
The AI group therefore still averaged approximately `0.557`, while the human group averaged approximately `0.611`, leaving the score-spread gap at approximately `-0.054`.
The improvement therefore helped the false-positive safety problem, but it did not repair the underlying score separation problem.
---
What's Still Broken
Evasion attacks EV01–EV09
EV01 through EV09 still evade the strongest AI label.
These attacks manipulate properties that my signals depend on, including typos, sentence structure, quotations, unusual vocabulary, punctuation, text length, and human editing.
A future improvement would require a signal that is more robust to paraphrasing and deliberate editing rather than depending mainly on language-model predictability and simple stylometric measurements.
I stopped here because Unit 8 asks for one measured improvement. Changing the detector or stylometry implementation would be a second improvement.
MF02 — one-character input
MF02 still causes a `500` error.
The route checks whether `text` is present and non-empty, but a single character passes that validation. Signal one then attempts to score it and raises:
```text
ValueError: Text is too short to score — a few sentences at least.
```
A future fix would add minimum usable-text validation before either signal runs and return a controlled `400` response instead of allowing the detector exception to become a server error.
I did not add that fix because it would be another improvement beyond the one threshold change measured in this unit.
MF03–MF06 and MF08 — malformed content accepted
Control-character text, punctuation-only text, a very long single word, emoji-only text, and extremely large text are still accepted because they are technically non-empty strings.
A future version should add route-level validation for meaningful text content, reasonable length limits, and supported input before calling the detector.
MF07 — unsupported/right-to-left script
The right-to-left-script attack is still accepted and receives a very high AI score.
The system currently has no language-support check, so unsupported-language behavior can incorrectly be interpreted as evidence that text was AI-generated.
A production version should identify whether the submitted language/script is supported before running the authorship detector.
Criterion 2 — Score spread
Criterion 2 remains MISSED after the improvement.
The AI samples average approximately `0.557`, while the human samples average approximately `0.611`.
The observed gap is:
```text
0.557 - 0.611 = -0.054
```
instead of the required:
```text
>= +0.20
```
The threshold improvement cannot change this because the criterion is based on the combined score before label mapping.
Fixing this problem would require changing signal one, signal two, or the combining rule. That would be a separate improvement, so I stopped after the single measured threshold change.
What I would fix next
If I continued the project, my next change would be route-level input validation.
I would reject:
text that is too short for the detector,
punctuation-only or control-character input,
emoji-only input,
extremely large input,
input without enough normal words or sentences,
unsupported languages/scripts when the detector cannot score them reliably.
After that, I would separately evaluate the model signal and stylometry signal on a larger labeled set before changing their weights.
The trade I'd make if this ran for real:
If this system were used for real people, I would continue to favor fewer false accusations even if that allows more AI-generated text to receive an `unsure` result or pass through.
That choice lowers detection recall, so the platform accepts the cost of missing some AI-generated writing rather than forcing legitimate writers to bear the more serious cost of being incorrectly accused.
---
Submission Checklist
Unit 7
[x] `criteria.md` has five numbered criteria, each naming a target
[x] Each criterion has a reason underneath
[x] `POST /submit` returns `content_id`, `guess`, `confidence`, `label`, `model_score`, and `style_score`
[x] Two signals measure different things, each with a named blind spot
[x] Three label variants are reachable
[x] `POST /appeal` changes status and writes to the log
[x] Signals and Scoring names `scoring.py::combine_signals`
[x] Sample Run includes a submission and an appeal
[x] At least four Unit 7 commits
Unit 8
[x] Rate limiting on `/submit`, with limits justified
[x] Flood run showing `429`
[x] Audit log records decisions and rejections
[x] Staff attack set run in full
[x] Ten audit log entries pasted as text
[x] Five criteria run across three trials
[x] Baseline diagnoses written for the criterion miss and broken attack patterns
[x] One improvement implemented and measured
[x] Attack Run — After added
[x] What's Still Broken updated from the after-run
[ ] At least four new Unit 8 commits
[ ] Same repository URL submitted
---
📖 How to run this project: RUNNING.md