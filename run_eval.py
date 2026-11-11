#!/usr/bin/env python3

"""
Run all five Provenance Guard criteria three times.

Usage:

    python run_eval.py --label before
    python run_eval.py --label after
"""

import argparse
import datetime as dt
import json
import sys

import config


for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def bodies_for(scenario):
    """
    Convert scenario texts into POST /submit request bodies.
    """

    if scenario.get("bodies"):
        return list(scenario["bodies"])

    return [
        {
            "text": text,
            "creator_id": f"eval_{scenario['criterion']}_{i}"
        }
        for i, text in enumerate(scenario["texts"], 1)
    ]


def describe(body):
    """
    Short readable description for the report.
    """

    if (
        set(body) == {"text", "creator_id"}
        and isinstance(body.get("text"), str)
    ):
        text = body["text"]

        if not text:
            return "(empty text)"

        return text[:70]

    return json.dumps(body)[:120]


def run_normal_scenario(
    requests,
    scenario,
    base_url,
    timeout
):
    """
    Run a normal scenario through POST /submit.
    """

    results = []

    bodies = bodies_for(scenario)

    groups = scenario.get(
        "groups",
        []
    )

    for i, body in enumerate(bodies, 1):

        preview = describe(body)

        try:

            response = requests.post(
                f"{base_url}/submit",
                json=body,
                timeout=timeout
            )

            try:
                payload = response.json()
            except Exception:
                payload = {}

            result = {
                "status": response.status_code,
                "guess": payload.get("guess"),
                "confidence": payload.get("confidence"),
                "model_score": payload.get("model_score"),
                "style_score": payload.get("style_score"),
                "label": payload.get("label"),
                "sent": preview,
            }

            if groups and i <= len(groups):
                result["expected_group"] = groups[i - 1]

            results.append(result)

        except Exception as exc:

            results.append({
                "status": None,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
                "sent": preview
            })

    return results


def run_appeal_scenario(
    requests,
    scenario,
    base_url,
    timeout
):
    """
    Test the complete appeal path.

    1. POST /submit
    2. capture content_id
    3. POST /appeal
    4. read /log
    5. verify appeal entry exists
    """

    results = []

    for i, body in enumerate(
        bodies_for(scenario),
        1
    ):

        preview = describe(body)

        try:

            # ----------------------------
            # Step 1: create submission
            # ----------------------------

            submit_response = requests.post(
                f"{base_url}/submit",
                json=body,
                timeout=timeout
            )

            try:
                submit_payload = (
                    submit_response.json()
                )
            except Exception:
                submit_payload = {}

            content_id = submit_payload.get(
                "content_id"
            )

            if (
                submit_response.status_code != 200
                or not content_id
            ):

                results.append({
                    "submit_status":
                        submit_response.status_code,

                    "content_id":
                        content_id,

                    "appeal_http_status":
                        None,

                    "final_status":
                        None,

                    "appeal_logged":
                        False,

                    "sent":
                        preview,

                    "error":
                        "submission did not create content_id"
                })

                continue

            # ----------------------------
            # Step 2: submit appeal
            # ----------------------------

            appeal_response = requests.post(
                f"{base_url}/appeal",
                json={
                    "content_id": content_id,
                    "reasoning": (
                        f"Evaluation appeal test {i}: "
                        "please review this automated decision."
                    )
                },
                timeout=timeout
            )

            try:
                appeal_payload = (
                    appeal_response.json()
                )
            except Exception:
                appeal_payload = {}

            # ----------------------------
            # Step 3: inspect audit log
            # ----------------------------

            log_response = requests.get(
                f"{base_url}/log?limit=500",
                timeout=timeout
            )

            try:
                log_payload = (
                    log_response.json()
                )
            except Exception:
                log_payload = {}

            entries = log_payload.get(
                "entries",
                []
            )

            appeal_logged = any(
                entry.get("content_id")
                == content_id

                and entry.get("event")
                == "appeal"

                and entry.get("status")
                == "under_review"

                for entry in entries
            )

            results.append({
                "submit_status":
                    submit_response.status_code,

                "content_id":
                    content_id,

                "appeal_http_status":
                    appeal_response.status_code,

                "final_status":
                    appeal_payload.get("status"),

                "appeal_logged":
                    appeal_logged,

                "sent":
                    preview
            })

        except Exception as exc:

            results.append({
                "submit_status":
                    None,

                "content_id":
                    None,

                "appeal_http_status":
                    None,

                "final_status":
                    None,

                "appeal_logged":
                    False,

                "sent":
                    preview,

                "error":
                    f"{type(exc).__name__}: {exc}"
            })

    return results


def print_trial_summary(
    scenario,
    trial_number,
    results
):
    """
    Print a useful short summary to the terminal.
    """

    criterion = scenario.get(
        "criterion"
    )

    # Criterion 4
    if scenario.get("mode") == "appeal":

        values = []

        for result in results:

            if (
                result.get("final_status")
                == "under_review"
                and result.get("appeal_logged")
                is True
            ):
                values.append("PASS")
            else:
                values.append("FAIL")

        print(
            f"  trial {trial_number}: "
            + ", ".join(values)
        )

        return

    # Criterion 5
    if criterion == 5:

        statuses = [
            str(result.get("status"))
            for result in results
        ]

        print(
            f"  trial {trial_number}: "
            + ", ".join(statuses)
        )

        return

    # Other criteria
    guesses = [
        result.get("guess")
        or str(result.get("status"))
        for result in results
    ]

    print(
        f"  trial {trial_number}: "
        + ", ".join(guesses)
    )


def main():

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=(
            argparse.RawDescriptionHelpFormatter
        )
    )

    parser.add_argument(
        "--trials",
        type=int,
        default=3
    )

    parser.add_argument(
        "--label",
        default=""
    )

    parser.add_argument(
        "--url",
        default=DEFAULT_URL
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=90.0
    )

    args = parser.parse_args()

    # ----------------------------
    # Dependencies
    # ----------------------------

    try:
        import requests

    except ImportError:

        print(
            "The requests package is not installed.\n"
            "Run: pip install -r requirements.txt",
            file=sys.stderr
        )

        sys.exit(1)

    try:
        import scenarios

    except ImportError:

        print(
            "No scenarios.py found.",
            file=sys.stderr
        )

        sys.exit(1)

    # ----------------------------
    # Validate scenarios
    # ----------------------------

    problems = scenarios.validate()

    if problems:

        print(
            "scenarios.py has problems:",
            file=sys.stderr
        )

        for problem in problems:
            print(
                f"  - {problem}",
                file=sys.stderr
            )

        sys.exit(1)

    # ----------------------------
    # Check service
    # ----------------------------

    try:

        health_response = requests.get(
            f"{args.url}/health",
            timeout=5
        )

        if not health_response.ok:
            raise RuntimeError(
                f"health returned "
                f"{health_response.status_code}"
            )

    except Exception:

        print(
            f"Nothing answering at {args.url}. "
            "Start it with: python app.py",
            file=sys.stderr
        )

        sys.exit(1)

    if args.trials < 3:

        print(
            f"!! {args.trials} trial(s). "
            "The assignment requires three."
        )

    rows = []

    # ----------------------------
    # Run all five criteria
    # ----------------------------

    for scenario in scenarios.SCENARIOS:

        print(
            f"\n{scenario['name']} "
            f"(criterion "
            f"{scenario.get('criterion')})"
        )

        trials = []

        for trial in range(
            1,
            args.trials + 1
        ):

            if (
                scenario.get("mode")
                == "appeal"
            ):

                results = (
                    run_appeal_scenario(
                        requests,
                        scenario,
                        args.url,
                        args.timeout
                    )
                )

            else:

                results = (
                    run_normal_scenario(
                        requests,
                        scenario,
                        args.url,
                        args.timeout
                    )
                )

            print_trial_summary(
                scenario,
                trial,
                results
            )

            trials.append(
                results
            )

        rows.append({
            "scenario":
                scenario,

            "trials":
                trials
        })

    write_report(
        rows,
        args
    )


def write_report(
    rows,
    args
):

    config.RESULTS_DIR.mkdir(
        exist_ok=True
    )

    stamp = (
        dt.datetime.now()
        .strftime(
            "%Y-%m-%d_%H%M"
        )
    )

    label = (
        f"_{args.label}"
        if args.label
        else ""
    )

    path = (
        config.RESULTS_DIR
        / f"run_{stamp}{label}.md"
    )

    n = args.trials

    headers = " | ".join(
        f"Run {i}"
        for i in range(
            1,
            n + 1
        )
    )

    divider = "|".join(
        ["---"] * n
    )

    lines = [
        (
            f"# Run log"
            f"{' - ' + args.label if args.label else ''}"
        ),
        "",
        "- Produced by: `run_eval.py::main`",
        "- Service: `app.py::submit`",
        "- Scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion",
        "",
        (
            "Fill in the target, run result, and verdict "
            "using criteria.md and the real output below."
        ),
        "",
        (
            f"| Criterion | Target | "
            f"{headers} | Verdict |"
        ),
        (
            f"|---|---|"
            f"{divider}|---|"
        ),
    ]

    for row in rows:

        scenario = row["scenario"]

        number = scenario.get(
            "criterion"
        )

        name = (
            f"{number}. "
            f"{scenario['name']}"
        )

        empty_runs = (
            " | ".join(
                [" "] * n
            )
        )

        lines.append(
            f"| {name} |  | "
            f"{empty_runs} |  |"
        )

    lines += [
        "",
        "---",
        "",
        "## What actually came back",
        "",
    ]

    for row in rows:

        scenario = row[
            "scenario"
        ]

        lines += [
            (
                f"### "
                f"{scenario['name']}"
            ),
            ""
        ]

        for (
            trial_number,
            results
        ) in enumerate(
            row["trials"],
            1
        ):

            lines += [
                (
                    f"**Trial "
                    f"{trial_number}**"
                ),
                "",
                "```json",
                json.dumps(
                    results,
                    indent=2
                ),
                "```",
                ""
            ]

    path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print(
        f"\nWrote "
        f"{path.relative_to(config.ROOT)}"
    )

    print(
        "Commit this file as evidence "
        "that the evaluation was run."
    )


if __name__ == "__main__":
    main()