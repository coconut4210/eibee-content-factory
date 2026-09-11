"""Scan eibee visible copy for versioned AI-writing patterns."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable


DEFAULT_CORPUS = Path(__file__).parents[1] / "references" / "ai-voice-corpus.json"
VISIBLE_FIELDS = {
    "title", "topic", "topic_summary", "positioning", "opening", "hook",
    "core_argument", "brand_transition", "product_use", "main_visual", "cta",
    "caption", "first_comment", "on_image_text", "voiceover", "script",
    "content", "text",
}


def _flags(rule: dict[str, Any]) -> int:
    return re.IGNORECASE if rule.get("flags") == "ignorecase" else 0


def load_corpus(corpus_path: Path | str = DEFAULT_CORPUS) -> dict[str, Any]:
    path = Path(corpus_path)
    corpus = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(corpus.get("rules"), list):
        raise ValueError("AI voice corpus must contain a rules list")
    required = {"id", "category", "severity", "pattern", "rationale", "rewrite_action"}
    rule_ids: set[str] = set()
    for index, rule in enumerate(corpus["rules"]):
        if not isinstance(rule, dict) or not required.issubset(rule):
            raise ValueError(f"AI voice corpus rule[{index}] is missing required fields")
        if rule["id"] in rule_ids:
            raise ValueError("AI voice corpus rule ids must be unique")
        rule_ids.add(rule["id"])
        if rule["severity"] not in {"block", "review"}:
            raise ValueError(f"AI voice corpus rule[{index}] has invalid severity")
        re.compile(rule["pattern"], _flags(rule))
    return corpus


def scan_text(
    text: str,
    *,
    corpus_path: Path | str = DEFAULT_CORPUS,
    field: str = "text",
) -> dict[str, Any]:
    corpus = load_corpus(corpus_path)
    findings: list[dict[str, Any]] = []
    for rule in corpus["rules"]:
        for match in re.finditer(rule["pattern"], text, _flags(rule)):
            findings.append({
                "rule_id": rule["id"],
                "category": rule["category"],
                "severity": rule["severity"],
                "field": field,
                "start": match.start(),
                "end": match.end(),
                "matched_text": match.group(0).strip(),
                "rationale": rule["rationale"],
                "rewrite_action": rule["rewrite_action"],
            })
    findings.sort(key=lambda item: (item["start"], item["end"], item["rule_id"]))
    blocking_count = sum(item["severity"] == "block" for item in findings)
    return {
        "corpus_version": corpus.get("version", "unknown"),
        "passed": blocking_count == 0,
        "blocking_count": blocking_count,
        "finding_count": len(findings),
        "findings": findings,
    }


def _visible_strings(value: Any, path: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in VISIBLE_FIELDS and isinstance(child, str):
                yield child_path, child
            elif isinstance(child, (dict, list)):
                yield from _visible_strings(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            if isinstance(child, (dict, list)):
                yield from _visible_strings(child, f"{path}[{index}]")


def scan_document(document: Any, *, corpus_path: Path | str = DEFAULT_CORPUS) -> dict[str, Any]:
    corpus = load_corpus(corpus_path)
    findings: list[dict[str, Any]] = []
    for field, visible_text in _visible_strings(document):
        findings.extend(scan_text(visible_text, corpus_path=corpus_path, field=field)["findings"])
    blocking_count = sum(item["severity"] == "block" for item in findings)
    return {
        "corpus_version": corpus.get("version", "unknown"),
        "passed": blocking_count == 0,
        "blocking_count": blocking_count,
        "finding_count": len(findings),
        "findings": findings,
    }


def build_rewrite_brief(report: dict[str, Any]) -> str:
    if report.get("passed"):
        return "扫描通过，无需修改。"
    lines = [
        "仅重写下列命中位置，不要润色或重写未命中的内容。",
        "保留原有事实、数字、证据、立场和平台约束，不得添加个人经历或新主张。",
    ]
    for index, finding in enumerate(report.get("findings", []), start=1):
        lines.append(
            f'{index}. [{finding["rule_id"]}] {finding["field"]}: '
            f'“{finding["matched_text"]}”\n   修改要求：{finding["rewrite_action"]}'
        )
    lines.append("修改后必须重新扫描；blocking_count 不为 0 时不得交付或进入审核。")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 text, Markdown, or JSON file")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--rewrite-brief", action="store_true")
    args = parser.parse_args(argv)
    try:
        raw = args.input.read_text(encoding="utf-8")
        report = (
            scan_document(json.loads(raw), corpus_path=args.corpus)
            if args.input.suffix.lower() == ".json"
            else scan_text(raw, corpus_path=args.corpus)
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, re.error) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.rewrite_brief:
        print(build_rewrite_brief(report))
    else:
        print("PASS" if report["passed"] else build_rewrite_brief(report))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
