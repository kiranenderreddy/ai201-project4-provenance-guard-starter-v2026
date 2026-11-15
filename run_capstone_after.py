import json
from datetime import datetime, timezone
from pathlib import Path

import requests


BASE_URL = "http://127.0.0.1:5000"
LOG_PATH = Path("logs") / "capstone_runs.jsonl"
RESULTS_DIR = Path("results")

REQUIRED_OUTPUT_FIELDS = {
    "content_id",
    "guess",
    "confidence",
    "label",
    "model_score",
    "style_score",
    "combined_score",
    "status",
}

REQUIRED_LOG_FIELDS = {
    "timestamp",
    "input",
    "output",
    "status_code",
    "duration_ms",
}


def submit(text, creator_id):
    try:
        response = requests.post(
            f"{BASE_URL}/submit",
            json={
                "text": text,
                "creator_id": creator_id,
            },
            timeout=120,
        )

        try:
            body = response.json()
        except ValueError:
            body = {"raw": response.text}

        return {
            "status_code": response.status_code,
            "body": body,
        }

    except Exception as exc:
        return {
            "status_code": None,
            "body": {
                "error": type(exc).__name__,
                "message": str(exc),
            },
        }


def read_capstone_log():
    if not LOG_PATH.exists():
        return []

    records = []

    with LOG_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    return records


def criterion_1(trial):
    cases = [
        "a",
        "hi",
        "abcde",
        "12345",
        "short",
    ]

    outputs = []

    for index, text in enumerate(cases, start=1):
        creator_id = f"cap_c1_t{trial}_{index}"

        result = submit(text, creator_id)

        outputs.append({
            "input": text,
            "creator_id": creator_id,
            **result,
        })

    passed = sum(
        1
        for result in outputs
        if result["status_code"] == 400
    )

    return {
        "passed": passed,
        "total": 5,
        "result": f"{passed}/5",
        "details": outputs,
    }


def criterion_2(trial):
    cases = [
        "!!! ??? ...",
        "---;;;:::",
        "ðŸ˜€ðŸ˜€ðŸ˜€ðŸ˜€ðŸ˜€",
        "ðŸš€ðŸ”¥ðŸ’¡ðŸŽ‰",
        "This sentence contains a control\x00character and must be rejected.",
        "This sentence contains another control\x01character and must be rejected.",
    ]

    outputs = []

    for index, text in enumerate(cases, start=1):
        creator_id = f"cap_c2_t{trial}_{index}"

        result = submit(text, creator_id)

        outputs.append({
            "input": repr(text),
            "creator_id": creator_id,
            **result,
        })

    passed = sum(
        1
        for result in outputs
        if result["status_code"] == 400
    )

    return {
        "passed": passed,
        "total": 6,
        "result": f"{passed}/6",
        "details": outputs,
    }


def criterion_3(trial):
    oversized_1 = (
        "This is valid text for an oversized request. "
        * 600
    )

    oversized_2 = (
        "Another ordinary sentence is repeated to exceed the limit. "
        * 500
    )

    cases = [
        {
            "name": "oversized_1",
            "text": oversized_1,
        },
        {
            "name": "oversized_2",
            "text": oversized_2,
        },
        {
            "name": "arabic_script",
            "text": "Ù‡Ø°Ø§ Ù†Øµ Ø¹Ø±Ø¨ÙŠ Ø·ÙˆÙŠÙ„ Ø¨Ù…Ø§ ÙŠÙƒÙÙŠ Ù„Ø§Ø®ØªØ¨Ø§Ø± Ù†Ø¸Ø§Ù… Ø§Ù„ØªØ­Ù‚Ù‚ Ù…Ù† Ø§Ù„Ù†ØµÙˆØµ",
        },
        {
            "name": "cyrillic_script",
            "text": "Ð­Ñ‚Ð¾ Ð´Ð¾ÑÑ‚Ð°Ñ‚Ð¾Ñ‡Ð½Ð¾ Ð´Ð»Ð¸Ð½Ð½Ñ‹Ð¹ Ñ€ÑƒÑÑÐºÐ¸Ð¹ Ñ‚ÐµÐºÑÑ‚ Ð´Ð»Ñ Ð¿Ñ€Ð¾Ð²ÐµÑ€ÐºÐ¸ ÑÐ¸ÑÑ‚ÐµÐ¼Ñ‹",
        },
    ]

    outputs = []

    for index, case in enumerate(cases, start=1):
        creator_id = f"cap_c3_t{trial}_{index}"

        result = submit(
            case["text"],
            creator_id,
        )

        body = result["body"]

        no_authorship_score = not any(
            field in body
            for field in [
                "guess",
                "confidence",
                "model_score",
                "style_score",
                "combined_score",
            ]
        )

        passed_case = (
            result["status_code"] == 400
            and no_authorship_score
        )

        outputs.append({
            "case": case["name"],
            "creator_id": creator_id,
            "text_length": len(case["text"]),
            "no_authorship_score": no_authorship_score,
            "passed": passed_case,
            **result,
        })

    passed = sum(
        1
        for result in outputs
        if result["passed"]
    )

    return {
        "passed": passed,
        "total": 4,
        "result": f"{passed}/4",
        "details": outputs,
    }


def criterion_4(trial):
    cases = [
        "a",
        "!!!",
        "ðŸ˜€ðŸ˜€ðŸ˜€",
        "This request contains a control\x00character and should fail.",
        "Ð­Ñ‚Ð¾ Ð½ÐµÐ¿Ð¾Ð´Ð´ÐµÑ€Ð¶Ð¸Ð²Ð°ÐµÐ¼Ñ‹Ð¹ Ñ‚ÐµÐºÑÑ‚ Ð´Ð»Ñ Ð¿Ñ€Ð¾Ð²ÐµÑ€ÐºÐ¸ Ð¶ÑƒÑ€Ð½Ð°Ð»Ð°",
    ]

    creator_ids = []
    request_results = []

    for index, text in enumerate(cases, start=1):
        creator_id = f"cap_c4_t{trial}_{index}"

        creator_ids.append(creator_id)

        result = submit(text, creator_id)

        request_results.append({
            "creator_id": creator_id,
            **result,
        })

    records = read_capstone_log()

    matched_records = {}

    for record in records:
        input_data = record.get("input")

        if not isinstance(input_data, dict):
            continue

        creator_id = input_data.get("creator_id")

        if creator_id in creator_ids:
            matched_records[creator_id] = record

    checks = []

    for creator_id in creator_ids:
        record = matched_records.get(creator_id)

        if record is None:
            checks.append({
                "creator_id": creator_id,
                "found": False,
                "has_required_fields": False,
                "status_code": None,
                "passed": False,
            })
            continue

        has_required_fields = REQUIRED_LOG_FIELDS.issubset(
            record.keys()
        )

        passed_case = (
            has_required_fields
            and record.get("status_code") == 400
        )

        checks.append({
            "creator_id": creator_id,
            "found": True,
            "has_required_fields": has_required_fields,
            "status_code": record.get("status_code"),
            "passed": passed_case,
            "record": record,
        })

    passed = sum(
        1
        for check in checks
        if check["passed"]
    )

    return {
        "passed": passed,
        "total": 5,
        "result": f"{passed}/5",
        "request_results": request_results,
        "details": checks,
    }


def criterion_5(trial):
    cases = [
        (
            "This is a normal supported English paragraph with enough "
            "words for the detector to process correctly."
        ),
        (
            "A careful writer can submit ordinary supported text and "
            "receive the expected provenance scoring fields."
        ),
        (
            "The validation layer should continue allowing meaningful "
            "Latin script writing through the normal scoring process."
        ),
    ]

    outputs = []

    for index, text in enumerate(cases, start=1):
        creator_id = f"cap_c5_t{trial}_{index}"

        result = submit(text, creator_id)

        body = result["body"]

        has_fields = (
            isinstance(body, dict)
            and REQUIRED_OUTPUT_FIELDS.issubset(
                body.keys()
            )
        )

        passed_case = (
            result["status_code"] == 200
            and has_fields
        )

        outputs.append({
            "creator_id": creator_id,
            "has_required_fields": has_fields,
            "passed": passed_case,
            **result,
        })

    passed = sum(
        1
        for result in outputs
        if result["passed"]
    )

    return {
        "passed": passed,
        "total": 3,
        "result": f"{passed}/3",
        "details": outputs,
    }


def run_trial(trial):
    print(f"\n===== TRIAL {trial} =====")

    results = {
        "criterion_1": criterion_1(trial),
        "criterion_2": criterion_2(trial),
        "criterion_3": criterion_3(trial),
        "criterion_4": criterion_4(trial),
        "criterion_5": criterion_5(trial),
    }

    print(
        "Criterion 1:",
        results["criterion_1"]["result"],
    )
    print(
        "Criterion 2:",
        results["criterion_2"]["result"],
    )
    print(
        "Criterion 3:",
        results["criterion_3"]["result"],
    )
    print(
        "Criterion 4:",
        results["criterion_4"]["result"],
    )
    print(
        "Criterion 5:",
        results["criterion_5"]["result"],
    )

    return results


def verdict(trials, criterion_name):
    for trial in trials:
        result = trial["results"][criterion_name]

        if result["passed"] != result["total"]:
            return "MISSED"

    return "MET"


def main():
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    all_trials = []

    for trial_number in range(1, 4):
        results = run_trial(trial_number)

        all_trials.append({
            "trial": trial_number,
            "results": results,
        })

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    json_path = (
        RESULTS_DIR
        / f"capstone_after_{timestamp}.json"
    )

    markdown_path = (
        RESULTS_DIR
        / f"capstone_after_{timestamp}.md"
    )

    with json_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            all_trials,
            file,
            indent=2,
            ensure_ascii=False,
        )

    criterion_names = [
        (
            "criterion_1",
            "1. Short and non-semantic input rejection",
            "5/5",
        ),
        (
            "criterion_2",
            "2. Malformed content rejection",
            "6/6",
        ),
        (
            "criterion_3",
            "3. Oversized and unsupported-script handling",
            "4/4",
        ),
        (
            "criterion_4",
            "4. Rejected-request structured logging",
            "5/5",
        ),
        (
            "criterion_5",
            "5. Valid supported text still works",
            "3/3",
        ),
    ]

    lines = [
        "# Capstone After-Improvement Results",
        "",
        "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
        "|---|---|---|---|---|---|",
    ]

    for key, name, target in criterion_names:
        run_1 = all_trials[0]["results"][key]["result"]
        run_2 = all_trials[1]["results"][key]["result"]
        run_3 = all_trials[2]["results"][key]["result"]

        final_verdict = verdict(
            all_trials,
            key,
        )

        lines.append(
            f"| {name} | {target} | "
            f"{run_1} | {run_2} | {run_3} | "
            f"{final_verdict} |"
        )

    lines.extend([
        "",
        "Detailed request and response evidence is stored in:",
        "",
        f"`{json_path.as_posix()}`",
        "",
    ])

    markdown_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\n===== AFTER-IMPROVEMENT SUMMARY =====\n")

    for key, name, target in criterion_names:
        run_1 = all_trials[0]["results"][key]["result"]
        run_2 = all_trials[1]["results"][key]["result"]
        run_3 = all_trials[2]["results"][key]["result"]

        print(
            f"{name}: "
            f"{run_1}, {run_2}, {run_3} "
            f"=> {verdict(all_trials, key)}"
        )

    print("\nSaved:")
    print(json_path)
    print(markdown_path)


if __name__ == "__main__":
    main()
