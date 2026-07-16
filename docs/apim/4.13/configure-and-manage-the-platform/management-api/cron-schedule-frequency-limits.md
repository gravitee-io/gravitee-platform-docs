# Cron Schedule Frequency Limits

## Overview

Cron Schedule Frequency Limits allow platform administrators to enforce minimum intervals for cron-based services in shared or SaaS environments. By setting limits in `gravitee.yml`, administrators prevent users from configuring schedules that run too frequently and risk degrading platform performance. This feature applies to documentation auto-fetch, dynamic properties, health-check, and dictionary polling services.

## Key Concepts

### Frequency Limit Enforcement

Administrators configure minimum intervals for each service type. When a user attempts to create or update an API, page, or dictionary with a schedule more frequent than the configured limit, the management API rejects the request with a validation error. For existing configurations that exceed newly applied limits, the platform silently enforces the limit at runtime by using the slower schedule.

### Cron Limit Format

Cron limits use the same 6-field cron format (including seconds) already used by APIM schedules. For example, `0 */5 * * * *` enforces a minimum interval of 5 minutes. An empty cron limit means no frequency restriction is applied.

### Dictionary Delay Limit

Dynamic dictionaries use a delay limit specified in milliseconds instead of cron expressions. A delay limit of `0` means no frequency restriction is applied.

## Prerequisites

Before configuring frequency limits, ensure you have:

* Access to the `gravitee.yml` configuration file
* Understanding of cron expression syntax (6-field format including seconds)
* Knowledge of existing API, page, and dictionary schedules in your environment

## Gateway Configuration

### Service Frequency Limits

| Property | Description | Example |
|:---------|:------------|:--------|
| `services.auto_fetch.cron_limit` | Minimum interval for documentation auto-fetch cron schedules. Empty string means no limit. | `0 */10 * * * *` (every 10 minutes) |
| `services.dynamic_properties.cron_limit` | Minimum interval for dynamic properties cron schedules. Empty string means no limit. | `0 */5 * * * *` (every 5 minutes) |
| `services.healthcheck.cron_limit` | Minimum interval for health-check cron schedules. Empty string means no limit. | `0 */2 * * * *` (every 2 minutes) |
| `services.dictionary.delay_limit` | Minimum polling delay for dynamic dictionaries in milliseconds. `0` means no limit. | `300000` (5 minutes) |

## Creating Frequency Limits

1. Edit the `gravitee.yml` file and add the desired limits under the `services` section.

 For example, to enforce a 5-minute minimum for dynamic properties:

 ```yaml
 services:
   dynamic_properties:
     cron_limit: 0 */5 * * * *
 ```

 For dictionary polling:

 ```yaml
 services:
   dictionary:
     delay_limit: 300000
 ```

2. Save the configuration file.

3. Restart the management API.

Existing APIs, pages, and dictionaries with schedules more frequent than the new limits will continue to run at the limited frequency without requiring manual updates. New or updated configurations will be validated against the limits, and users will receive validation errors if they attempt to configure schedules that exceed the limits.

## Managing Existing Configurations

When frequency limits are applied to an environment with existing APIs, pages, or dictionaries, no immediate action is required. Existing configurations that exceed the new limits will continue to function, but the platform will silently enforce the limit at runtime by using the slower schedule.

For example, if an API has a dynamic properties schedule of `0 */2 * * * *` (every 2 minutes) and a new limit of `0 */5 * * * *` (every 5 minutes) is applied, the API will run at the 5-minute interval.

To align existing configurations with the new limits:

1. Review API, page, and dictionary schedules manually.
2. Update schedules to comply with the new limits.
3. Communicate the new limits to API publishers and documentation maintainers to ensure they configure schedules appropriately.

## Restrictions

* Limits are environment-wide and cannot be customized per API, page, or dictionary.
* Runtime enforcement is silent; users are not notified when the platform uses the limit value instead of their configured schedule.
* Validation errors only occur during creation or update operations; existing configurations are not rejected.
* No UI indication of applied limits is shown when users configure schedules; warnings appear only when they attempt to save.
* Cron frequency comparison uses a fixed reference time (`2026-01-01 00:00`); cron expressions with no future executions from this date will cause validation errors.
* Empty cron limits or a delay limit of `0` means no frequency restriction is applied.

## Related Changes

Validation logic has been added to the management API for documentation auto-fetch, dynamic properties (v2 and v4 APIs), health-check (v2 and v4 APIs), and dictionary services. When a user attempts to save a configuration with a schedule more frequent than the configured limit, the API returns a validation error with a message indicating the limit.

Error messages include the specific limit value and the affected resource name:

* **Documentation Auto-Fetch (validation):**
 `"property [fetchCron] of source [<sourceType>] must not run more frequently than [<cronLimit>] for page [<pageName>]"`

* **Documentation Auto-Fetch:**
 `"Invalid fetchCron expression in page '<pageName>': it must not run more frequently than the configured limit <cronLimit>"`

* **Dynamic Properties (v2 API):**
 `"Dynamic properties schedule must not run more frequently than the configured limit: <cronLimit>"`

* **Dynamic Properties (v4 API):**
 `"Dynamic properties schedule must not run more frequently than the configured limit: <cronLimit>"`

* **Health-Check (v2 API):**
 `"Healthcheck schedule must not run more frequently than the configured limit: <cronLimit>"`

* **Health-Check (v4 API):**
 `"Healthcheck schedule must not run more frequently than the configured limit: <cronLimit>"`

* **Dictionary:**
 `"Dictionary trigger must not run more frequently than the configured limit: <delayLimitMillis>ms"`

