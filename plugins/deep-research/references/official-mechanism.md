# Official Mechanism Notes

This note records the public mechanism this plugin preserves.

OpenAI documentation describes ChatGPT Deep Research as a three-step process:

1. Clarification: an intermediate model clarifies user intent and gathers context such as preferences, goals, or constraints.
2. Prompt rewriting: an intermediate model produces a more detailed prompt from the original input and clarifications.
3. Deep research: the detailed prompt is passed to the deep research model.

The same documentation says Deep Research via the Responses API does not include clarification or prompt rewriting by default. Developers can add those steps because the model expects a fully formed prompt before it starts researching.

Primary official source:

- https://developers.openai.com/api/docs/guides/deep-research#prompting-deep-research-models

Related official cookbook entry found by the OpenAI docs search index:

- https://developers.openai.com/cookbook/examples/deep_research_api/introduction_to_deep_research_api#clarifying-questions-in-chatgpt-vs-the-deep-research-api

Implementation boundary:

- This plugin is a workflow wrapper for Codex.
- It does not reproduce private ChatGPT product code, hidden prompts, entitlement behavior, or internal orchestration.
- It intentionally implements only the documented interaction pattern.

## Product Behavior Observation

The useful older interaction pattern was not only "search more sources." It was a brief negotiation:

1. The user gave a draft intent.
2. The assistant asked about style, article type, spoiler/detail level, target audience, and focus.
3. The user answered.
4. The assistant confirmed the article shape in natural language.
5. Research and writing started from that confirmed shape.

The weaker newer task-card pattern is:

1. The user gives a short topic.
2. The system creates a generic task list.
3. The user can edit or start.
4. Research proceeds with inferred assumptions.

For long-form writing, the plugin should prefer the older brief negotiation pattern.
