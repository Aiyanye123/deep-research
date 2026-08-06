from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_chinese_prose.py"
SPEC = importlib.util.spec_from_file_location("check_chinese_prose", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT_PATH}")
check_chinese_prose = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_chinese_prose
SPEC.loader.exec_module(check_chinese_prose)


class ChineseProseCheckerTests(unittest.TestCase):
    def test_formal_profile_allows_normal_colon_and_date_range(self) -> None:
        text = (
            "研究范围：2019—2023 年中国城市公共交通投入。"
            "样本城市的单位客运成本下降了 8.4%，地区差异仍然明显。"
        )
        findings = check_chinese_prose.analyze(text, "formal")
        self.assertFalse([item for item in findings if item.level == "failure"])
        self.assertFalse(
            [item for item in findings if item.code == "punctuation-density"]
        )

    def test_protected_quotations_and_references_are_not_rewritten_by_policy(self) -> None:
        text = """# 讨论

受访者说：“当然可以，这套系统用于赋能团队。”

> 希望这对你有帮助。

图 2：价值闭环示意图

| 字段 | 含义 |
| --- | --- |
| 说明 | 打开想象空间 |

# 参考文献

某报告：《商业闭环：组织实践》。
"""
        findings = check_chinese_prose.analyze(text, "essayistic")
        self.assertFalse([item for item in findings if item.level == "failure"])

    def test_chat_residue_and_opaque_jargon_fail(self) -> None:
        text = "当然可以。下面的组合拳将为团队赋能。希望这对你有帮助。"
        findings = check_chinese_prose.analyze(text, "essayistic")
        codes = {item.code for item in findings if item.level == "failure"}
        self.assertEqual(codes, {"chat-residue", "opaque-jargon"})

    def test_reversal_is_contextual_warning_not_failure(self) -> None:
        text = "这不是预算减少，而是统计口径变化。表 1 给出了两套口径。"
        findings = check_chinese_prose.analyze(text, "formal")
        self.assertTrue([item for item in findings if item.code == "performed-reversal"])
        self.assertFalse([item for item in findings if item.level == "failure"])

    def test_technical_terms_receive_context_warning(self) -> None:
        text = "该方法把事件链路写入日志，并用控制回路验证状态。"
        findings = check_chinese_prose.analyze(text, "technical")
        self.assertTrue([item for item in findings if item.code == "context-jargon"])
        self.assertFalse([item for item in findings if item.level == "failure"])

    def test_unknown_profile_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            check_chinese_prose.analyze("中文内容。", "unknown")


if __name__ == "__main__":
    unittest.main()
