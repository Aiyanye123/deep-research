# Chinese Prose Profiles

Use this reference only for Chinese deliverables. It adapts material-driven,
natural Chinese writing practices to Deep Research. Use it as guidance, not a
required profile, ledger, or audit process. Final prose review and polishing
are always required; separate management files are not.

## Priority

Apply rules in this order:

1. The confirmed brief and the user's explicit article requirements.
2. Factual accuracy, quotation fidelity, source boundaries, and required format.
3. The selected prose profile in this document.
4. General anti-AI-pattern guidance.

Never sacrifice a fact, citation, quotation, technical term, or required format to
make prose appear less machine-generated.

## Useful Writing Modes

These describe tendencies, not compulsory labels. A work may mix them as the
material requires. Avoid making every genre sound the same.

### `essayistic`

Use for literary and cultural criticism, reviews, columns, public-facing essays,
narrative nonfiction, opinion writing, and explanatory articles whose voice is
part of the value.

- Keep a visible thinking presence without inventing personal experience.
- Let close reading, evidence, and the writer's judgment move together.
- Permit uneven paragraph lengths, brief asides, restrained humor, and qualified
  first person when they suit the brief.
- Do not turn every paragraph into a balanced summary.

### `formal`

Use for academic papers, policy research, legal or financial analysis, market
reports, literature reviews, journals, and institutional deliverables.

- Prefer precise, calm prose and explicit source attribution.
- Let evidence hierarchy, causal limits, and uncertainty carry the voice.
- Preserve conventional headings, citations, footnotes, definitions, captions,
  and reference formatting.
- Do not add personality merely to signal that a person wrote the text.

### `technical`

Use for technical reports, standards analysis, engineering explanations, methods,
specifications, and documentation-like research.

- Prefer stable terminology, direct verbs, short dependency chains, and explicit
  conditions.
- Keep code, identifiers, formulas, units, schemas, and procedure ordering exact.
- Use repetition when it prevents ambiguity. Terminological consistency outranks
  stylistic variation.

## Citations in Chinese Prose

Follow the user's, publisher's, or discipline's citation style first. Otherwise,
put a concise attribution or hyperlink near the supported claim; name the author,
organization, document, and date when they matter to interpretation. Use notes
or a reference list for bibliographic detail when the format supports them, while
keeping the connection between claim and source clear. Group citations only when
their coverage is unambiguous. A direct quotation must be exact and locatable;
identify a translation as such. Do not cite an inaccessible original as read or
let moving a citation change which claim it supports.

The optional `scripts/check_chinese_prose.py` diagnostic accepts `--language en`
for English paragraph-edge repetition warnings. For either language, `--terms`
accepts a UTF-8 JSON object mapping a label to a list of known equivalent names,
for example `{"SQLite": ["SQLite", "某数据库译名"]}`. A warning only flags
co-occurrence; bilingual introductions and justified variants can be intentional.

## Examples of Movement and Attribution

The examples below are invented to show technique, not evidence or templates.
Use actual sources, exact locators, and verified claims in a real article; the
first-person narrative example applies only to explicitly requested creative or
fictional writing, never to non-fiction.

- **Reported feature:** Weak: “项目进展显著，居民生活得到改善。” Better:
  “按某公交公司 2025 年冬季运营月报，7 路早班车从两班增至四班后，西站几位每周去市医院复诊的老人候车时间从四十分钟缩到十来分钟；不过晚高峰跨区段的返程车仍常要等两趟才挤得上。”
  Name the record and interviewees, connect operational change to lived effect,
  and keep the remaining limit visible instead of listing sources one by one.
- **Technical analysis:** Weak: “这个设置可以解决并发问题。” Better:
  “在单写者锁模式下（见引擎手册第 4 节），两个连接同时写入时，第二个连接会因等待锁而阻塞；把写事务拆短能压缩占锁窗口，但无法消除高并发持续写入下的排队瓶颈。”
  Cite the relevant specification, explain the condition and mechanism, and
  state where the fix stops working.
- **Research review:** Weak: “研究一致证明工具提高效率。” Better:
  “A 团队 2024 年的实验室对照实验（N=48）测得单次检索耗时缩短约两成；B 团队 2025 年对医院科室的半年现场追踪则显示，因交接审批未改，日均总工时变化不大。两项研究的任务边界与周期不同，不能直接合并。”
  Identify each study with its design and scope before comparing conclusions.
- **Cultural criticism:** Weak: “人物的沉默体现了深刻的孤独。” Better:
  “第三幕客厅聚会那场戏里，众人刚把话头转向他，他便低头去整袖口，直到旁人另起话题才抬眼；他用这几秒钟把反应藏进动作里，场上的尴尬也就留在了对话之外。”
  Anchor the scene, move from concrete detail to tension in the work itself, and
  avoid meta-commentary such as “让读者看到”.
- **Film or literary commentary (invented):** Weak: “导演用精妙的剪辑和压抑的配乐，深刻揭露了现代人的异化。”
  Better: “饭局散场那段戏（约第 68 分钟），镜头没有切去主角的脸，而是盯着桌上凉透的残羹摇了将近二十秒；门外电梯的提示音一声接一声，屋里始终没人去关灯，把原本还勉强维持的体面晾在原地，观众也跟着一起等这场尴尬自己垮掉。”
  Anchor the moment, state what camera and sound do, and show how that formal
  choice shifts the scene's relationship or viewing experience.
- **Creative or fictional narrative (invented; explicitly authorized fiction only):**
  Weak: “站在空荡的站台上，我突然明白了时间流逝的无情与生命的珍贵。”
  Better: “末班车开走后，站台灯熄掉一半，售票亭玻璃上还贴着去年的春运时刻表。我把围巾又绕了一圈，沿着站外那排还没拆的旧围挡往回走。”
  Only for explicitly requested fiction or creative writing—never invent scenes
  or first-person experience in non-fiction; let environment and physical action
  carry mood instead of announcing an abstract epiphany.

## Literary Craft Options

Use these options when the material and purpose call for them; direct judgment
openings, explicit explanation of how a detail supports a point, and settled
conclusions remain valid whenever the piece needs them.

- **调节叙述距离：** 按文章需要决定贴近现场、紧贴文本细部，还是退后半步作对照；
  态度可以通过选材、停顿和词义轻重带出，不必每段都由作者出面表态。
- **并置与延迟转折：** 除显式转折词外，也可把不同处境的事实、前后呼应的细节或
  表面一致却彼此错位的材料并排摆放，让反差自己推进问题。
- **母题回环与留白：** 适合长文或随笔时，可以让同一物象、动作或说法在后文换个
  处境再出现，借含义偏移组织段落；需要点明它与论点的关系时直接说清，适合留白
  收束时则不必再补一句总结。
- **守住语体质感：** 白话主干里可适度借用口语节奏或简洁书面词，但全篇应保持同一套
  语体底色，避免中途突然滑入翻译腔或生硬的术语堆砌。

## Material-Driven Writing

Use the material and actual sources already collected. Research and writing can
inform each other; follow a consequential gap when needed without restarting
intake or creating a second formal workflow.

- Let details, reasoning, and interpretation develop the subject. Passages can
  build atmosphere, pacing, or ambiguity where the genre benefits; each paragraph
  need not prove a registered claim. Remove repetition that adds no meaning.
- If a consequential assertion lacks support, check the relevant source or
  adjust the claim. In research, criticism, and non-fiction, do not invent
  examples, scenes, consensus, quotations, or user experience (only explicitly
  requested fiction or creative storytelling may invent scenes); do not silently
  shorten the requested deliverable.
- In literary criticism, let specific scenes, formal features, dialogue, editing,
  framing, sound, omissions, or textual contrasts support interpretation.
- In formal and technical work, distinguish observed fact, source claim,
  inference, interpretation, and forecast.

## Find A Speaking Position

The writer's presence comes from selection and judgment, not simulated biography.
Before drafting, identify internally:

- What the evidence establishes and what remains uncertain.
- Which finding or contradiction makes this article worth writing.
- What the writer currently believes, why, and where that judgment stops.
- What a reader will naturally need to know after each section.

Do not fabricate having watched, interviewed, tested, visited, or experienced
something in research, reporting, or criticism; only explicitly requested
fiction or creative storytelling may invent scenes or persona. First person in
non-fiction may express a defensible judgment or describe a real research action,
but it must not create false firsthand authority.

## Build Natural Movement

- Let a connected thought develop across paragraphs. Related observations,
  source material, and interpretation can stay together until their relation is
  clear. Break paragraphs when focus or pace calls for it; avoid both scattered
  verdicts and uniformly long blocks.
- Do not repeatedly use the same paragraph sequence of overview, concession,
  correction, and closing maxim. A useful judgment may deserve emphasis, but
  every paragraph need not produce a quotable line or summarize itself.
- State actual distinctions and explain their consequences. Repeatedly setting
  up a simplified opposing view and correcting it can conceal how little the
  reasoning has advanced. Replacing the connective does not fix that structure.
- Remove defensive padding aimed at imagined objections. Keep necessary limits
  beside the claims they affect and explain how they change the conclusion.
  Direct judgment still needs its actual uncertainty and competing evidence.
- Use a theoretical concept when it helps explain an action, relationship,
  conflict, or mechanism. Make the connection clear in language the reader can
  follow. Replace labels that merely rename observations with the actual analysis;
  preserve exact definitions and terms needed for academic or technical work.
- In essays and criticism, sustain an attentive speaking position: what is
  noticed, how the experience develops, and why the response changes. Use
  supported particulars instead of repeatedly naming abstract emotion or depth.
  Let emotional movement follow discoveries in the material; do not impose a
  crescendo or moral verdict. Formal and technical writing can remain restrained
  and precise.
- Introduce a source where it contributes to the explanation. Attribution,
  material, and judgment can form continuous prose; citations may move with the
  supported claims. Keep evidence boundaries while avoiding a new source-summary
  and mini-verdict for every example.
- Reach the subject quickly. Avoid announcing the article structure unless the
  article type requires an abstract, executive summary, or methods overview.
- Put the actor, action, claim, or observed feature early enough that the reader
  can follow a long sentence.
- Connect sections through evidence and unresolved questions, not generic depth
  markers such as "更深一层" or "值得注意的是".
- Vary sentence and paragraph length in response to information density. Do not
  manufacture roughness, slang, errors, or random asides.
- Let concrete evidence carry emotion and significance. Do not explain a scene a
  second time after its effect is already clear.
- State judgments directly, then place their reasons nearby. Do not create a
  straw misunderstanding solely to perform a dramatic reversal.
- Stop when the argument is complete. Do not append a generic summary, optimism,
  historical significance, or forced elevation.

## Protected Content

Treat the following as protected unless the user explicitly asks to transform it:

- Direct quotations and primary-text excerpts.
- Laws, standards, definitions, formulas, code, commands, and identifiers.
- Names, dates, numbers, ranges, units, statistical notation, and technical terms.
- Citation markers, footnotes, bibliography entries, URLs, and link targets.
- Headings required by a journal, report template, or publication.
- Tables, figure IDs, captions, source notes, alt text, and cross-references.
- Markdown, document, and machine-readable structure.

Colons, dashes, parallel structures, contrast sentences, and first person are not
global errors. Judge their frequency and function under the selected profile.

## Rewrite Rules

- Actively dismantle recurring mechanical symmetry and aphoristic closures
  across connected passages. Rebuild sentences around the actual action,
  sequence, cause, or consequence, adjusting sentence boundaries and paragraph
  movement. Restore natural variation in length and emphasis; swapping paired
  connectives or synonyms alone is insufficient. Keep a balanced comparison when
  it conveys a necessary distinction, rather than banning sentence forms.
- Delete defensive self-commentary, declarations of fairness, and disclaimer
  padding addressed to imagined critics. Where a limit or distinction changes
  the judgment, state its substance and consequence directly by the relevant
  claim. Preserve actual uncertainty and counterevidence. Reread the revised
  passage with its neighbors for rhythm, continuity, and preserved meaning.
- Prioritize natural, concrete, accurate Chinese. Use precise verbs, meaningful
  details, and judgments with reasons. Language should serve the content.
- Replace empty praise such as "很高级" or "很有感觉" with the observable
  feature, action, contrast, or effect that supports the judgment. In research,
  criticism, and non-fiction, use actual material and do not invent a detail to
  make a sentence sound concrete.
- Cut stock phrases, bureaucratic voice, business jargon, invented labels, and
  degree adverbs that add no information. Rhetoric, abstractions, and grand
  evaluations must not substitute for explaining the subject.
- Let sentence length vary naturally. A long sentence should serve narrative,
  rhythm, or argument with a clear internal relation. Revise overloaded syntax
  rather than mechanically breaking every sentence into short statements.
- Polish substantially where needed: rewrite sentences, paragraphs, and
  transitions, remove redundant explanations, and improve the order of material.
  A few synonym substitutions do not constitute a full prose review. Preserve
  intellectual complexity, the requested length, and productive literary language.
- Replace inflated significance and promotional claims with the specific fact or
  consequence that justifies them.
- Replace vague authority with a named source, institution, document, date, or a
  clearly marked uncertainty.
- Prefer direct verbs over nominalized management language when precision is not
  lost.
- Remove chat residue, praise of the user, process narration, and generic offers
  of further help from the deliverable.
- Break repetitive three-part structures and uniform mid-length sentences when
  they are habits rather than necessary organization.
- Keep useful repetition in formal and technical writing when it preserves a
  defined term or prevents reference ambiguity.
- Preserve counterarguments, qualifications, and inconvenient evidence. Natural
  prose is not permission to make the thesis cleaner than the research.

## Final Reading

Read the whole completed text and polish before delivery. Check the passage and
its connections for a limited edit. Revisit facts or source boundaries affected
by substantive changes. The Chinese checker may help diagnose a specific issue;
it is optional, and warnings require judgment. No paired drafts, handoff artifact,
or separate factual-drift certificate is required.

Read paragraph endings and transitions together to hear repeated closures,
reversals, and reannouncements of the thesis. Revise the connected passage when
that pattern flattens its movement. Do not create a new quota for sentence forms,
metaphors, paragraph lengths, or ending types. When learning from a user sample,
transfer its handling of viewpoint and development, not its conspicuous wording,
added intensity, or unverified detail.
