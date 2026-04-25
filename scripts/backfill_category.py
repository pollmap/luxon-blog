#!/usr/bin/env python3
"""
backfill_category.py — 기존 블로그 포스트에 category frontmatter 자동 주입.

사용법:
  python scripts/backfill_category.py              # dry-run (리포트만)
  python scripts/backfill_category.py --verbose    # 개별 파일 결과 출력
  python scripts/backfill_category.py --write      # 실제 파일 수정

카테고리 5개: building / field / failure / deep-dive / retro
매칭 되지 않은 포스트는 UNMATCHED로 리포트되며 수동 태깅이 필요하다.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

# Windows cp949 환경에서도 한글/em-dash 출력하도록 UTF-8 강제
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "src" / "content" / "blog"


# slug/filename 기반 카테고리 추론 룰 (상단이 더 높은 우선순위)
_CATEGORY_RULES: list[tuple[re.Pattern[str], str]] = [
    # 1) Deep Dive — 학술/이론/수식/모델 심층
    (
        re.compile(
            r"^(kyle|stochastic|game-theory|great-books|double-machine-learning|"
            r"structural-vector|rough-volatility|optimal-execution|stat-arb|"
            r"factor-risk|robust-investment|slippage|extremity-premium|"
            r"delta-neutral-liquidity|duesenberry|risk-based-auto|"
            r"uncertain-asymmetric|vulnerable-growth|xrp-anomaly|spx-vix-optimal|"
            r"crypto-microstructure|crypto-lob|crypto-portfolio|deep-learning-multi)"
        ),
        "deep-dive",
    ),
    (
        re.compile(
            r"(kyle-model|optimal-transport|monte-carlo|copula|topological|"
            r"anomaly-prediction|lstm-|factor-investing|stat-arb-)"
        ),
        "deep-dive",
    ),
    (re.compile(r"^understanding-[a-z0-9]{6,}"), "deep-dive"),

    # 2) Retro — 회고·정기 업데이트
    (
        re.compile(
            r"^(retro|weekly|monthly|quarterly|yorun|요런시점)"
        ),
        "retro",
    ),
    (re.compile(r"(looking-back|year-in-review|quarter-recap)"), "retro"),

    # 3) Field — 시장/사건/뉴스/산업 관찰
    (
        re.compile(
            r"^(oracle|macro-daily|predictive_history|softbank|"
            r"claude-subscriptions|llm-stock|mev-auction)"
        ),
        "field",
    ),
    (
        re.compile(
            r"(kimchi-premium|fx-spillover|stablecoin|us-recession|"
            r"briefing|ipo-impact)"
        ),
        "field",
    ),

    # 4) Building — 구현/도구/프로젝트 릴리스
    (
        re.compile(
            r"^(building-|implementing-|deploying-|scaling-|integrating-|shipping-|"
            r"nexus-finance|luxon-terminal|cufa-report|"
            r"mcp-[0-9]|mcp-tools|mcp-server|"
            r"open-source-|quant-v[0-9]|quant-v\d|"
            r"risk-management-quant)"
        ),
        "building",
    ),
    (
        re.compile(
            r"(toolchain|pipeline-release|infrastructure-release)"
        ),
        "building",
    ),

    # 5) Failure — 실패·회귀·버그
    (
        re.compile(
            r"^(postmortem|failure|regression|bug-|lesson-learned|fixing-)"
        ),
        "failure",
    ),
    (re.compile(r"(broke-|crashed-|performance-regression|rollback-)"), "failure"),

    # 6) Catch-all fallbacks — 더 넓은 패턴 (위 세부 룰이 먼저 확인됨)
    # 'understanding-*' 대부분은 학술 요약 → deep-dive
    (re.compile(r"^understanding-"), "deep-dive"),
    # jordan_peterson 대화·강의 해석 → deep-dive
    (re.compile(r"^jordan_peterson-"), "deep-dive"),
    # 퀀트 모델 구현/논문 (hmm/bsde/factor/regime 등)
    (
        re.compile(
            r"^(adaptive-|conformal-|crypto-carry|deepm-|gt-score|hybrid-hmm|"
            r"ivdfm-|macro-regime|perp-futures|tcp-tail|universal-crypto)"
        ),
        "deep-dive",
    ),
    (
        re.compile(
            r"(hmm|bsde|change-point|dynamic-factor|anti-overfitting|"
            r"tail-calibration|microstructure-ofi|regime-robust|carry-crash)"
        ),
        "deep-dive",
    ),
]


def infer_category(slug: str) -> Optional[str]:
    for pattern, category in _CATEGORY_RULES:
        if pattern.search(slug):
            return category
    return None


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """YAML frontmatter + body 분리. Frontmatter 없으면 빈 dict."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    fm_text = text[4:end]
    body = text[end + 5:]
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return {}, text
    return fm, body


def write_frontmatter(fm: dict, body: str) -> str:
    """dict를 YAML frontmatter로 직렬화."""
    fm_text = yaml.safe_dump(
        fm,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    return f"---\n{fm_text}---\n{body}"


def slug_from_path(path: Path) -> str:
    """'2026-04-02-foo-bar.md' → 'foo-bar'"""
    name = path.stem
    m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)", name)
    return m.group(1) if m else name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    parser.add_argument(
        "--write", action="store_true", help="apply changes (default: dry-run)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="print per-file result"
    )
    parser.add_argument(
        "--unmatched-only",
        action="store_true",
        help="verbose: show only unmatched posts (useful for tuning rules)",
    )
    args = parser.parse_args()

    if not BLOG_DIR.exists():
        print(f"ERROR: blog dir not found: {BLOG_DIR}", file=sys.stderr)
        return 1

    posts = sorted(BLOG_DIR.glob("*.md"))
    print(f"Scanning {len(posts)} posts in {BLOG_DIR}\n")

    stats = {
        "already_tagged": 0,
        "inferred": 0,
        "unmatched": 0,
        "parse_error": 0,
        "per_category": {},
    }
    modified: list[str] = []
    unmatched_posts: list[str] = []

    for post in posts:
        try:
            text = post.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            stats["parse_error"] += 1
            continue

        fm, body = parse_frontmatter(text)
        if not fm:
            stats["parse_error"] += 1
            continue

        slug = slug_from_path(post)

        if "category" in fm and fm["category"]:
            stats["already_tagged"] += 1
            cat = fm["category"]
            stats["per_category"][cat] = stats["per_category"].get(cat, 0) + 1
            continue

        inferred = infer_category(slug)
        if inferred is None:
            stats["unmatched"] += 1
            unmatched_posts.append(post.name)
            if args.verbose and (args.unmatched_only or not args.unmatched_only):
                print(f"  [UNMATCHED] {post.name}")
            continue

        stats["inferred"] += 1
        stats["per_category"][inferred] = stats["per_category"].get(inferred, 0) + 1
        fm["category"] = inferred

        if args.write:
            post.write_text(write_frontmatter(fm, body), encoding="utf-8")
            modified.append(post.name)

        if args.verbose and not args.unmatched_only:
            print(f"  [{inferred:>9}] {post.name}")

    print("\n--- Summary ---")
    print(f"Total posts:        {len(posts)}")
    print(f"Already tagged:     {stats['already_tagged']}")
    print(f"Newly inferred:     {stats['inferred']}")
    print(f"Unmatched:          {stats['unmatched']}")
    if stats["parse_error"]:
        print(f"Parse errors:       {stats['parse_error']}")

    print("\nCategory distribution:")
    for cat, count in sorted(stats["per_category"].items()):
        print(f"  {cat:>10}: {count}")

    if args.write and modified:
        print(f"\n{len(modified)} file(s) modified.")
    elif not args.write:
        print("\n[dry-run] Use --write to apply changes.")

    if stats["unmatched"] and not args.verbose:
        print(
            f"\n{stats['unmatched']} unmatched — run with -v --unmatched-only to list."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
