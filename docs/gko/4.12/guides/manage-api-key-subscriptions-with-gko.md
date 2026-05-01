---
description: >-
  An end-to-end guide for managing API key subscriptions with GKO, including
  custom keys, expiry dates, and zero-downtime key rotation.
---

# Manage API key subscriptions with GKO

## Overview

This guide walks through subscribing an application to an API Key plan with GKO, supplying custom API keys with optional expiry dates, and rotating keys without downtime. GKO forwards the desired keys to APIM through the Automation API, and APIM reconciles each key against its existing record for the subscription.

For the schema, validation rules, and reconciliation behavior, see the [Subscription CRD reference](../overview/custom-resource-definitions/subscription.md#api-key-subscriptions).

{% hint style="info" %}
GKO-managed subscriptions only work when GKO is configured to sync APIs with a Gravitee API management control plane (i.e. `local=false` for v2 APIs, or `syncFrom=MANAGEMENT` for v4 APIs). See [api-storage-and-control-options](../getting-started/api-storage-and-control-options/ "mention") for more information about these configuration options.
{% endhint %}

## Before you begin

* Gravitee Kubernetes Operator 4.12 or above is running on your cluster.
* Gravitee API Management 4.12 or above and a Gravitee Gateway are running and reachable from the cluster.
* A `ManagementContext` resource referencing the APIM control plane is already applied. The examples below reference it as `dev-ctx`.
* The target API and application are managed by GKO.
* The target API has a plan with `security.type: API_KEY`.

## Procedure

### Step 1. Define an API with an API Key plan

Apply an `ApiV4Definition` whose plan uses `API_KEY` security:

{% code lineNumbers="true" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: api-v4-with-api-key
spec:
  contextRef:
    name: dev-ctx
  name: "api-v4-with-api-key"
  description: "API v4 with API KEY managed by Gravitee Kubernetes Operator"
  version: "1.0"
  type: PROXY
  listeners:
    - type: HTTP
      paths:
        - path: "/k8s-apikey-with-ctx-v4"
      entrypoints:
        - type: http-proxy
          qos: AUTO
  endpointGroups:
    - name: Default HTTP proxy group
      type: http-proxy
      endpoints:
        - name: Default HTTP proxy
          type: http-proxy
          inheritConfiguration: false
          configuration:
            target: https://api.gravitee.io/echo
          secondary: false
  flowExecution:
    mode: DEFAULT
    matchRequired: false
  plans:
    API_KEY:
      name: "API Key plan"
      description: "API key plan needs a key to authenticate"
      security:
        type: "API_KEY"
      flows:
        - enabled: true
          selectors:
            - type: HTTP
              path: "/"
              pathOperator: STARTS_WITH
```
{% endcode %}

### Step 2. Define an application

Apply an `Application` that GKO can attach to the subscription. `contextRef` and `settings` are both required:

{% code lineNumbers="true" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: Application
metadata:
  name: simple-application
spec:
  contextRef:
    name: dev-ctx
  name: "simple-app"
  description: "API key consumer application"
  settings:
    app:
      type: WEB
```
{% endcode %}

### Step 3. Create the subscription with custom API keys

Apply a `Subscription` that lists the custom keys in the `apiKeys` array. Each key is between 32 and 256 characters, and `expireAt` is optional:

{% code lineNumbers="true" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: Subscription
metadata:
  name: api-key-subscription
spec:
  api:
    name: api-v4-with-api-key
  application:
    name: simple-application
  plan: API_KEY
  apiKeys:
    - key: "my-custom-api-key-1-at-least-32c"
      expireAt: "2026-12-31T23:59:59Z"
    - key: "my-custom-api-key-2-at-least-32c"
```
{% endcode %}

### Step 4. Rotate a key without downtime

To roll a key over without breaking active consumers:

1. Add the replacement key to `apiKeys` while keeping the existing key in place. Apply the manifest. Both keys are now valid in APIM.
2. Update consumers to use the replacement key.
3. Remove the old key from `apiKeys`. Apply the manifest. APIM revokes the old key immediately.

{% hint style="warning" %}
Removing a key from `apiKeys` revokes it in APIM on the next apply. Don't remove a key until every consumer has switched to its replacement.
{% endhint %}

### Step 5. Reactivate a revoked key

To bring back a key that was previously revoked through GKO, add it back to `apiKeys` and apply the manifest. APIM reactivates the key and applies the `expireAt` value from the spec, if present.

## Verification

To verify API key rotation is working as expected, follow these steps:

1.  Apply the resources from Steps 1-3 and confirm GKO sets the `Subscription` `Accepted` condition to `True`:


    ```bash
    kubectl describe subscription api-key-subscription
    ```


    The output's `Conditions` section lists a row whose `Type` is `Accepted` and `Status` is `True`.


2.  Open the API Management Console, navigate to the subscription's edit page, and confirm that the **API Keys** card lists each value from the `apiKeys` array. Hover the status icon next to a key: the tooltip reads `Valid` for an active key.


    The page also displays the banner *"This subscription was created by the Kubernetes Operator and cannot be managed through the console."*


    <!-- TODO: Screenshot of the subscription edit page in APIM Console showing the API Keys card with two valid keys and the GKO banner -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-gko-2550-active-keys.png" alt=""><figcaption><p>Subscription edit page showing the two custom API keys with Valid status</p></figcaption></figure>


3.  Apply an updated `Subscription` whose `apiKeys` array swaps the first key for a new value. Reload the Console and confirm:

    * The new key appears in the **API Keys** card with the `Valid` tooltip.
    * The removed key's tooltip now reads `Revoked or Expired`, and the **Revoked/Expired at** column displays the time of revocation.
    * For each remaining valid key, the **Revoked/Expired at** column shows the `expireAt` value from the manifest, or `-` if `expireAt` was omitted.


    <!-- TODO: Screenshot of subscription edit page after rotation -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-gko-2550-rotated-keys.png" alt=""><figcaption><p>Subscription edit page after key rotation</p></figcaption></figure>
