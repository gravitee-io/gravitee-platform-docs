---
description: Configure automatic cleanup of events and audit data from the database.
hidden: true
noIndex: true
---

# Cleanup Services

## Overview

Gravitee APIM stores event and audit data in the database. Over time, these collections grow and consume significant storage. APIM provides two built-in cleanup services that automatically remove old data:

* **Events cleanup service:** Removes old events per type, keeping only the most recent entries.
* **Audit cleanup service:** Removes audit records older than a specified retention period.

Both services are **disabled by default** and run on the primary cluster node only. Enable and configure them in the Management API `gravitee.yml` file.

## Events cleanup service

The events cleanup service groups events by type and reference (for example, API ID or dictionary ID), keeps the most recent events per group, and deletes the rest.

### Configuration

Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
services:
  events:
    enabled: true
    cron: "@daily"
    keep: 5
    timeToLive: 30
```
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Management API service:

```bash
gravitee_services_events_enabled=true
gravitee_services_events_cron=@daily
gravitee_services_events_keep=5
gravitee_services_events_timeToLive=30
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Set the `api.services.events` block in your `values.yaml` file. The APIM Helm chart renders this block directly into the Management API `gravitee.yml` at install time, gated by `enabled: true`:

```yaml
api:
  services:
    events:
      enabled: true
      cron: "@daily"
      keep: 5
      timeToLive: 30
```
{% endtab %}
{% endtabs %}

Other cron examples:

```yaml
# Run every day at midnight
cron: "0 0 0 * * *"

# Run every Sunday at 2:00 AM
cron: "0 0 2 * * SUN"

# Run every 6 hours
cron: "0 0 */6 * * *"

# Run on the 1st of every month at 3:00 AM
cron: "0 0 3 1 * *"
```

{% hint style="info" %}
The cron expression uses 6 fields: second, minute, hour, day, month, weekday. Spring aliases such as `@daily`, `@weekly`, and `@monthly` are also accepted.
{% endhint %}

#### Configuration Properties

<table><thead><tr><th width="280">Property</th><th width="400">Description</th><th>Default</th></tr></thead><tbody><tr><td><code>services.events.enabled</code></td><td>Enable or disable the events cleanup service.</td><td><code>false</code></td></tr><tr><td><code>services.events.cron</code></td><td>Cron expression that defines when the cleanup runs. Supports standard cron syntax and Spring aliases such as <code>@daily</code>, <code>@weekly</code>, and <code>@monthly</code>.</td><td><code>@daily</code></td></tr><tr><td><code>services.events.keep</code></td><td>Number of most recent events to retain per event type and reference. Events beyond this count are deleted.</td><td><code>5</code></td></tr><tr><td><code>services.events.timeToLive</code></td><td>Maximum duration (in minutes) for a single cleanup run. If the cleanup operation exceeds this time, it stops gracefully.</td><td><code>30</code></td></tr></tbody></table>

#### How it works

1. The service iterates over all environments in the installation.
2. For each environment, it groups events by type and reference ID (for example, API, dictionary, organization, shared policy group, or gateway).
3. Within each group, it keeps the most recent events (determined by the `keep` value) and deletes older events in batches.
4. If the operation exceeds the `timeToLive` duration, the cleanup stops.

## Audit cleanup service

The audit cleanup service removes audit records older than a configurable retention period.

### Configuration

Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
services:
  audit:
    enabled: true
    cron: "0 1 * * * *"
    retention:
      days: 365
```
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Management API service:

```bash
gravitee_services_audit_enabled=true
gravitee_services_audit_cron=0 1 * * * *
gravitee_services_audit_retention_days=365
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Set the `api.services.audit` block in your `values.yaml` file. The APIM Helm chart renders this block directly into the Management API `gravitee.yml` at install time, gated by `enabled: true`:

```yaml
api:
  services:
    audit:
      enabled: true
      cron: "0 1 * * * *"
      retention:
        days: 365
```
{% endtab %}
{% endtabs %}

#### Configuration properties

<table><thead><tr><th width="280">Property</th><th width="400">Description</th><th>Default</th></tr></thead><tbody><tr><td><code>services.audit.enabled</code></td><td>Enable or disable the audit cleanup service.</td><td><code>false</code></td></tr><tr><td><code>services.audit.cron</code></td><td>Cron expression that defines when the cleanup runs.</td><td><code>0 1 * * * *</code> (1:00 AM daily)</td></tr><tr><td><code>services.audit.retention.days</code></td><td>Number of days to retain audit records. Records older than this value are deleted.</td><td><code>365</code></td></tr></tbody></table>

#### How it works

1. The service iterates over all environments in the installation.
2. For each environment, it deletes all audit records older than the configured retention period.

### Limitations

* Both services run on the **primary cluster node only**. If the primary node isn't available, cleanup doesn't occur until a new primary is elected.
* The events cleanup service has a time limit (`timeToLive`). If the database contains a large backlog of events, it may take multiple runs to fully clean up. Increase the `timeToLive` value or run the service more frequently to address this.
