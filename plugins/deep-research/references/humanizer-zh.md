# Chinese AI-Pattern Audit

Use this compact reference after a Chinese draft exists. It diagnoses recurring
machine-writing patterns; it does not define the article voice and does not
override `references/chinese-prose.md`.

## Preserve First

Do not alter a claim, qualification, citation, quotation, date, number, unit,
technical term, textual anchor, or source boundary merely to remove a stylistic
pattern. Protected material stays unchanged and factual drift returns to the
evidence audit.

## High-Confidence Problems

Remove these when they appear as generated residue rather than quoted material:

- Chat openings or endings such as praise, "当然", "希望这对你有帮助", or an
  offer to continue.
- Knowledge-cutoff disclaimers or references to training data.
- Claims attributed only to "专家", "业内人士", "研究表明", or "多个来源"
  when a specific source should be available.
- Promotional claims such as "令人叹为观止", "充满活力", "开创性",
  "必游之地", or generic claims of excellence.
- Unsupported statements that an event "标志着", "象征着", "彰显了", or
  "奠定了基础" for a broad trend.
- Generic optimistic conclusions, compulsory "挑战与展望", and conclusions that
  merely repeat the introduction.
- Business and model jargon that replaces actors and consequences, including
  "赋能", "组合拳", "打开想象空间", "认知跃迁", and "价值闭环".

## Contextual Patterns

Inspect rather than mechanically delete:

- Repeated "此外", "同时", "值得注意的是", "需要指出的是", or similar
  paragraph openers.
- Repeated dramatic reversals such as "不是……而是……", "看似……实则……",
  or "你以为……其实……".
- Forced three-part lists, parallel slogans, or several consecutive paragraphs
  ending in quotable verdicts.
- Synonym cycling that renames the same person, concept, or organization instead
  of using stable terminology.
- Fake ranges such as "从 X 到 Y" when X and Y do not form a meaningful scale.
- Excessive bold text, emoji, inline label lists, decorative quotation marks, or
  headings that exist only to create visual structure.
- Uniform sentence length, repeated paragraph shapes, and mechanical transitions.
- Decorative metaphors that move across several unrelated image systems.
- Excessive hedging that obscures the actual uncertainty.

Colons, dashes, contrast, first person, and repeated technical terms are not AI
signals by themselves. Their purpose, frequency, and article type decide whether
they need revision.

## Authenticity Without Fabrication

A human voice may contain judgment, uncertainty, mixed reactions, restrained
humor, and uneven rhythm. It may not invent firsthand experience, a scene, weather,
dialogue, psychology, or a precise detail that the research does not support.

For literary criticism, personality should emerge through selection, close
reading, interpretive risk, and engagement with counterreadings. For formal and
technical work, accuracy, proportion, and clear uncertainty are sufficient human
qualities.

## Audit Loop

1. Identify the pattern and the factual work the sentence is trying to do.
2. Keep the fact, source role, and qualification.
3. Rewrite only the unnecessary performance around them.
4. Run `scripts/check_chinese_prose.py` with the article profile.
5. Compare the result with `researched-draft.md` and restore any lost evidence.
