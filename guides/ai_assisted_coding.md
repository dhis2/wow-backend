# Guidelines for AI-Assisted Development

## Why Introduce Guidelines?

DHIS2 uses AI as part of project development. After several months of use, it has become clear that we need some guidelines to maintain valuable human interactions and ensure that AI-generated code is integrated successfully. AI-assisted development can introduce issues such as:
- overly long text descriptions
- text that can obscure the author's intended meaning or actual thoughts
- code that may not be fully understood by the human author
- code that may not fit in with project direction/patterns/guidelines
- replacing meaningful communication with colleagues
- being less considerate to colleagues

The `platform-backend` team is adopting these guidelines to start with. These guidelines should be treated as a living document. They can be updated/debated as new behaviours emerge and existing behaviours change over time.

## Guidelines

**Guiding principle:** AI should assist, not replace, human judgement or ownership.

### Text
1. Text drafted with AI should be clear, concise and understandable to its intended audience. This includes, for example:
    - PR descriptions
    - Jira issues (features, bugs)
    - code comments

   If the text is unnecessarily wordy or convoluted, use your judgement and edit it to make it clearer and more concise.
2. Text should communicate the author's intended meaning and not the AI's explanation of its own process.

### Code
1. AI-generated code **must** be reviewed and fully understood by the author before it is committed. The author should be able to:
    - explain what the code does
    - answer any questions about the code
    - explain and justify why the code is needed
2. AI-generated code should follow existing project patterns, conventions and architectural direction.
3. New patterns or approaches should only be introduced when they provide a clear long-term benefit to the project.
4. Avoid unnecessary code, abstractions, dependencies and complexity. Solutions should be no more complex than necessary to solve the problem.

### Human Interaction
1. Your productivity gains land in someone else's review queue. More PRs, bigger diffs and more discussion all fall on colleagues. Factor in their time, not just yours.
2. Do not pass AI-generated output directly to a colleague without reviewing it first. This may be from an AI code review or for a bug report. Before sharing, the author should:
    - understand it
    - filter out false positives
    - remove noise and unnecessary text
    - verify or reproduce its claims
3. The author should take ownership of the message and communicate the conclusion in their own words.
4. Post your own messages, PR comments, Jira comments, Slack (whether you're starting a thread or replying). Drafting with AI is fine, wiring up an agent to post or reply for you is not.