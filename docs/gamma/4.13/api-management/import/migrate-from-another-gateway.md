---
hidden: false
noIndex: false
description: Migrate an API estate from Kong, Apigee, MuleSoft, or Azure to Gravitee API Management. Learn how the method works and what it refuses to convert.
---

# Migrate from another gateway

A migration from a legacy gateway to Gravitee is a conversion, not a copy. Each source gateway expresses authentication, rate limiting, and transformation in its own constructs, and only some of those have a faithful Gravitee equivalent. This article explains the method Gravitee uses to make that conversion auditable, and the failure modes it is built to catch.

To perform a migration, see [Migrate an API estate to Gravitee](migrate-an-api-estate-to-gravitee.md).

## Overview

The migration is driven by the `gravitee-migration` agent skill, a set of Markdown instructions that an AI coding agent loads into context. One file holds the source-agnostic method. Each source gateway has its own reference file holding that gateway's construct vocabulary. There is nothing to install and nothing to deploy.

The following division of labor matters more than the tooling:

* **The agent generates and validates.** It reads the source export, applies a mapping, emits API definitions, and checks every expression it produced.
* **You decide.** You pick the API the mapping is derived from, you confirm that its behavior is correct, and you own the pass criteria for the final reconciliation.

The agent never establishes on its own that a migration is correct. It establishes that the estate matches a mapping you approved.

## How it works

### The mapping comes from one signed-off API

Rather than converting an estate against a mapping table written in advance, the method derives the table from a worked example.

You migrate one representative API by hand and put it in front of the team that owns it. They confirm the behavior, not the configuration. That produces a matched pair: the source export, and a Gravitee API you have agreed is correct. The construct-to-Policy mapping that pair demonstrates becomes the migration context for everything that follows.

The mapping is therefore proven against real traffic before it is applied at scale, and every generated API traces back to a decision a named person made.

### Every source gateway has an invisible layer

No API-by-API export is a complete statement of an estate's behavior. The following gateways each enforce something outside the API definition, applied to APIs that never mention it:

* MuleSoft Anypoint applies automated policies org-wide.
* Apigee attaches environment flow hooks and grants access through operation groups.
* Azure API Management has global policy and product policy.
* Kong has global plugins, WSO2 has application-level throttling, and LiteLLM has an estate-wide budget.

If you migrate only what the API export contains, the result is an estate that looks complete and enforces less than the original. The invisible layer has to be exported alongside the API definitions. It is then migrated as its own flow, rather than folded as a copy into every API.

For where it lives on each gateway, see the [source gateway reference](source-gateway-reference.md).

### Failures are silent by default

The method insists on validation and reconciliation because the characteristic migration defect raises no error anywhere. The following failures are all silent:

* **An Expression Language reference that resolves to nothing does not fail.** It evaluates to null, the Policy does nothing at all, and the API returns 200. The control you migrated is not running, and nothing in the logs says so.
* **Source-gateway condition syntax left in a Gravitee condition behaves the same way.** It resolves to nothing, and the API stops rejecting what it used to reject.
* **Groovy is not compile-checked at import or at deploy.** A script that does not parse imports cleanly, deploys, shows as started, and returns the same bare 500 as one that threw at runtime.

A migration can import, deploy, report success, and be wrong. That is why the estate is generated as drafts, and every expression is checked against an inventory taken beforehand. Both gateways are then replayed against the same upstream before anything is published.

### Widening is more dangerous than narrowing

In every estate Gravitee has diffed, the first pass produced at least one migrated API that accepted a request the original rejected. The cause is usually a missing required field, an unmatched path, or a guard branch with no equivalent.

The asymmetry is what makes this worth stating. An API that has become **stricter** than the original generates support tickets within a day. An API that has become **more permissive** generates nothing at all, which is why the reconciliation has to include the cases that are supposed to fail.

Reconciliation results are reported as four figures rather than a percentage: probes, matched, accepted divergences, and real divergences. An accepted divergence is one you expect and do not treat as a defect, such as a timestamp or a request ID.

## Why some constructs have no conversion

A small number of constructs are refused by name rather than converted. The principle is that a plausible conversion is worse than no conversion, because it produces a migration that imports, deploys, reports success, and does the wrong thing.

The following constructs are refused:

| Construct | Why there is no conversion |
| --- | --- |
| AWS usage-plan quotas | Metered per API key over a rolling period tied to a billing construct with no Gravitee counterpart. The same number would enforce something different. |
| Per-model cost budgets in an AI gateway | The conversion depends on per-model pricing that changes without notice, so a converted limit stops being the limit that was set. |
| Source-gateway transformation languages, beyond the translatable subset | Anything not translatable is emitted as a named item together with the API it sits on. |

Each refusal is reported as the construct, the API it sits on, and the decision you still owe.

## How mappings are marked

Every mapping in a per-source reference carries one of the following evidence markings:

* **Verified.** The mapping was exercised against a live instance of the source gateway and compared on the wire.
* **Unverified.** The mapping is well-founded, but the tested estate contained no example of it, so it was never exercised.

An unverified mapping is a starting point for a scoping conversation, not a measured fact. When a customer asks whether a construct converts, say which of the two you are quoting.

## Scoping a MuleSoft migration

Anypoint splits an API across the following two artifacts, and which one is in scope changes an estimate more than anything else on this page:

* **The API Manager instance.** This holds endpoint configuration and applied policies, and it is what Gravitee replaces.
* **The Mule application.** This holds flows, connector operations, and DataWeave transformations, and it is integration logic.

That yields the following two projects:

* **Gateway-only exit.** You drop Anypoint and keep the Mule runtime. The Mule application becomes an upstream that Gravitee points at, and DataWeave is never touched.
* **Full MuleSoft exit.** The same application is a rebuild, and not one Gravitee performs. Gravitee is an API gateway, not an iPaaS.

Where transformations do have to move, a fixed corpus of 354 real DataWeave transformations was measured. Of those, 59% were refused outright. The remainder split between trivial translations, structural translations, and files that were not transformations at all.

## Data handling

The agent reads your exported source configuration, and on some platforms that export contains consumer credentials.

Where the agent runs, what it retains, and whether it uses a model endpoint inside your own network boundary are your decisions. The skills are Markdown, and the exports stay on infrastructure you control. Agree the arrangement with your security reviewer before you point the agent at a production estate.

## Next steps

* [Migrate an API estate to Gravitee](migrate-an-api-estate-to-gravitee.md "mention")
* [Source gateway reference](source-gateway-reference.md "mention")
