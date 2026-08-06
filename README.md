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

- **动态澄清**：至少提出 3 个问题，但不设固定上限；问题由选题中的真实不确定性生成，不使用“字数、平台、文风、引用格式”固定问卷。
- **多波次研究**：把检索分为定位、扩展、反证、缺口补全和核验等阶段，阻止模型只搜索几个网页就收尾。
- **动态证据门**：来源数量不是唯一目标。插件同时检查来源质量、信息增量、关键论断覆盖、反方材料和未解决缺口。
- **持久研究会话**：查询、来源、论断、文本锚点、缺口和阶段状态都会写入文件，可在上下文压缩或新任务中继续。
- **原创洞见**：在写作前区分材料共识、现有解释、反向解读与作者自己的论证，避免机械拼接网页摘要。
- **长文连续性**：通过提纲、章节证据分配与 continuity notes 维持术语、论证和章节衔接。
- **中英文润色**：中文按文章类型选择评论性、正式或技术配置；英文使用独立通用规则，不套用中文句式限制。
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
| `prose-humanizer` | 文章类型导向的中英文润色 |

主 Skill 会按固定阶段调用其余六个 Skill，并通过 `workflow-gate` 检查是否有阶段被遗漏。

## 中文写作配置

中文成稿不会按知乎、公众号或 Bangumi 等平台套用固定文风，而是根据内容和文体选择：

- `essayistic`：文学文化批评、评论、专栏、公共写作和叙事性非虚构
- `formal`：学术、政策、法律、金融、市场和机构型报告
- `technical`：工程、标准、方法、规范与技术说明

中文检查器只把模型自述、聊天结尾等高置信残留判为失败。冒号、破折号、第一人称、转折和专业术语不会被机械删除。直接引语、参考文献、链接、表格、图注、代码、名称和数字受到保护。

## 研究深度

插件提供 `light`、`standard`、`deep` 和 `exhaustive` 四种配置，但使用动态目标而不是简单凑来源数。当前 `exhaustive` 配置的合格来源下限为 24、证据价值下限为 65 单位、动态来源目标为 100；只有完成来源通道、反证、核验和信息饱和检查后，才可能低于动态目标停止。稀缺、权威、深入阅读且能覆盖关键论断的材料可以获得更高证据价值，低质量聚合页、重复转载和无信息增量的页面不能用来填数。

## 会话与评估

严重研究任务会在独立目录中保存 `brief.md`、研究计划、来源与论断账本、文本锚点、提纲、原始研究稿和最终审计结果。即使 Codex 发生上下文压缩，也可以通过会话文件继续，而不是依赖聊天记忆。

运行结构化评估：

```powershell
python plugins/deep-research/scripts/evaluate_run.py --session <研究会话目录>
```

运行中文文风检查：

```powershell
python plugins/deep-research/scripts/check_chinese_prose.py <稿件.md> --profile essayistic
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

项目采用 [Apache License 2.0](LICENSE)。部分中文写作规则吸收了 MIT 许可的 Human Writing Skill 1.1.0，完整归属信息见 [`THIRD_PARTY_NOTICES.md`](plugins/deep-research/THIRD_PARTY_NOTICES.md)。
