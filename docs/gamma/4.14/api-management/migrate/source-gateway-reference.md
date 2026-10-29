---
hidden: false
noIndex: false
description: Source gateway migration reference for Gravitee API Management, covering Management API paths, Expression Language syntax, and credential export.
---

# Source gateway reference

This page is the lookup reference for a gateway migration. For the method, see [Migrate an API estate to Gravitee](migrate-an-api-estate-to-gravitee.md). For why the method is shaped the way it is, see [Plan a gateway migration](plan-a-gateway-migration.md).

{% hint style="info" %}
The mappings and coverage on this page were verified against API Management 4.12.x.
{% endhint %}

## Management API paths

Much of the configuration surface is on the v1 path even where APIs and plans are on v2. If a v2 route returns 404, try the v1 form. The following table lists the path version that serves each object:

| Purpose | Path version |
| --- | --- |
| List and create APIs, plans, subscriptions | v2 |
| Deploy an API | v2 |
| Shared policy groups | v2 |
| Dictionaries | v1, under `/configuration/dictionaries` |
| Installed policy list | v1 |
| Resources | v1 |

There is no environment `variables` collection. Environment-scoped values are dictionaries, and per-consumer values are subscription metadata.

The API key header defaults to `X-Gravitee-Api-Key`. Change it for the environment with the `portal.apikeyHeader` setting, or add a `transform-headers` step to the API.

## Expression Language syntax

The following table contrasts the Expression Language forms Gravitee accepts with the forms that are commonly written by mistake:

| Valid | Not valid |
| --- | --- |
| `{#context.attributes['name']}` | `#context.variables` |
| `{#dictionaries['dictName']['key']}` | `#context.dictionaries` |
| `{#request.headers['X'][0]}` | |
| `{#response.status}` | |
| `{#request.content}` | |

The following rules apply to every generated expression:

* Guard anything that might be absent, and terminate every expression in a non-null fallback.
* `#request.content` is populated only for content-aware policies. A policy that has not declared it reads null.
* Source-gateway condition syntax left in a Gravitee condition does not error. It resolves to nothing, and the API stops rejecting what it used to reject.
* Gravitee does not compile-check Groovy at import or at deploy. A script that does not parse imports, deploys, shows as started, and returns the same bare 500 as one that threw.

## Where the invisible layer lives

The following table lists where each source gateway holds behavior that no API export contains:

| Source gateway | Where the invisible layer lives |
| --- | --- |
| MuleSoft Anypoint | Automated policies, applied org-wide |
| Apigee X and Apigee Edge | Environment flow hooks, product-level quota, access granted through operation groups |
| Azure API Management | Global policy and product policy |
| WSO2 API Manager | Application-level throttling |
| Kong | Global plugins |
| LiteLLM | Estate-wide budget |
| IBM API Connect | Catalog-level and product-level assembly |
| AWS API Gateway | Usage plans and stage-level settings |

## Credential export

The following table states whether each source gateway's consumer credentials can be read and reused as Gravitee API keys:

| Source gateway | Do credentials export? |
| --- | --- |
| Apigee X | Yes. Consumer key and secret both export in full. Verified: no key 401, wrong key 401, original key 200. |
| AWS API Gateway | Yes. The key value exports and is accepted verbatim. |
| MuleSoft Anypoint | Yes. `GET /exchange/api/v2/organizations/{orgId}/applications/{appId}` returns `clientSecret`, as does the `apiplatform/repository/v2` equivalent. Verified against a live organization as organization owner, September 3, 2026. |
| WSO2 API Manager | Partly. The secret is readable, but the key manager that issues its tokens leaves with the gateway. Ask about both. |
| LiteLLM | No. The secret is write-only after creation, so every consumer is reissued. |

{% hint style="warning" %}
Read credentials from the single-application endpoint, not from the collection endpoint. On more than one platform the list response omits the secret while the individual `GET` returns it. A collection response that omits the secret is the most common reason this question is answered wrongly. It is also why the MuleSoft Anypoint secret is widely believed to be write-only.
{% endhint %}

## Evidence and coverage

Two kinds of number appear in the following table, and they answer different questions:

* **Classification.** A classification counts the constructs in a real estate and says what converts.
* **Reconciliation.** A reconciliation replays requests through both gateways and says whether behavior matches. Reconciliation figures are given as probes, matched, accepted divergences, and real divergences.

Kong is currently the only source carrying both. The following table lists the evidence recorded for each source gateway:

| Source gateway | Version tested | Evidence |
| --- | --- | --- |
| Kong, classic and AI | 3.9.1 OSS | Classification: 2 services, 2 routes, 9 plugin instances across 6 distinct plugin names; 8 converted, 1 refused by name. Reconciliation: 15 probes, 15 matched, 0 accepted, 0 real. Enterprise and Konnect constructs are out of scope. |
| AWS API Gateway, REST APIs | Live account | 10 probes, 10 matched, 0 accepted, 0 real |
| WSO2 API Manager | 4.3.0 | 7 probes, 7 matched, 0 accepted, 0 real |
| OpenRouter | Live service | 8 probes, 7 matched, 1 accepted, 0 real |
| IBM API Connect | v12 | 3 probes, 3 matched, 0 accepted, 0 real |
| Azure API Management | Developer tier | 9 probes, 5 matched, 0 accepted, 4 real. Three of the four share one root cause. |
| LiteLLM | 1.90.0 | 22 probes, 8 matched, 12 accepted, 2 real. The two share one root cause. |
| Apigee X | Live organization | Converted, imported, started, credential path verified. No traffic diff. |
| MuleSoft Anypoint | Live organization | Converted, imported, started. Transformations diffed against MuleSoft's own engine. No traffic diff. |
| Layer 7 and CA API Gateway | Gravitee side only | All fourteen target policies confirmed present on a licensed 4.12 install. `xslt` requires the Enterprise Edition. The source image does not start without a license, so the source half is unverified. |

For the constructs that are refused rather than converted, see [Constructs that have no conversion](plan-a-gateway-migration.md#constructs-that-have-no-conversion).

## Next steps

* [Migrate an API estate to Gravitee](migrate-an-api-estate-to-gravitee.md "mention")
* [Plan a gateway migration](plan-a-gateway-migration.md "mention")
