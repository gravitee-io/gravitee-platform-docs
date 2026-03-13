# GKO 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:GKO-2024 -->
#### **LLM Analytics and Dashboard**

* Introduces environment-level monitoring of LLM proxy usage with two computed metrics: total token count (`LLM_PROMPT_TOTAL_TOKEN`) and total cost (`LLM_PROMPT_TOKEN_COST`), supporting `COUNT` and `AVG` measures.
* Adds provider and model filtering via `LLM_PROXY_MODEL` and `LLM_PROXY_PROVIDER` dimensions, enabling platform teams to track AI usage, control costs, and audit LLM access across APIs.
* Includes a pre-configured LLM dashboard template with 10 widgets tracking request volume, token consumption, cost evolution, and response status distribution.
* Requires the new analytics engine enabled and Elasticsearch backend storing `additional-metrics` fields for LLM token and cost data.
<!-- /PIPELINE:GKO-2024 -->

## Improvements

## Bug Fixes
