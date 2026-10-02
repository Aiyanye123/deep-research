# Official Mechanism Notes

This note records public descriptions that informed the plugin. They are not a
required internal architecture for this local workflow.

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
- Its opening inquiry and research choices are locally authored; they may go
  beyond the public interaction description without claiming access to private code.

## Local Interaction Choices

Opening questions are required unless explicitly waived. They help discover
deeper assumptions and wider directions as well as clarify practical constraints.
Wait for answers, briefly confirm the chosen direction, and then research and
write with judgment. No fixed negotiation rounds or task-card sequence is required.
Every completed written deliverable receives a final prose review and polish.
