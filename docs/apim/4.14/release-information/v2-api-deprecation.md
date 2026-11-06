---
description: v2 APIs are deprecated from API Management 4.13. Learn the removal timeline, what you need to do, and how to migrate your v2 APIs to v4.
---

# v2 API Deprecation and Migration to v4

## Overview

This page explains the deprecation of v2 APIs in Gravitee API Management (APIM), the timeline for their removal, and how to migrate your v2 APIs to v4.

{% hint style="warning" %}
From 4.13.0 (October 2026), v2 APIs are deprecated. What you need to do depends on how you deploy APIM:

* **Hybrid and Gravitee Cloud:** Migrate your v2 APIs to v4 before September 30, 2027.
* **Self-hosted:** The October 2027 release of APIM removes v2 APIs. You can remain on the last version of APIM that supports v2 APIs through its official support window. For more information, see [Support model](https://documentation.gravitee.io/platform-management/support-model).
{% endhint %}

## What deprecation means

Deprecation is advance notice that Gravitee intends to remove v2 APIs in a future release. Nothing changes for your v2 APIs today:

* v2 APIs continue to run on the Gateway.
* Client applications can still call the v2 APIs that you deployed.
* You can still create, configure, and deploy v2 APIs.
* Gravitee continues to support v2 APIs until the release that removes them.

Deprecation gives you time to plan your migration to v4 APIs before v2 APIs are removed.

## Timeline

The following table shows the key dates for the deprecation and removal of v2 APIs:

| Date               | Milestone                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| October 16, 2025   | APIM 4.9 introduces the v2 to v4 migration tool.                                                   |
| October 2026       | APIM 4.13.0 deprecates v2 APIs.                                                                    |
| September 30, 2027 | Deadline for hybrid and Gravitee Cloud customers to complete the migration of their v2 APIs to v4. |
| October 2027       | The October 2027 release of APIM removes v2 APIs.                                                  |

Migrate your v2 APIs to v4 before you upgrade to the October 2027 release.

The steps that you need to take depend on how you deploy APIM:

* [Hybrid and Gravitee Cloud](v2-api-deprecation.md#hybrid-and-gravitee-cloud)
* [Self-hosted installations](v2-api-deprecation.md#self-hosted-installations)

### Hybrid and Gravitee Cloud

Gravitee upgrades Cloud environments as new releases become available. If you use v2 APIs in a hybrid or Gravitee Cloud deployment, complete your migration to v4 before September 30, 2027, ahead of the October 2027 release.

{% hint style="warning" %}
If you expect that you can't complete your migration before September 30, 2027, contact your Gravitee account manager or customer success manager as early as possible.
{% endhint %}

### Self-hosted installations

If you run a self-hosted installation, you control when you upgrade:

* You can remain on the last version of APIM that supports v2 APIs through its official support window. For more information, see [Support model](https://documentation.gravitee.io/platform-management/support-model).
* Before you upgrade to the October 2027 release, migrate all of your v2 APIs to v4.

Gravitee recommends that you don't wait longer than necessary. Migrating earlier gives you access to the capabilities that are only available with v4 APIs, and leaves time to test your migrated APIs.

## Why Gravitee is removing v2 APIs

v4 is the API definition that Gravitee builds on. Every new capability is delivered for v4 APIs, and the gap between what v2 and v4 APIs can do widens with each release. Bringing all APIs onto a single definition lets Gravitee focus on one execution engine, one Policy Studio, and one set of capabilities.

v4 APIs are also required for Gravitee Gamma, the unified experience in which you manage your APIs, event streams, and agents in one place. Gamma doesn't include v2 APIs. Migrating to v4 is the first step to adopting Gamma without friction. For more information, see the [Gamma documentation](https://documentation.gravitee.io/gamma).

## Benefits of v4 APIs

Migrating to v4 is more than a compliance exercise. v4 APIs give you capabilities that aren't available for v2 APIs:

* **MCP and AI agents.** MCP and agent tooling are built on the v4 API definition. You can expose a v4 API as an MCP server so that AI agents can discover and call it. These capabilities aren't available for v2 APIs. For more information, see [Convert REST APIs to an MCP Server](../ai-agent-management/convert-your-apis-to-mcp-servers.md).
* **Event-driven and asynchronous APIs.** v4 APIs support message APIs, native Kafka APIs, and protocol mediation, in addition to HTTP proxy APIs.
* **A redesigned Policy Studio.** The v4 Policy Studio makes it easier to design flows and apply policies to each phase of an API.
* **Improved observability.** v4 APIs support OpenTelemetry tracing that you turn on for each API, and logs that help you diagnose errors.
* **A more capable execution engine.** v4 APIs run on the reactive execution engine. For example, path parameters are extracted once and shared across all flows, and ambiguous paths are rejected before deployment.
* **Long-term support.** v4 APIs receive all new features and improvements.

For a detailed comparison of the two definitions, see [v2 and v4 API Comparison](../create-and-configure-apis/gravitee-api-definitions/v2-and-v4-api-comparison.md).

## What you need to do

To prepare for the removal of v2 APIs, complete the following steps:

1. **Identify your v2 APIs.** In the APIM Console, the **APIs** page shows the definition version of each API in the **API Type** column.
2. **Plan your migration.** Decide the order in which you migrate your APIs. Start with representative APIs in a non-production environment.
3. **Migrate your APIs.** Use the migration tool to convert each v2 API to a v4 API. For more information, see [How to migrate](v2-api-deprecation.md#how-to-migrate).
4. **Test and deploy.** Test each migrated API, and then deploy it.
5. **Update your automation.** If you manage v2 APIs with the Management API, the Gravitee Kubernetes Operator, Terraform, or CI/CD pipelines, update your definitions and pipelines to use the v4 API definition.

## How to migrate

APIM includes a migration tool that converts a v2 API into a v4 API. The tool is available from APIM 4.9, and it's designed to be reliable and predictable:

* **It checks compatibility first.** Before anything changes, the tool runs a compatibility check against your API.
* **It never produces a partial migration.** If the tool detects an element that it can't migrate, it stops and reports the incompatibilities so that you can fix them.
* **It's reversible.** If the migrated API doesn't work as expected, you can roll back to the v2 API.
* **It preserves your analytics.** The API's pre-migration data remains visible in its analytics dashboard and connection logs. For more information, see [Maintain analytics continuity after migrating v2 APIs to v4](../v2-api-analytics-continuity-after-migration.md).

### Migrate an API in the Console

To migrate a single API, complete the following steps:

1. Enable the **Emulate v4 engine** option for your v2 API, and then deploy the API.
2. From the API's **Info** page, click **Migrate to v4**.
3. Review the results of the compatibility check, and fix any issues that it reports.
4. Start the migration.
5. Test the migrated API with **Debug Mode**, and then deploy it.

For the full procedure, see [Migrate APIs](../create-and-configure-apis/create-apis/migrate-apis.md).

### Migrate APIs in bulk with the Management API

If you have a large number of v2 APIs, you can call the migration tool from the Management API and script the migration of many APIs.

To check whether an API can be migrated without changing it, call the migration endpoint in `DRY_RUN` mode:

```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  "https://<management-api-host>/management/v2/organizations/<orgId>/environments/<envId>/apis/<apiId>/_migrate?mode=DRY_RUN"
```

The response contains the migration `state` of the API and a list of `issues`. The following table describes each state:

| State           | Description                                                                                 |
| --------------- | ------------------------------------------------------------------------------------------- |
| `MIGRATABLE`    | The API is compatible with v4. Returned in `DRY_RUN` mode.                                  |
| `CAN_BE_FORCED` | The API can be migrated, but some settings need attention. Review the issues before you continue. |
| `IMPOSSIBLE`    | The API can't be migrated until you fix the issues that the response lists.                 |
| `MIGRATED`      | The API was migrated to v4.                                                                 |

To migrate the API, call the same endpoint without the `mode` parameter:

```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  "https://<management-api-host>/management/v2/organizations/<orgId>/environments/<envId>/apis/<apiId>/_migrate"
```

To migrate an API that returns the `CAN_BE_FORCED` state, review the issues, and then call the endpoint with `mode=FORCE`.

The caller needs permission to update the API definition. After you migrate an API, test it, and then deploy it to apply the v4 definition to the Gateway.

{% hint style="info" %}
Run the migration in `DRY_RUN` mode across all of your v2 APIs first. The results show you which APIs migrate without changes and which APIs need attention, which helps you plan your migration.
{% endhint %}

## Get help

If you have questions about the deprecation, or if the migration tool reports an incompatibility that you can't resolve, contact your Gravitee account manager, your customer success manager, or [Gravitee Support](https://support.gravitee.io).

## Resources

For more information about v4 APIs and the migration, see the following articles:

* [Migrate APIs](../create-and-configure-apis/create-apis/migrate-apis.md)
* [Maintain analytics continuity after migrating v2 APIs to v4](../v2-api-analytics-continuity-after-migration.md)
* [v2 and v4 API Comparison](../create-and-configure-apis/gravitee-api-definitions/v2-and-v4-api-comparison.md)
* [Breaking Changes and Deprecations](breaking-changes-and-deprecations.md)
* [Migrate from v2 to v4 APIs](https://www.gravitee.io/landing-pages/v2-v4-migration)
* [v2 to v4 Migration: Why MCP and Agents Only Live on v4](https://www.gravitee.io/blog/v2-to-v4-migration-mcp-and-agents-only-live-on-v4)
