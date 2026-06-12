---
description: Release notes
metaLinks:
  alternates:
    - release-notes.md
hidden: true
noIndex: true
---

# Release notes

## 1.0.0

**Terraform Registry:** [gravitee-io/apim](https://registry.terraform.io/providers/gravitee-io/apim/1.0.0)

Version **1.0.0** is the first **Generally Available (GA)** release of the Gravitee APIM Terraform provider.

### Highlights

- **GA support model** for provider **1.0.x** (see [Compatibility & support](#compatibility--support)).
- **Two new managed resources:** `apim_group`, `apim_dictionary` (and matching data sources).
- **New optional attributes** on existing resources (API products, OpenTelemetry logs, console notifications, Kafka plan/listener fields, subscription consumer configuration, etc.).
- **Stricter HRID validation** and removal of **`metadata.hidden`** (see [Breaking changes & migration](#breaking-changes--migration)).

#### APIM version and “new fields”

On APIM **older than 4.12**, the provider still talks to the Automation API, but:

- Attributes that require a newer Management API may be **ignored on apply**, **fail at the API**, or **never appear in read-back**, depending on the field.
- Prefer **pinning** `version = "~> 1.0.0"` only when APIM is **≥ 4.12**, or **omit** new blocks/attributes in `.tf` when running against **4.9 – 4.11**.

### New resources

| Resource | Data source | Description | Examples (Terraform Registry) |
| --- | --- | --- | --- |
| [`apim_group`](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/resources/group) | [`apim_group`](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/data-sources/group) | User groups and member roles per scope | [Simple Group](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_group) |
| [`apim_dictionary`](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/resources/dictionary) | [`apim_dictionary`](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/data-sources/dictionary) | Manual or dynamic dictionaries for gateway properties | [Manual dictionary](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_dictionary-manual) · [Dynamic dictionary](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_dictionary-dynamic) |

Repository mirrors: `examples/use-cases/group-developers/`, `examples/use-cases/dictionary-manual/`, `examples/use-cases/dictionary-dynamic/`.

### New and changed fields (by resource)

Fields below are **new or changed since provider 0.5.x** (last widely used preview line). They are **additive** for Terraform state (no resource `schema_version` upgrade). Minimum APIM versions are indicative—validate against your Automation API deployment.

#### `apim_apiv4` / `apim_apiv4` (data source)

| Attribute path | Type | Min APIM (recommended) | Notes |
| --- | --- | --- | --- |
| `allow_multi_jwt_oauth2_subscriptions` | bool | 4.11+ | JWT/OAuth2 multi-plan subscriptions |
| `allowed_in_api_products` | bool | 4.11+ | HTTP Proxy APIs in API Products |
| `console_notification` | object | 4.11+ | |
| `console_notification.events` | list(string) | 4.11+ | |
| `console_notification.groups` | list(string) | 4.11+ | |
| `analytics.otel_logs` | object | 4.11+ | OpenTelemetry log export |
| `analytics.otel_logs.enabled` | bool | 4.11+ | |
| `analytics.reporter_metrics_enabled` | bool | 4.11+ | |
| `listeners.kafka.port` | number | 4.11+ | Kafka listener port |
| `plans.bootstrap_port` | number | 4.11+ | Kafka-oriented plan fields |
| `plans.broker_range_start` | number | 4.11+ | |
| `plans.broker_range_end` | number | 4.11+ | |
| `type` | string (enum) | 4.11+ | New API type value **`EDGE`** allowed |

**Removed (see migration):** `metadata.hidden`

**Unchanged (large nested areas):** `endpoint_groups`, `flows`, `listeners` (except `kafka.port`), `plans` (except Kafka broker fields), `pages`, `properties`, `members`, `services`, etc.—no other schema path removals since 0.5.x.

Resource reference: [apim_apiv4](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/resources/apiv4)

#### `apim_application` / `apim_application` (data source)

| Attribute path | Change | Notes |
| --- | --- | --- |
| _(no new paths)_ | — | |
| `metadata.hidden` | **Removed** | See migration |
| `settings.tls.client_certificate` | **Deprecated** (unchanged since 0.5.x) | Migrate to `client_certificates` |

Guides: [Simple application](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_application-simple) · [Application with group](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_application-with-group)

Resource reference: [apim_application](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/resources/application)

#### `apim_shared_policy_group` / data source

| Attribute path | Change | Notes |
| --- | --- | --- |
| `api_type` | enum **+ `EDGE`** | New allowed value only |

Resource reference: [apim_shared_policy_group](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/resources/shared_policy_group)

Guides: [SPG on API](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_spg-api) · [SPG rate limit](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_spg-ratelimit)

#### `apim_subscription` / data source

| Attribute path | Type | Min APIM (recommended) | Notes |
| --- | --- | --- | --- |
| `api_keys` | list(object) | 4.11+ | Custom API keys (API Key plans) |
| `api_keys.key` | string | 4.11+ | |
| `api_keys.expire_at` | string | 4.11+ | |
| `consumer_configuration` | object | **4.12+** | Push-plan consumer config |
| `consumer_configuration.channel` | string | **4.12+** | |
| `consumer_configuration.entrypoint_id` | string | **4.12+** | |
| `consumer_configuration.entrypoint_configuration` | string (JSON) | **4.12+** | |

Data source exposes `consumer_configuration` but not `api_keys` (read semantics).

Guides: [Subscription (JWT)](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_subscription) · [Subscription (API Key)](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_subscription-apikey)

Resource reference: [apim_subscription](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/resources/subscription)

#### `apim_group` _(new)_

| Attribute path | Type | Notes |
| --- | --- | --- |
| `hrid`, `name`, `notify_members` | string / bool | |
| `members` | list | |
| `members.source`, `members.source_id` | string | IdP / memory source |
| `members.roles` | map(string) | Scope → role |
| `environment_id`, `organization_id`, `id` | string | `id` computed |

#### `apim_dictionary` _(new)_

| Attribute path | Type | Notes |
| --- | --- | --- |
| `hrid`, `name`, `description`, `type`, `deployed` | various | `MANUAL` or `DYNAMIC` |
| `manual.properties` | map(string) | Manual dictionary entries |
| `dynamic.provider.http` | object | URL, method, headers, JOLT `specification`, etc. |
| `dynamic.trigger.rate`, `dynamic.trigger.unit` | number / string | Poll interval |
| `environment_id`, `organization_id`, `id` | string | |

### Upgrade

```hcl
terraform {
  required_providers {
    apim = {
      source  = "gravitee-io/apim"
      version = "~> 1.0.0"
    }
  }
}
```

Then run:

```bash
terraform init -upgrade
terraform plan
```

Review [Breaking changes & migration](#breaking-changes--migration) before upgrading production workspaces.

### Compatibility & support

Wording follows the style of the platform [support model](https://documentation.gravitee.io/platform-overview/gravitee-platform/support-model) (12-month support per APIM minor).

#### Provider ↔ APIM ↔ Terraform / OpenTofu

| Provider version | APIM version | Capability | Terraform / OpenTofu |
| --- | --- | --- | --- |
| **1.0.x** | **4.12.x** | **Full** — all provider attributes supported against Automation API | **1.9+** / latest OpenTofu ([registry](https://registry.terraform.io/providers/gravitee-io/apim/latest)) |
| **1.0.x** | **4.9.x – 4.11.x** | **Compatible** — existing configurations continue to work; **new 1.0 attributes are not managed** (see [New fields](#new-and-changed-fields-by-resource)) | **1.9+** / latest OpenTofu |
| **0.5.x** | 4.11.x (and 4.10.x / 4.9.x without newest API features) | **Best effort only** — no standard maintenance commitment | 1.9+ / latest |
| **0.4.x** | 4.10.x / 4.9.x | **Best effort only** | 1.10+ / latest |
| **0.3.x and below** | 4.8.x – 4.10.x | **Little to no support** — upgrade strongly recommended | Not part of standard tests |

#### Support policy

| Provider line | Support level |
| --- | --- |
| **1.0.x** | **Standard maintenance** — bug fixes, security patches, and compatibility updates aligned with supported APIM minors. |
| **0.5.x**, **0.4.x** | **Best effort only** — no guarantee of fixes; use only while blocked on migration to **1.0.x**. |

> **Note:** Until the [Terraform documentation page](https://documentation.gravitee.io/apim/terraform) is updated for GA, the preview disclaimer (“tech preview”, “fixes mainly on latest”) applies to **0.x** lines only; **1.0.x** is the supported GA line.


### Breaking changes & migration

Terraform **resource schema version remains 0**. There is **no automatic state upgrade** step in 1.0.0. Migration is **configuration and validation** cleanup plus APIM version alignment.

#### 1. HRID validation (stricter)

**What changed:** `hrid` (and the same pattern on nested HRIDs such as `plans.*.hrid`, `pages.*.hrid`) now must match:

```text
^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$
```

Previously (0.5.x), values could **end with `-` or `_`** (e.g. `my-api-`, `api_v2_`).

**What users see** (example):

```text
Error: Invalid Attribute Value Match

  with apim_apiv4.example,
  on main.tf line 12, in resource "apim_apiv4" "example":
  12:   hrid = "my-api-"

Attribute hrid value must be valid according to the regex pattern:
^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$
```

**Affected resources:** `apim_apiv4`, `apim_application`, `apim_shared_policy_group`, `apim_subscription`, `apim_group`, `apim_dictionary`.

**Migration:**

1. Find HRIDs ending with `-` or `_` (and fix exported HCL if you used [export tutorial](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides/docgen_export-tutorial)).
2. Rename to a suffix that ends with a letter or digit (`my-api-v1`, `api_v2`).
3. Because `hrid` uses **replace-on-change**, expect **destroy + create** for that Gravitee object unless you use a careful import/rename runbook.

**Newly allowed:** HRIDs may **start with a digit** (e.g. `2api`) where the old rule required a leading letter.

#### 2. `metadata.hidden` removed

**What changed:** Nested attribute `metadata.hidden` removed from `apim_apiv4` and `apim_application`.

**What users see:**

- **Usually no Terraform error** if `hidden` remains inside a `metadata { ... }` block. Terraform drops unknown nested object keys before the provider runs ([Terraform type-system behavior](https://github.com/hashicorp/terraform/issues/33570)).
- **Silent behavior change:** `hidden = true` no longer affects the Management API; metadata may appear visible in Console when users expected otherwise.

**Migration:**

- Remove all `hidden = ...` lines from `metadata` blocks (recommended for clarity).
- Update modules and export pipelines; remove from examples such as:

  ```hcl
  metadata {
    hidden = false   # remove — ignored on 1.0.0
    name   = "email-support"
    # ...
  }
  ```

#### 3. Deprecated (not removed in 1.0.0)

| Attribute | Resource | Action |
| --- | --- | --- |
| `settings.tls.client_certificate` | `apim_application` | Plan shows **deprecation** warning; migrate to `settings.tls.client_certificates` |

#### 4. Recommended migration checklist

| Step | Action |
| --- | --- |
| 1 | Confirm APIM version (target **4.12** for full 1.0 feature set). |
| 2 | Pin provider to `~> 1.0.0` and run `terraform init -upgrade`. |
| 3 | Fix HRIDs that fail the new regex (see above). |
| 4 | Remove `metadata.hidden` from all modules. |
| 5 | Replace deprecated `client_certificate` where used. |
| 6 | Run `terraform plan` in non-production; resolve validation errors before apply. |
| 7 | Optionally adopt new resources/fields ([guides](https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides)). |

**Not required for 1.0.0:** `terraform state rm`, state surgery, or `schema_version` migration (unchanged).

### Known limitations

* When you run `terraform plan` for APIs, several differences exist between state and remote. These do not impact runtime and will be fixed in upcoming patches.
  * State stores the dynamic properties service configuration as an encoded JSON string instead of plain JSON.
  * The encrypted properties payload is marked as changed because encrypted values replace unencrypted values.
  * Group members order changes (no runtime impacts) cannot be changed, addition must come last
  * All group members roles are returned (even if not set), following this specific order: API, APPLICATION, INTEGRATION (no runtime impacts) it is advised to set them all to avoid plan diff.

### Links

| Topic | URL |
| --- | --- |
| Provider registry (this release) | https://registry.terraform.io/providers/gravitee-io/apim/1.0.0 |
| Provider docs (latest) | https://registry.terraform.io/providers/gravitee-io/apim/latest/docs |
| OpenTofu | https://search.opentofu.org/provider/gravitee-io/apim/latest |
| All guides index | https://registry.terraform.io/providers/gravitee-io/apim/latest/docs/guides |
