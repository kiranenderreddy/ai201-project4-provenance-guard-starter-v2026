# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives

Of 10 clearly human-written samples, at most 1 may receive the high-confidence AI label.

**Why this target:**

A false accusation is more harmful to a real writer than allowing some AI-generated text to pass through. I chose at most 1 false positive in 10 because I want the strongest AI label to be used cautiously.

---

## 2. Score spread

The average combined score for clearly AI-generated text should be at least 0.20 higher than the average combined score for clearly human-written text.

**Why this target:**

I chose a 0.20 gap because I want clearly AI and clearly human writing to have a noticeable separation rather than receiving almost identical scores. A smaller gap would make the final labels less meaningful.

---

## 3. Label coverage

All three reader-facing labels must be reachable using no more than 6 deliberately chosen test inputs.

**Why this target:**

Each label represents a different level of confidence, so every label should actually be reachable. Six inputs gives me enough room to deliberately test examples near each score range without making the test unnecessarily large.

---

## 4. Appeal path

In 3 out of 3 valid appeal tests, submitting an appeal must change the content status to `under_review` and create an audit-log entry.

**Why this target:**

The appeal path is deterministic system behavior rather than a probabilistic model prediction. For a valid content ID, I expect the appeal process and audit logging to work every time.

---

## 5. Bad input

In 3 out of 3 invalid-input tests, requests with missing or empty `text` must return a controlled 4xx response instead of crashing the service.

**Why this target:**

Invalid requests should fail safely and predictably. I chose 3 out of 3 because input validation is deterministic and should not sometimes produce an internal server error.
---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
