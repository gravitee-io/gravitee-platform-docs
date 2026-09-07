---
hidden: false
noIndex: false
description: Migrate an API estate from a legacy gateway to Gravitee API Management with the migration agent skill. Follow the steps to convert and reconcile it.
---

# Migrate an API estate to Gravitee

## Overview

* **Outcome.** Every API from a source gateway runs in Gravitee API Management, with its consumers subscribed and its behavior reconciled against the original gateway.
* **Use this when.** You are moving an estate off Kong, Apigee, MuleSoft Anypoint, Azure API Management, AWS API Gateway, WSO2, IBM API Connect, Layer 7, LiteLLM, or OpenRouter.
* **Not covered here.** Why the method works and what it refuses to convert, in [Migrate from another gateway](migrate-from-another-gateway.md). Per-gateway paths, syntax, and coverage, in the [source gateway reference](source-gateway-reference.md). DNS and hostname changes, which are planned outside this guide.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* A Gravitee environment you can create APIs in, and a Management API token for it.
* Read access to the source gateway's management or admin API.
* An upstream that both gateways can proxy, for the reconciliation run.
* Custom API keys enabled at the environment level, if you intend to reuse consumer credentials.
* Agreement from your security reviewer on where the agent runs and what it retains.

## Migrate the estate

To migrate the estate, complete the following steps:

1. [Inventory the Gravitee environment](#inventory-the-gravitee-environment)
2. [Export the source estate](#export-the-source-estate)
3. [Migrate one API by hand](#migrate-one-api-by-hand)
4. [Generate the remaining APIs as drafts](#generate-the-remaining-apis-as-drafts)
5. [Validate every expression](#validate-every-expression)
6. [Carry the consumers across](#carry-the-consumers-across)
7. [Reconcile both gateways](#reconcile-both-gateways)

### Inventory the Gravitee environment

To establish what generated APIs must reference rather than duplicate, complete the following steps:

1. List the existing APIs, dictionaries, shared policy groups, resources, and plans in the target environment.
2. Retrieve the installed policy list. Treat it as the allowed vocabulary for generation.
3. Record the result. Every name a generated API refers to is resolved against this inventory.

{% hint style="warning" %}
A policy that is not installed fails at deploy time with an error that reads like a definition error. `basic-authentication` is not present on a stock install, and `javascript` is not a Gravitee policy at all.
{% endhint %}

Much of the configuration surface is on the v1 Management API path even where APIs and plans are on v2. For which path serves which object, see the [source gateway reference](source-gateway-reference.md#management-api-paths).

#### Verification

To confirm the inventory is complete, complete the following steps:

1. Confirm the installed policy list contains every policy the migration intends to generate.
2. Confirm every dictionary, shared policy group, and resource the mapping will reference appears in the inventory.

### Export the source estate

To capture the whole of the source estate, complete the following steps:

1. Export the API definitions from the source gateway.
2. Export the objects that hold behavior no API definition contains, such as global policies, product-level quota, and application-level throttling. For where these live on each gateway, see the [source gateway reference](source-gateway-reference.md#where-the-invisible-layer-lives).
3. Confirm the export is complete rather than the platform's default representation. On Apigee, only the full bundle format is a complete statement of a proxy.

Every export this step requires is read-only, and none require an admin credential to be handed over. Where the platform has an authenticated CLI, the agent uses your team's existing session.

#### Verification

To confirm the export is usable, complete the following steps:

1. Confirm the export includes the objects that hold behavior outside the API definitions.
2. On Apigee, confirm each proxy exported in the full bundle format, and read the step lists for execution order rather than the file order in the bundle.

### Migrate one API by hand

To produce the mapping the rest of the estate is generated from, complete the following steps:

1. Pick an API that is representative rather than easy.
2. Convert it and attach the equivalent Gravitee policies.
3. Add the global layer as its own flow. Keep it separate from the individual APIs rather than folding a copy into each one.
4. Replay the requests the owning team cares about through both gateways, including the requests that are supposed to fail.
5. Obtain explicit sign-off on the API's behavior, not on its configuration.
6. Record the construct-to-policy mapping that the signed-off pair demonstrates.

#### Verification

To confirm the mapping is sound, complete the following steps:

1. Confirm the owning team has signed off on the API's behavior.
2. Confirm the recorded mapping covers every construct the source export contains.

### Generate the remaining APIs as drafts

To convert the rest of the estate, complete the following steps:

1. Apply the recorded mapping to each remaining export.
2. Resolve every name the generated definitions refer to against the environment inventory.
3. Validate the context paths before you submit a batch. A single invalid context path blocks an entire import run.
4. Import the APIs and leave every one of them in draft.

{% hint style="warning" %}
Keep every generated API in draft until its reconciliation has passed. An API that is deployed before it is checked is an API somebody can route traffic to.
{% endhint %}

#### Verification

To confirm the batch imported correctly, complete the following steps:

1. Confirm every export produced a corresponding API.
2. Confirm no generated API is deployed.

### Validate every expression

To confirm the generated controls run, complete the following steps:

1. Check every generated Expression Language reference against the [syntax reference](source-gateway-reference.md#expression-language-syntax).
2. Confirm each reference resolves against an object the environment inventory proved exists.
3. Guard anything that may be absent, and terminate every expression in a non-null fallback.
4. Confirm that no source-gateway condition syntax remains in any Gravitee condition.
5. Confirm that `#request.content` is referenced only by content-aware policies. A policy that has not declared it reads null.
6. Parse-check every Groovy script before import. Gravitee does not compile-check Groovy at import or at deploy.

{% hint style="danger" %}
None of these failures raise an error. An expression that resolves to nothing evaluates to null, the policy does nothing, and the API returns 200. See [Failures are silent by default](migrate-from-another-gateway.md#failures-are-silent-by-default).
{% endhint %}

#### Verification

To confirm no expression is inert, complete the following steps:

1. Confirm every expression resolves against an object the environment inventory proved exists.
2. Confirm every Groovy script parses outside Gravitee.

### Carry the consumers across

To move consumers without reissuing their credentials, complete the following steps:

1. Enable custom API keys at the environment level, through the environment settings endpoint. Without this you receive `You are not allowed to provide a custom API Key`.
2. Create the plans.
3. Create one subscription per source application.
4. Where the source gateway exports usable credentials, pass the application's real key as the API key. Read credentials from the single-application endpoint rather than the collection endpoint. For which gateways export credentials, see the [source gateway reference](source-gateway-reference.md#credential-export).
5. Match the API key header. Set `portal.apikeyHeader` for the environment, or add a `transform-headers` step.
6. Wait for the subscription to sync before you test it. The API Gateway answers 401 until it does, typically for about fifteen seconds.

{% hint style="info" %}
Under external client management, where an organization issues credentials through an outside identity provider, the secret is held by that provider rather than by the gateway. Confirm which model the customer uses before you promise that credentials carry across.
{% endhint %}

#### Verification

To confirm a migrated consumer works, complete the following steps:

1. Send a request with the consumer's original key, and confirm the API returns 200.
2. Send a request with no key, and confirm the API returns 401.
3. Send a request with an incorrect key, and confirm the API returns 401.

### Reconcile both gateways

To establish that behavior matches, complete the following steps:

1. Point both gateways at the same upstream.
2. Replay your own cases against each gateway. Include every case that is supposed to fail.
3. Compare status, headers, and body for each case.
4. Retry any 404 that carries the text `No context-path matches the request URI`. That wording means the route has not deployed yet. Retrying on the status code alone masks a genuine 404.
5. Classify each divergence as accepted or real. An accepted divergence is one you expect and do not treat as a defect, such as a timestamp or a request ID.
6. Report the run as four figures: probes, matched, accepted divergences, and real divergences.

#### Verification

To confirm the reconciliation is sound, complete the following steps:

1. Confirm the run includes every negative case the source gateway rejects.
2. Confirm each divergence is classified as accepted or real.

## Verification

To confirm that the migration as a whole succeeded, complete the following steps:

1. Confirm that probes equals matched plus accepted divergences plus real divergences, for every source gateway in scope.
2. Confirm every real divergence has a named owner and a recorded decision.
3. Confirm every refused construct is reported with the API it sits on and the decision it still needs.
4. Confirm no API is deployed that has not passed its reconciliation.

## Next steps

* [Migrate from another gateway](migrate-from-another-gateway.md "mention")
* [Source gateway reference](source-gateway-reference.md "mention")
* [Secure your API proxy](../build/secure-your-api-proxy.md "mention")
