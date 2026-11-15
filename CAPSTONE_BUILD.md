# Capstone Build Check

Shape B failure-hardening extension is connected to `POST /submit`.

Development smoke checks confirmed:

- normal supported text still reaches the detector,
- one-character text returns a controlled 400 instead of crashing,
- punctuation-only input is rejected,
- emoji-only input is rejected.

Formal capstone acceptance testing has not started yet.