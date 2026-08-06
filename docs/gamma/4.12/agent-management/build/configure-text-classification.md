---
hidden: false
noIndex: false
description: >-
  Configure the AI - Prompt Guard Rails policy against a text classification
  model, set the sensitivity threshold, choose whether to block or log, and tune
  the result.
---

# Configure text classification

The **AI - Prompt Guard Rails** policy screens prompts with a text classification model. This page covers the policy's settings and how to tune them. For choosing which model sits behind it, see [Select a text classification model](select-a-text-classification-model.md).

## Policy settings

The policy is attached in the LLM Studio, on the request phase. See [Configure an LLM Proxy](configure-an-llm-proxy.md) for the steps to add a policy to a flow.

| Setting | Description | Default |
| --- | --- | --- |
| **Resource Name** | The AI Model Text Classification resource that loads the model. Required — without it the policy fails rather than passing the prompt through | - |
| **Prompt preset** | **All prompts (for LLM APIs)** screens every prompt in the request. **Custom prompt (for none LLM APIs)** screens a value you point at with **Prompt Location** | `ALL_PROMPTS` |
| **Prompt Location** | Where to read the text from, when **Prompt preset** is set to the custom option | - |
| **Content Checks** | A comma-separated list of model labels to act on, for example `TOXIC,OBSCENE`. Leave it empty to match every label the model emits | Empty, so all labels |
| **Sensitivity threshold** | The minimum classification score that counts as a match | `0.8` |
| **Request Policy** | **Block request** rejects a matching request. **Log request** records it and lets it through | `LOG_REQUEST` |

{% hint style="warning" %}
The valid values for **Content Checks** are the labels your selected model emits, and they aren't shared across models. A label the running model never emits produces a filter that silently never matches. The label sets are listed in [Select a text classification model](select-a-text-classification-model.md).
{% endhint %}

## Start in log mode

**Request Policy** defaults to **Log request** for a reason. A guardrail that blocks traffic on its first day blocks legitimate prompts along with the rest, and you have no baseline to tell the two apart.

Run the policy in log mode first, watch what it flags on real traffic, and tune the threshold and the label list against that. Switch to **Block request** once the flagged set looks right.

## Tune the sensitivity threshold

The **Sensitivity threshold** is the confidence score a classification must reach before the policy acts on it. It trades two failure modes against each other:

* **A higher threshold acts less often.** Fewer legitimate prompts are caught by mistake, and more genuinely harmful ones get through.
* **A lower threshold acts more often.** Fewer harmful prompts get through, and more legitimate ones are blocked or logged.

Neither direction is safe by default. Which error costs you more depends on what sits behind the proxy, so tune the threshold on your own traffic rather than adopting a number from elsewhere.

## Watch accuracy per language

Model accuracy varies sharply by language — the same model can score above 0.94 on English and below 0.55 on a low-resource language. If quality degrades for a particular language, moving up the BERT family, from Tiny to Mini to Small to DistilBERT Multilingual, generally improves it. If latency is the problem instead, move down.

The per-language F1 scores for the binary models are in [Select a text classification model](select-a-text-classification-model.md).

## Known limitations

The limitations below are properties of the models themselves and apply wherever the resource runs:

* **Llama Prompt Guard 2 86M.** In the optimized build Gravitee ships, accuracy degrades against the 22M variant, at recall `0.80` and AUC-ROC `0.75`. Use the 22M variant.
* **Llama Prompt Guard 2, both variants.** A 512-token context window, so longer prompts need segmenting. Both focus on explicit attacks and don't reliably catch subtle or novel techniques. Meta recommends domain-specific fine-tuning for production use.
* **BERT Tiny Toxicity.** The lowest accuracy of the BERT family, and a wide gap between English at `0.94` and low-resource languages, with Hebrew at `0.51`.
* **BERT Mini Toxicity.** Hebrew scores `0.41`, below BERT Tiny. Some languages show overfitting, with a train-eval gap up to `0.11`.
* **BERT Small Toxicity.** Overfits on Spanish, Italian, and Hindi.
* **DistilBERT Multilingual Toxicity.** Binary classification only, with F1 from `0.62` to `0.96`. Weaker on Hebrew, Amharic, and Chinese.
* **Detoxify ONNX.** The largest model at 300M parameters, with the highest memory use and latency. Covers 7 languages, without Arabic, Chinese, Hindi, Japanese, or German.
* **MiniLMv2 Toxic Jigsaw.** English only. Trained on Wikipedia talk pages, so it doesn't reliably generalize to social media, code, or technical content.
* **All binary models.** No fine-grained toxicity categories — the answer is toxic or not toxic.
* **All multi-label models.** Thresholds need tuning per label for good precision and recall.

## Next steps

* [Select a text classification model](select-a-text-classification-model.md). Compare the eight models before you commit to one.
* [AI resources](ai-resources.md). Understand how the gateway loads and shares the model.
* [Configure an LLM Proxy](configure-an-llm-proxy.md). Attach the policy to a flow.
