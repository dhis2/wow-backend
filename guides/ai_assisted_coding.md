# Guidelines for AI-assisted development

## Why introduce guidelines?

DHIS2 allows using coding agents as part of project development. After several months of use, it has become obvious that we need some guidelines to maintain valuable human interactions and attempt to integrate AI code successfully. Some byproducts of AI use can be:
- overly-lengthy text descriptions
- text descriptions ___can be___ harder to comprehend vs someone's own thoughts
- code that may not be fully understood by the human author
- code that may not fit in with project direction/patterns/guidelines
- communicating with collegues through AI
- not being considerate to fellow colleagues

These guidelines should be treated as a living document. They can be updated/debated as new behaviours emerge and existing behaviours change over time.

Initial guideline categories cover aspects like:
- `Language`
    - words used
    - scope
    - meaning
    - structure
- `Code`
    - comprehension of produced code
    - relevance of produced code
    - bloat
    - project compatibility (style, convention, patterns etc.)
- `Human Interaction`
    - consideration for fellow colleagues
    - keeping meaningful/valuable human interactions

## Guidelines

### Language
1. Text produced by AI should be fully understandable and easy to read. Some examples:
    - PR descriptions
    - Jira issues (features, bugs)
    - code comments

   If the text looks too wordy or convoluted, use your judgement and edit until it:
    - reads more easily
    - is clearer
    - is more concise

### Code
1. Code produced **must** be fully understood by the author. The author should be able to:
    - explain what the code does
    - answer any questions about the code
    - defend/advocate why the code is warranted
2. Code produced should align with project direction/patterns

3. New patterns/approaches should benefit and fit in with the project. They should:
    - help long-term vision
    - ideally not be one-off hacks

### Human Interaction
1. Do not dump AI output onto a colleague. This may be from an AI code review or a bug report. Try to:
    - understand it (where possible)
    - filter out false positives before sending on
    - filter out noise/unnecessary text
    - confirm/reproduce its assertions/theories/claims

2. Keep human-to-human communication where relevant/valuable
    - PR comments/responses
    - Jira issue comments/responses
    - Slack messages

## Can any of this be automated?

Some of the guidelines could ___potentially___ be automated which would make things easier e.g. Experiment with agent config/tools to get closer to a desired output for `Language` & `Code` topics.
