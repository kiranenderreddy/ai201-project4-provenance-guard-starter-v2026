"""
Unit 8 evaluation scenarios for Provenance Guard.

These scenarios correspond to the five acceptance criteria in criteria.md.
"""

SCENARIOS = [
    # ---------------------------------------------------------
    # Criterion 1: False positives
    # Target:
    # Of 10 clearly human-written samples, at most 1 may receive
    # the high-confidence AI label.
    #
    # NOTE:
    # These are neutral stand-in samples for testing.
    # The original criterion asks for personally written samples.
    # ---------------------------------------------------------
    {
        "name": "false positives",
        "criterion": 1,
        "texts": [
            """I went to the grocery store after work because I forgot to buy milk yesterday. The parking lot was packed, so I parked near the back and walked in the rain.""",

            """My laptop was acting strange this morning. It took a long time to start, and one of the applications froze twice before I restarted the computer.""",

            """I tried making pasta for dinner, but I added too much salt to the sauce. It was still edible, although next time I will taste it before adding more seasoning.""",

            """The meeting started a few minutes late because two people were still joining. We discussed the timeline, assigned several tasks, and agreed to check progress again next week.""",

            """I usually prefer studying early in the morning because it is quieter. Once the day gets busy, I find it harder to focus without checking my phone.""",

            """There was a lot of traffic on the highway today. A drive that normally takes twenty minutes took almost forty-five, and I barely arrived on time.""",

            """I ordered a pair of shoes online last week. They looked good in the pictures, but the size felt slightly tight when they arrived, so I may return them.""",

            """I cleaned my room this afternoon and finally organized the papers on my desk. I also found a receipt that I had been looking for since last month.""",

            """The weather changed suddenly while I was outside. It was sunny when I left home, but about thirty minutes later it started raining and I did not have an umbrella.""",

            """I watched a movie last night that started slowly but became more interesting halfway through. The ending was not what I expected, but overall I enjoyed it."""
        ],
    },

    # ---------------------------------------------------------
    # Criterion 2: Score spread
    #
    # First 3 = clearly AI-style
    # Last 3 = clearly human-style
    #
    # Target:
    # average AI combined score must be at least 0.20 higher
    # than average human combined score.
    # ---------------------------------------------------------
    {
        "name": "score spread",
        "criterion": 2,
        "groups": [
            "ai",
            "ai",
            "ai",
            "human",
            "human",
            "human",
        ],
        "texts": [
            """Artificial intelligence provides organizations with scalable methods for automating repetitive processes. These systems can analyze large quantities of information, identify patterns, and support decision making. When implemented effectively, artificial intelligence can improve efficiency and consistency.""",

            """The implementation of standardized processes enables organizations to optimize operational performance. Furthermore, continuous evaluation supports strategic alignment, improves productivity, and promotes sustainable organizational outcomes.""",

            """Modern technology offers numerous opportunities for organizations to improve efficiency and productivity. By implementing structured systems and data-driven strategies, businesses can optimize workflows, reduce operational challenges, and achieve consistent results.""",

            """I missed the bus this morning and had to wait almost twenty minutes for the next one. My coffee was already cold by then, so the morning was off to a pretty bad start.""",

            """I was looking for my keys for ten minutes before realizing they were in my jacket pocket. I had already checked the kitchen twice, which made it even more annoying.""",

            """I tried a new sandwich place near work yesterday. The food was good, but they forgot my drink, and I did not notice until I was already halfway back to the office."""
        ],
    },

    # ---------------------------------------------------------
    # Criterion 3: Label coverage
    #
    # Target:
    # all three labels reachable with <= 6 inputs.
    # ---------------------------------------------------------
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            # Deliberately repetitive AI-style text
            """The system works well. The system works well. The system works well. The system works well. The system works well. The system works well. The system works well. The system works well.""",

            # Borderline
            """Artificial intelligence provides organizations with methods for analyzing information and supporting decisions. The technology can improve some workflows, although its usefulness depends on the situation and the people using it.""",

            # Human-style
            """Missed the bus again. Great. At 6:17 a.m. I was standing outside with one shoe half untied, coffee leaking through the lid, and my phone at 3% battery. Then the driver actually stopped for me and I nearly dropped the coffee trying to run."""
        ],
    },

    # ---------------------------------------------------------
    # Criterion 4: Appeal path
    #
    # run_eval.py will:
    # submit -> get content_id -> appeal -> inspect audit log.
    #
    # Target:
    # 3/3 become under_review AND create appeal log entry.
    # ---------------------------------------------------------
    {
        "name": "appeal path",
        "criterion": 4,
        "mode": "appeal",
        "texts": [
            """This is the first normal submission used to test the appeal workflow. It contains enough text for the detector to process without being an invalid request.""",

            """This is another valid submission used to verify that a real content identifier can be challenged through the appeal endpoint successfully.""",

            """The final appeal test checks whether the service changes the content status and records the appeal in the audit log correctly."""
        ],
    },

    # ---------------------------------------------------------
    # Criterion 5: Bad input
    #
    # Target:
    # all 3 invalid inputs return controlled 4xx responses.
    # ---------------------------------------------------------
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {
                "text": "",
                "creator_id": "eval_bad_empty"
            },
            {
                "creator_id": "eval_bad_missing"
            },
            {
                "text": "   ",
                "creator_id": "eval_bad_whitespace"
            }
        ],
    },
]


def validate() -> list[str]:
    """
    Validate the scenarios before the evaluation starts.
    """

    problems = []

    for i, scenario in enumerate(SCENARIOS, 1):

        if not scenario.get("name"):
            problems.append(
                f"scenario {i} has no name"
            )

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') "
                f"has both texts and bodies"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict"
                    )

            continue

        if not texts:
            problems.append(
                f"scenario {i} has no texts and no bodies"
            )
            continue

        for j, text in enumerate(texts, 1):

            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty"
                )

            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i}, text {j} still contains placeholder text"
                )

    return problems