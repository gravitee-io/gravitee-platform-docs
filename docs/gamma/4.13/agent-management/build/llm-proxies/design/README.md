---
hidden: false
noIndex: false
description: Design an LLM Proxy with entrypoints, guardrails, rate limiting, text classification, and runtime model overrides. Pick the setting you want to configure.
---

# Design

The Design group of an LLM Proxy controls the paths it answers on, the models it reaches, and the policies it applies to the traffic it carries.

* [**Configure LLM Proxy entrypoints**](../../configure-llm-proxy-entrypoints.md). Change the context paths consumers call, switch to virtual hosts, and edit the entrypoint plugin options.
* [**Add the Token Rate Limit policy**](../../add-the-token-rate-limit-policy.md). Cap the tokens a consumer spends over a rolling period.
* [**Add the Cost Rate Limit policy**](../../add-the-cost-rate-limit-policy.md). Cap what a consumer spends in dollars over a period.
* [**Select a text classification model**](../../select-a-text-classification-model.md). Compare the text classification models on accuracy, languages, and labels.
* [**Configure text classification**](../../configure-text-classification.md). Set the AI - Prompt Guard Rails policy sensitivity threshold, and choose whether to block or log.
* [**Override the model at runtime**](../../override-the-model-at-runtime.md). Route a request to a different model than the client asked for by setting a context attribute on a flow.
