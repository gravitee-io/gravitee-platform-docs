---
description: Understand the lifecycle states for v4 APIs and the allowed transitions between them.
---

# API lifecycle states

## Overview

Every v4 API has a **lifecycle state** that controls its visibility on the Developer Portal and signals its stage in the API retirement workflow. Only APIs with the `PUBLISHED` lifecycle state appear on the Developer Portal. The lifecycle state is separate from the API's runtime state (STARTED or STOPPED), which controls whether the Gateway accepts traffic.

The available lifecycle states are:

<table>
    <thead>
        <tr>
            <th width="167">State</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>CREATED</code></td>
            <td>The API has been created but hasn't been published. This is the initial state for APIs created through the Console or Management API.</td>
        </tr>
        <tr>
            <td><code>PUBLISHED</code></td>
            <td>The API is published and available on the Developer Portal (subject to visibility settings).</td>
        </tr>
        <tr>
            <td><code>UNPUBLISHED</code></td>
            <td>The API has been unpublished from the Developer Portal. It can be republished later. This is the default state for APIs created through the Gravitee Kubernetes Operator.</td>
        </tr>
        <tr>
            <td><code>DEPRECATED</code></td>
            <td>The API is no longer visible on the Developer Portal. New plans can't be created on a deprecated API, and the Console removes publish and unpublish actions. Existing subscriptions and Gateway traffic aren't affected.</td>
        </tr>
        <tr>
            <td><code>ARCHIVED</code></td>
            <td>The API is fully retired. An archived API can't be started or stopped through the Management API. Use this state to preserve the API's history and analytics. This is a <strong>terminal state</strong> — the API can't transition to any other lifecycle state after archival.</td>
        </tr>
    </tbody>
</table>

{% hint style="info" %}
The lifecycle state doesn't affect whether the Gateway routes traffic to the API. To stop traffic, change the API's runtime state to STOPPED using the **Stop the API** action in the Danger Zone.
{% endhint %}

## Allowed transitions

Not all state transitions are valid. The following table shows which transitions are allowed:

<table>
    <thead>
        <tr>
            <th width="150">From</th>
            <th>Allowed transitions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>CREATED</code></td>
            <td><code>PUBLISHED</code>, <code>UNPUBLISHED</code>, <code>DEPRECATED</code>, <code>ARCHIVED</code></td>
        </tr>
        <tr>
            <td><code>PUBLISHED</code></td>
            <td><code>UNPUBLISHED</code>, <code>DEPRECATED</code>, <code>ARCHIVED</code></td>
        </tr>
        <tr>
            <td><code>UNPUBLISHED</code></td>
            <td><code>PUBLISHED</code>, <code>DEPRECATED</code>, <code>ARCHIVED</code></td>
        </tr>
        <tr>
            <td><code>DEPRECATED</code></td>
            <td><code>ARCHIVED</code> (Gravitee Kubernetes Operator only)</td>
        </tr>
        <tr>
            <td><code>ARCHIVED</code></td>
            <td>None (terminal state)</td>
        </tr>
    </tbody>
</table>

Key rules:

* **ARCHIVED is terminal.** Once an API reaches the ARCHIVED state, it can't transition to any other lifecycle state.
* **DEPRECATED → ARCHIVED is supported through the Gravitee Kubernetes Operator only.** The Console and Management API don't allow transitions from DEPRECATED. To archive a deprecated API through the operator, update the `lifecycleState` field in your `ApiV4Definition` resource to `ARCHIVED`. For details, see [Deprecate or archive an API](../../../../gko/4.11/guides/publish-apis-to-the-portal.md#deprecate-or-archive-an-api).
* **No backward transition to CREATED.** After an API has been published or unpublished, it can't return to the CREATED state.
* **API Review blocks transitions from CREATED.** If API Review is enabled and the API has an active review in progress (IN\_REVIEW status), transitions from CREATED are blocked until the review is completed.

## Typical retirement workflow

A common pattern for gracefully retiring an API:

1. **PUBLISHED** → **DEPRECATED**: Signal that the API is being retired. The API is no longer visible to consumers, and new plans can't be created on it.
2. Deprecate or close the API's individual plans to block new subscriptions.
3. Stop the API's runtime state (STARTED → STOPPED) after all consumers have migrated.
4. **DEPRECATED** → **ARCHIVED** (operator only): Archive the API to preserve its history and analytics, or delete it.

## Change the lifecycle state

### Console

1. Log in to the APIM Console.
2. Click **APIs** in the left nav.
3. Select the API.
4. Click **Configuration** in the inner left nav, then click the **General** tab.
5. Scroll to the **Danger Zone** section and use the appropriate action:
    * **Publish the API**: Transitions to PUBLISHED.
    * **Unpublish the API**: Transitions to UNPUBLISHED (visible only when the API is currently PUBLISHED).
    * **Deprecate**: Transitions to DEPRECATED.

{% hint style="info" %}
The Console doesn't expose an **Archive** action. To set the ARCHIVED state, use the Management API or the [Gravitee Kubernetes Operator](../../../../gko/4.11/guides/publish-apis-to-the-portal.md).
{% endhint %}

### Management API

Update the API's `lifecycleState` field using the Management API:

```bash
curl -X PUT "https://{management-api}/management/v2/environments/{envId}/apis/{apiId}" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "lifecycleState": "DEPRECATED"
  }'
```

Replace `DEPRECATED` with the target state (`PUBLISHED`, `UNPUBLISHED`, `DEPRECATED`, or `ARCHIVED`).

## Lifecycle state vs. plan status

The API lifecycle state and plan status are separate concepts:

* **API lifecycle state** controls whether the API is visible to consumers and restricts certain management operations (for example, new plans can't be created on a deprecated API, and archived APIs can't be started or stopped).
* **Plan status** controls whether a specific plan accepts new subscriptions. A plan with DEPRECATED status blocks new subscriptions but keeps existing ones active.

Deprecating an API's lifecycle state doesn't automatically deprecate or close its plans. To fully block new subscriptions, deprecate the individual plans as a separate step.
