"""
Signal two: the style signal.

This signal measures the shape of the writing rather than its meaning.

It uses:
1. sentence-length variation
2. vocabulary diversity
3. punctuation density

The final style signal is between 0 and 1.
Higher means more AI-like.
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split text into sentences."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split text into lowercase words with punctuation removed."""
    return re.findall(r"[a-z0-9']+", text.lower())


def sentence_length_spread(text: str) -> float:
    """
    Measure how much sentence lengths vary.

    Returns a normalized value from 0 to 1.
    Higher means sentence lengths vary more.
    """
    sentence_list = sentences(text)

    lengths = [
        len(words(sentence))
        for sentence in sentence_list
        if words(sentence)
    ]

    if len(lengths) < 2:
        return 0.0

    mean_length = statistics.mean(lengths)

    if mean_length == 0:
        return 0.0

    spread = statistics.stdev(lengths) / mean_length

    return min(spread, 1.0)


def type_token_ratio(text: str) -> float:
    """
    Measure vocabulary diversity.

    Unique words / total words.

    Higher means more varied vocabulary.
    """
    token_list = words(text)

    if not token_list:
        return 0.0

    unique_words = len(set(token_list))
    total_words = len(token_list)

    return unique_words / total_words


def punctuation_density(text: str) -> float:
    """
    Measure how much punctuation appears relative to text length.

    Returns punctuation characters / total characters.
    """
    if not text:
        return 0.0

    punctuation = re.findall(r"[^\w\s]", text)

    return len(punctuation) / len(text)


def style_signal(text: str) -> float:
    """
    Combine the three style measurements into one 0-1 score.

    Higher means more AI-like.

    Low sentence-length variation is treated as more AI-like.
    Low vocabulary diversity is treated as more AI-like.
    Low punctuation density is treated as more AI-like.
    """

    spread = sentence_length_spread(text)
    vocabulary = type_token_ratio(text)
    punctuation = punctuation_density(text)

    # Low sentence variation looks more AI-like.
    spread_ai = 1.0 - spread

    # Lower vocabulary diversity looks more AI-like.
    vocabulary_ai = 1.0 - vocabulary

    # Scale punctuation density.
    # Around 8% punctuation or higher is treated as strongly varied.
    punctuation_scaled = min(punctuation / 0.08, 1.0)
    punctuation_ai = 1.0 - punctuation_scaled

    score = (
        spread_ai
        + vocabulary_ai
        + punctuation_ai
    ) / 3.0

    return round(max(0.0, min(score, 1.0)), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")

    print(
        f"sentence_length_spread   "
        f"{sentence_length_spread(text):.4f}"
    )

    print(
        f"type_token_ratio         "
        f"{type_token_ratio(text):.4f}"
    )

    print(
        f"punctuation_density      "
        f"{punctuation_density(text):.4f}"
    )

    print(
        f"style_signal             "
        f"{style_signal(text):.4f}   "
        "(higher = more likely AI)"
    )