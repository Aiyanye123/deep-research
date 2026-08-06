<div align="center">
  <img src="plugins/deep-research/assets/logo.png" width="112" alt="Deep Research 图标">
  <h1>Deep Research for Codex</h1>
  <p>面向高质量长文的可控、可恢复、证据驱动型深度研究插件。</p>
  <p><strong>简体中文</strong> | <a href="README_EN.md">English</a></p>
</div>

> [!NOTE]
> 这是一个独立开源的 Codex 插件，不是 ChatGPT 官方 Deep Research 的复刻，也不使用 OpenAI 的私有内部机制。

## 为什么做这个插件

普通的“帮我深入研究”提示词很容易在打开少量网页后提前停止，也常常直接从搜索摘要跳到成稿。Deep Research 把研究过程变成一个可检查的持久化工作流：先澄清真正影响研究方向的问题，再分波次搜索、登记来源与论断、检查证据缺口，只有达到动态证据门槛后才允许进入提纲和写作。

它主要面向：

- 文学、影视与文化批评
- 学术论文、政策研究和研究报告
- 市场、行业、金融和法律分析
- 需要数千字到数万字的证据型长文
- 需要图表、示意图或解释性图片的研究成果

## 核心能力

- **动态澄清**：至少提出 3 个问题，但不设固定上限；问题由选题中的真实不确定性生成，不使用与任务无关的固定问卷。
- **多波次研究**：把检索分为定位、扩展、反证、缺口补全和核验等阶段，阻止模型只搜索几个网页就收尾。
- **动态证据门**：来源数量不是唯一目标。插件同时检查来源质量、信息增量、关键论断覆盖、反方材料和未解决缺口。
- **持久研究会话**：查询、来源、论断、文本锚点、缺口和阶段状态都会写入文件，可在上下文压缩或新任务中继续。
- **原创洞见**：在写作前区分材料共识、现有解释、反向解读与作者自己的论证，避免机械拼接网页摘要。
- **长文连续性**：通过提纲、章节证据分配与 continuity notes 维持术语、论证和章节衔接。
- **多语言成稿润色**：根据语言、文章类型和内容调整表达，同时保护事实、引用与原有论证。
- **事实防漂移**：Humanizer 前自动保留不可变的研究稿副本，润色后再次核对引用、数字、限定语和来源边界。
- **研究可视化**：可生成可复现图表、Mermaid 图、表格，或调用 Codex 图像生成能力制作明确标注的解释性图片。

## 工作流

```text
动态澄清
  -> 确认 brief
  -> 多波次检索与来源登记
  -> 证据门
     -> 未通过：继续补充研究
     -> 通过：证据审计
  -> 洞见与提纲
  -> 独立洞见验收
  -> 图表与视觉决策
  -> 长文写作
  -> 保存原始研究稿
  -> 按文章类型润色
  -> 最终事实审计
  -> 工作流验收
```

## 安装

要求已安装支持插件市场的 Codex CLI。

```powershell
codex plugin marketplace add Aiyanye123/deep-research
codex plugin add deep-research@aiyanye-deep-research
```

安装或升级后请新建一个 Codex 任务，使新版 Skill 被完整加载。

## 使用

在 Codex 中选择 **Deep Research**，或直接提出类似请求：

```text
使用 Deep Research 调研这个选题。在正式研究前，根据选题中真正影响论证和检索方向的不确定性向我提问；确认 brief 后再开始多波次研究，达到证据门槛后撰写长文。
```

插件会先完成动态提问，不会在同一轮直接开始搜索。用户回复后，它会生成并确认 brief，再建立持久化研究会话。

## 七个 Skill

| Skill | 职责 |
| --- | --- |
| `deep-research` | 主流程、澄清协议和阶段门控 |
| `research-orchestrator` | 查询策略、研究波次、缺口与停止条件 |
| `evidence-auditor` | 来源、论断、引用与事实漂移审计 |
| `insight-architect` | 原创论点、反向解读和长文结构 |
| `research-visualizer` | 图表、表格、示意图和生成图片 |
| `longform-writer` | 分章节写作与长文连续性 |
| `prose-humanizer` | 文章类型导向的多语言成稿润色 |

主 Skill 会按固定阶段调用其余六个 Skill，并通过 `workflow-gate` 检查是否有阶段被遗漏。

## 中文写作配置

写作方向由语言、文章类型、议题、证据密度、读者关系和已确认的 brief 共同决定，不以发布渠道作为文风预设。中文成稿会选择一个内容导向的配置：

- `essayistic`：强调解释、判断和行文节奏，允许有依据的第一人称与不完全对称的段落结构。
- `formal`：强调精确归因、论证边界、稳定结构和规范的研究文档组成部分。
- `technical`：强调术语一致、条件明确、步骤直接，并精确保留代码、公式、单位和标识符。

`style-sheet.md` 会记录所选配置、保护内容、引用可见性、证据保留策略、句子节奏、段落推进、技术密度以及需要保留或避免的表达习惯。润色阶段以会话中的论断、来源、文本锚点和提纲为材料基础，不得重新启动澄清、创建第二套研究计划、虚构材料、改写直接引语或擅自缩短目标篇幅。发现证据缺口时必须返回研究流程。

中文稿件完成润色后运行：

```powershell
python plugins/deep-research/scripts/check_chinese_prose.py <稿件.md> --profile <essayistic|formal|technical>
```

检查器只将模型自述、对话结尾和不透明的宣传黑话等高置信残留判为失败。标点、转折、第一人称和依赖语境的术语最多产生警告，不会被机械删除。直接引语、引文标记、参考文献、表格、图注、链接、代码、名称、数字和机器字段受到保护。英文及其他语言使用对应语言的润色规则，不运行中文检查器。

## 研究深度

插件提供 `light`、`standard`、`deep` 和 `exhaustive` 四种配置，但使用动态目标而不是简单凑来源数。当前 `exhaustive` 配置的合格来源下限为 24、证据价值下限为 65 单位、动态来源目标为 100；只有完成来源通道、反证、核验和信息饱和检查后，才可能低于动态目标停止。稀缺、权威、深入阅读且能覆盖关键论断的材料可以获得更高证据价值，低质量聚合页、重复转载和无信息增量的页面不能用来填数。

## 会话与评估

严重研究任务会在独立目录中保存 `brief.md`、研究计划、来源与论断账本、文本锚点、提纲、原始研究稿和最终审计结果。即使 Codex 发生上下文压缩，也可以通过会话文件继续，而不是依赖聊天记忆。

运行结构化评估：

```powershell
python plugins/deep-research/scripts/evaluate_run.py --session <研究会话目录>
```

## 项目结构

```text
.agents/plugins/marketplace.json     Codex Git 市场清单
plugins/deep-research/
  .codex-plugin/plugin.json          插件元数据
  skills/                             七个工作流 Skill
  scripts/                            会话、门控、评估与图表脚本
  references/                         研究与写作规则
  tests/                              回归测试
```

更多实现细节见 [`ARCHITECTURE.md`](plugins/deep-research/ARCHITECTURE.md)。

## 验证

```powershell
cd plugins/deep-research
python -m unittest discover -s tests -v
```

## 许可证

项目采用 [Apache License 2.0](LICENSE)。部分写作规则吸收了 MIT 许可的 Human Writing Skill 1.1.0，完整归属信息见 [`THIRD_PARTY_NOTICES.md`](plugins/deep-research/THIRD_PARTY_NOTICES.md)。
