---
hidden: false
noIndex: false
description: Design an LLM Proxy with guardrails, token rate limiting, text classification, and runtime model overrides. Pick the setting you want to configure.
---

# Design

The Design group of an LLM Proxy controls the models it reaches and the policies it applies to the traffic it carries.

* [**Configure an LLM Proxy**](../../configure-an-llm-proxy.md): Configure guardrails, PII filtering, rate limiting, security plans, and structured output.
* [**Add the Token Rate Limit policy**](../../add-the-token-rate-limit-policy.md): Cap the tokens a consumer spends over a rolling period.
* [**Configure text classification**](../../configure-text-classification.md): Set the AI - Prompt Guard Rails policy sensitivity threshold, and choose whether to block or log.
* [**Select a text classification model**](../../select-a-text-classification-model.md): Compare the text classification models on accuracy, languages, and labels.
* [**Override the model at runtime**](../../override-the-model-at-runtime.md): Route a request to a different model than the client asked for by setting a context attribute on a flow.
