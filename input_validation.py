"""
Capstone input-hardening rules for Provenance Guard.

This module validates whether submitted text is suitable for the
existing detector before the detector or stylometry signal sees it.
"""

import re
import unicodedata


MIN_WORDS = 8
MAX_TEXT_CHARS = 20_000


def validate_text_for_scoring(text):
    """
    Return:
        (True, None, None)
    when text is suitable for scoring.

    Otherwise return:
        (False, error_code, message)
    """

    if not isinstance(text, str) or not text.strip():
        return (
            False,
            "invalid_text",
            "text is required and cannot be empty.",
        )

    stripped = text.strip()

    # Prevent extremely large requests from reaching the model.
    if len(stripped) > MAX_TEXT_CHARS:
        return (
            False,
            "text_too_long",
            f"text cannot exceed {MAX_TEXT_CHARS} characters.",
        )

    # Reject hidden/control characters except normal whitespace.
    for char in stripped:
        category = unicodedata.category(char)

        if category.startswith("C") and char not in "\n\r\t":
            return (
                False,
                "control_characters",
                "text contains unsupported control characters.",
            )

    # Require actual alphabetic language content.
    alphabetic_count = sum(
        1 for char in stripped if char.isalpha()
    )

    if alphabetic_count < 10:
        return (
            False,
            "non_semantic_text",
            "text must contain enough written language to be scored.",
        )

    # The current detector is intended for English/Latin-script text.
    latin_letters = [
        char
        for char in stripped
        if char.isalpha()
        and "LATIN" in unicodedata.name(char, "")
    ]

    non_latin_letters = [
        char
        for char in stripped
        if char.isalpha()
        and "LATIN" not in unicodedata.name(char, "")
    ]

    if not latin_letters:
        return (
            False,
            "unsupported_script",
            "text must contain supported Latin-script writing.",
        )

    if non_latin_letters:
        return (
            False,
            "unsupported_script",
            "text contains unsupported non-Latin script characters.",
        )

    # Reject one-character inputs, giant single words, and other
    # inputs too short to produce a meaningful detector score.
    words = re.findall(
        r"[^\W\d_]+(?:['’-][^\W\d_]+)*",
        stripped,
        flags=re.UNICODE,
    )

    if len(words) < MIN_WORDS:
        return (
            False,
            "text_too_short",
            f"text must contain at least {MIN_WORDS} words to be scored.",
        )

    return True, None, None