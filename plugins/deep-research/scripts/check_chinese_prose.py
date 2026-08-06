#!/usr/bin/env python3
"""Profile-aware diagnostics for Chinese Deep Research prose.

Adapted from Human Writing Skill 1.1.0 under the MIT License. See
THIRD_PARTY_NOTICES.md. The checker reports shapes; it never rewrites prose.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


PROFILES = ("essayistic", "formal", "technical")

CHAT_RESIDUE = (
    "希望这对你有帮助",
    "希望这对您有帮助",
    "如果你想让我",
    "如果您想让我",
    "请告诉我",
    "当然可以",
    "您说得完全正确",
)

MODEL_DISCLOSURES = (
    "作为一个AI",
    "作为 AI",
    "根据我最后的训练",
    "我的知识截止",
    "训练数据截止",
)

HARD_JARGON = (
    "商业闭环",
    "价值闭环",
    "赋能",
    "组合拳",
    "打开想象空间",
    "认知跃迁",
    "价值释放",
)

CONTEXT_JARGON = (
    "底层逻辑",
    "顶层设计",
    "技术底座",
    "链路",
    "方法论",
    "核心变量",
    "生态位",
    "颗粒度",
    "协同",
    "沉淀",
)

PROMOTIONAL = (
    "令人叹为观止",
    "充满活力",
    "开创性",
    "必游之地",
    "无缝体验",
    "持久影响",
    "不断演变的格局",
)

ROAD_SIGNS = (
    "更微妙的是",
    "还有一层",
    "只说对了一半",
    "值得注意的是",
    "需要指出的是",
    "从某种意义上说",
    "让我们深入探讨",
    "下面将深入探讨",
)

GENERIC_ENDINGS = (
    "未来可期",
    "让我们拭目以待",
    "迈出了重要一步",
    "开启了新的篇章",
    "带来更多可能性",
)

VAGUE_AUTHORITY = (
    re.compile(r"(?:有|一些|多位)?专家(?:普遍)?(?:认为|指出|表示|强调)"),
    re.compile(r"(?:业内|行业)人士(?:认为|指出|表示)"),
    re.compile(r"(?:研究|报告|数据显示|资料)表明"),
    re.compile(r"(?:多个|多方)来源(?:显示|指出|认为)"),
    re.compile(r"(?:有|一些)?观察者(?:认为|指出)"),
)

PIVOTS = (
    re.compile(r"(?:并)?不是[^。！？\n]{0,90}而是"),
    re.compile(r"并非[^。！？\n]{0,90}而是"),
    re.compile(r"不在于[^。！？\n]{0,90}而在于"),
    re.compile(r"与其说[^。！？\n]{0,90}(?:不如|倒不如)"),
    re.compile(r"看似[^。！？\n]{0,90}(?:其实|实际|实则)"),
    re.compile(r"表面(?:上)?[^。！？\n]{0,90}(?:其实|实际|实则)"),
    re.compile(r"你以为[^。！？\n]{0,90}其实"),
)

SIGNIFICANCE = (
    re.compile(r"(?:标志着|象征着|彰显了|见证了)[^。！？\n]{0,45}(?:意义|转变|时代|趋势|影响)?"),
    re.compile(r"(?:奠定了|打下了)[^。！？\n]{0,35}(?:基础|基石)"),
)

REPEATED_OPENERS = (
    "此外",
    "同时",
    "然而",
    "因此",
    "首先",
    "其次",
    "最后",
    "值得注意的是",
    "需要指出的是",
)


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    line: int
    message: str
    sample: str


def mask_value(value: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in value)


def mask_span(match: re.Match[str]) -> str:
    return mask_value(match.group())


def mask_lines(text: str, predicate) -> str:
    lines = text.splitlines(keepends=True)
    return "".join(mask_value(line) if predicate(line) else line for line in lines)


def mask_protected(text: str) -> str:
    """Mask protected structures while preserving offsets and line numbers."""

    patterns = (
        re.compile(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", re.DOTALL),
        re.compile(r"```.*?```", re.DOTALL),
        re.compile(r"`[^`\n]*`"),
        re.compile(r"\]\([^\n)]*\)"),
        re.compile(r"https?://[^\s)>]+"),
        re.compile(r"<[^>\n]+>"),
        re.compile(r"“[^”\n]*”|「[^」\n]*」|『[^』\n]*』"),
    )
    masked = text
    for pattern in patterns:
        masked = pattern.sub(mask_span, masked)

    bibliography = re.compile(
        r"(?im)^#{1,6}\s*(?:参考文献|参考资料|References|Bibliography)\s*$"
    ).search(masked)
    if bibliography:
        masked = masked[: bibliography.start()] + mask_value(masked[bibliography.start() :])

    def protected_line(line: str) -> bool:
        stripped = line.lstrip()
        if stripped.startswith(">"):
            return True
        if stripped.startswith("|") and "|" in stripped[1:]:
            return True
        return bool(
            re.match(
                r"(?:图|表)\s*\d+[\s.:：-]|(?:Figure|Table)\s+\d+[\s.:：-]|"
                r"(?:来源|资料来源|Source)\s*[:：]",
                stripped,
                re.IGNORECASE,
            )
        )

    return mask_lines(masked, protected_line)


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def excerpt(value: str, width: int = 70) -> str:
    compact = re.sub(r"\s+", " ", value).strip()
    return compact if len(compact) <= width else compact[: width - 1] + "…"


def term_findings(
    original: str,
    prose: str,
    terms: tuple[str, ...],
    *,
    level: str,
    code: str,
    message: str,
) -> list[Finding]:
    findings = []
    for term in terms:
        for match in re.finditer(re.escape(term), prose):
            findings.append(
                Finding(level, code, line_number(original, match.start()), message, term)
            )
    return findings


def regex_findings(
    original: str,
    prose: str,
    patterns: tuple[re.Pattern[str], ...],
    *,
    level: str,
    code: str,
    message: str,
) -> list[Finding]:
    matches = []
    for pattern in patterns:
        matches.extend(pattern.finditer(prose))
    return [
        Finding(
            level,
            code,
            line_number(original, match.start()),
            message,
            excerpt(match.group()),
        )
        for match in sorted(matches, key=lambda item: item.start())
    ]


def paragraph_openers(original: str, prose: str) -> list[Finding]:
    positions: dict[str, list[int]] = {item: [] for item in REPEATED_OPENERS}
    offset = 0
    for line in prose.splitlines(keepends=True):
        stripped = line.lstrip(" \t#*-0123456789.、")
        for opener in REPEATED_OPENERS:
            if stripped.startswith(opener):
                positions[opener].append(offset + line.find(opener))
                break
        offset += len(line)

    findings = []
    for opener, matches in positions.items():
        if len(matches) >= 4:
            findings.append(
                Finding(
                    "warning",
                    "repeated-opener",
                    line_number(original, matches[0]),
                    f"同一段落开场重复 {len(matches)} 次，检查是否由模板推进。",
                    opener,
                )
            )
    return findings


def punctuation_findings(original: str, prose: str, profile: str) -> list[Finding]:
    thresholds = {
        "essayistic": {"—": 3, "–": 3, "：": 10, ":": 10},
        "formal": {"—": 8, "–": 8, "：": 24, ":": 24},
        "technical": {"—": 12, "–": 12, "：": 36, ":": 36},
    }
    findings = []
    for symbol, threshold in thresholds[profile].items():
        positions = [match.start() for match in re.finditer(re.escape(symbol), prose)]
        if len(positions) >= threshold:
            findings.append(
                Finding(
                    "warning",
                    "punctuation-density",
                    line_number(original, positions[0]),
                    f"全文出现 {len(positions)} 个“{symbol}”，检查是否形成固定句法；该标点不是禁用项。",
                    symbol,
                )
            )
    return findings


def rhythm_findings(original: str, prose: str) -> list[Finding]:
    paragraphs: list[tuple[int, str]] = []
    for match in re.finditer(r"(?m)^(?!\s*$)(.+)$", prose):
        value = match.group(1).strip()
        if value and not value.startswith("#"):
            paragraphs.append((match.start(), value))
    if len(paragraphs) < 10:
        return []

    short = [item for item in paragraphs if len(re.findall(r"[\u4e00-\u9fff]", item[1])) <= 24]
    if len(short) / len(paragraphs) < 0.75:
        return []
    return [
        Finding(
            "warning",
            "uniform-short-paragraphs",
            line_number(original, short[0][0]),
            "超过四分之三的可识别段落很短，检查是否在排队输出结论。",
            excerpt(short[0][1]),
        )
    ]


def analyze(text: str, profile: str) -> list[Finding]:
    if profile not in PROFILES:
        raise ValueError(f"Unknown profile: {profile}")
    prose = mask_protected(text)
    findings = []
    findings.extend(
        term_findings(
            text,
            prose,
            CHAT_RESIDUE + MODEL_DISCLOSURES,
            level="failure",
            code="chat-residue",
            message="删除对话残留或模型自我说明。",
        )
    )
    findings.extend(
        term_findings(
            text,
            prose,
            HARD_JARGON,
            level="failure",
            code="opaque-jargon",
            message="用具体参与者、动作、成本或后果替代空泛黑话。",
        )
    )
    findings.extend(
        term_findings(
            text,
            prose,
            CONTEXT_JARGON,
            level="warning",
            code="context-jargon",
            message="结合专业语境判断；本义准确时保留，用来抬价时改写。",
        )
    )
    findings.extend(
        term_findings(
            text,
            prose,
            PROMOTIONAL,
            level="warning",
            code="promotional-language",
            message="检查宣传性措辞是否有具体证据支撑。",
        )
    )
    findings.extend(
        term_findings(
            text,
            prose,
            ROAD_SIGNS,
            level="warning",
            code="model-signpost",
            message="让证据或问题承担过渡，避免模板化洞察路标。",
        )
    )
    findings.extend(
        term_findings(
            text,
            prose,
            GENERIC_ENDINGS,
            level="warning",
            code="generic-ending",
            message="检查结尾是否脱离证据而强行乐观或升华。",
        )
    )
    findings.extend(
        regex_findings(
            text,
            prose,
            VAGUE_AUTHORITY,
            level="warning",
            code="vague-authority",
            message="核对附近是否有明确来源；否则命名来源、标明不确定性或删除。",
        )
    )
    findings.extend(
        regex_findings(
            text,
            prose,
            PIVOTS,
            level="warning",
            code="performed-reversal",
            message="检查是否为了显得深刻而制造翻案；真实对比和论证转折可以保留。",
        )
    )
    findings.extend(
        regex_findings(
            text,
            prose,
            SIGNIFICANCE,
            level="warning",
            code="inflated-significance",
            message="用可验证的影响或具体后果替代空泛意义宣告。",
        )
    )
    findings.extend(paragraph_openers(text, prose))
    findings.extend(punctuation_findings(text, prose, profile))
    findings.extend(rhythm_findings(text, prose))
    return sorted(findings, key=lambda item: (item.line, item.level, item.code))


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Chinese Deep Research prose without rewriting it."
    )
    parser.add_argument("path", help="Markdown/text path, or - for stdin")
    parser.add_argument("--profile", choices=PROFILES, required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        text = read_text(args.path)
    except (OSError, UnicodeError) as error:
        print(f"无法读取稿件：{error}", file=sys.stderr)
        return 2
    if not re.search(r"[\u4e00-\u9fff]", text):
        print("没有检测到中文正文。", file=sys.stderr)
        return 2

    findings = analyze(text, args.profile)
    failures = [item for item in findings if item.level == "failure"]
    warnings = [item for item in findings if item.level == "warning"]

    if args.as_json:
        print(
            json.dumps(
                {
                    "profile": args.profile,
                    "status": "fail" if failures else "pass",
                    "failures": [asdict(item) for item in failures],
                    "warnings": [asdict(item) for item in warnings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"配置：{args.profile}")
        print(f"失败项：{len(failures)}；警告项：{len(warnings)}")
        if failures:
            print("\n需要修改")
            for item in failures:
                print(f"- 第 {item.line} 行 [{item.code}] {item.message} {item.sample}")
        if warnings:
            print("\n需要人工判断")
            for item in warnings:
                print(f"- 第 {item.line} 行 [{item.code}] {item.message} {item.sample}")
        if not findings:
            print("\n未发现检查器覆盖的问题。")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
