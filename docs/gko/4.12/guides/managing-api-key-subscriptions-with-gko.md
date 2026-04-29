# Managing API Key Subscriptions with GKO

## Overview

GKO now supports API Key subscriptions in addition to JWT, OAuth, and mTLS. You can create subscriptions to API Key plans, provide your own custom API keys, rotate keys declaratively, and source key values from Kubernetes Secrets.

{% hint style="info" %}
GKO-managed subscriptions only work when GKO is configured to sync APIs with a Gravitee API management control plane (i.e. `local=false` for v2 APIs, or `syncFrom=MANAGEMENT` for v4 APIs).
{% endhint %}

## Prerequisites

Before you begin, ensure the following:

* Gravitee Kubernetes Operator is running on your system.
* Gravitee API Management and a Gravitee Gateway are running on your system.
* Your API has a plan with `security.type: API_KEY` and the plan is in `PUBLISHED` status.

## Subscribe to an API Key plan

To subscribe to an API Key plan without specifying a custom key, create a `Subscription` resource that references the plan. APIM generates a key automatically.

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Subscription
metadata:
  name: my-api-key-subscription
spec:
  api:
    name: my-api
  application:
    name: my-app
  plan: API_KEY
```

## Use custom API keys

You can provide your own API key values using the `apiKeys` field. This is useful when you need deterministic, pre-shared keys rather than auto-generated ones.

{% hint style="warning" %}
Custom API keys must be between 32 and 256 characters long. Keys shorter than 32 characters or longer than 256 characters are rejected by the CRD schema validation.
{% endhint %}

```yaml
apiVersion: gravitee.io/v1alpha1
kind: Subscription
metadata:
  name: my-api-key-subscription
spec:
  api:
    name: my-api
  application:
    name: my-app
  plan: API_KEY
  apiKeys:
    - key: "a]3kP!9xR#mW2vL$8nQ5yT0uF6jB7dHs"
```

You can also set an expiration date on individual keys using the `expireAt` field:

```yaml
apiKeys:
  - key: "a]3kP!9xR#mW2vL$8nQ5yT0uF6jB7dHs"
    expireAt: "2026-12-31T23:59:59Z"
```

## Source API keys from Kubernetes Secrets

Instead of hardcoding key values in the Subscription manifest, you can store them in a Kubernetes Secret and reference them. This keeps sensitive values out of your Git repository.

1.  Create a Secret containing your API key:

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: my-api-key-secret
    type: Opaque
    stringData:
      apiKey: "a]3kP!9xR#mW2vL$8nQ5yT0uF6jB7dHs"
    ```

2.  Reference the Secret in your Subscription using the `[[ secret ... ]]` template syntax:

    ```yaml
    apiVersion: gravitee.io/v1alpha1
    kind: Subscription
    metadata:
      name: my-api-key-subscription
    spec:
      api:
        name: my-api
      application:
        name: my-app
      plan: API_KEY
      apiKeys:
        - key: '[[ secret `my-api-key-secret/apiKey` ]]'
    ```

## Rotate API keys

GKO manages API key rotation declaratively. When you update the `apiKeys` list in your Subscription spec, GKO reconciles the desired state with APIM:

* Keys present in the spec but not yet in APIM are created.
* Keys present in APIM but removed from the spec are revoked.
* Previously revoked keys that reappear in the spec are reactivated.

### Instant rotation

To rotate a key instantly, replace the old key with a new one in the spec:

```yaml
apiKeys:
  - key: "Qw8$mN3!xR7vKp2#LsY9fT0uJ6bD5hWa"
```

On the next reconciliation, GKO revokes the old key and creates the new one. Consumers using the old key are immediately rejected by the Gateway.

### Gradual rotation

For zero-downtime rotation, add the new key alongside the old one first:

```yaml
apiKeys:
  - key: "a]3kP!9xR#mW2vL$8nQ5yT0uF6jB7dHs"
  - key: "Qw8$mN3!xR7vKp2#LsY9fT0uJ6bD5hWa"
```

Both keys are active simultaneously. Once all consumers have migrated to the new key, remove the old one:

```yaml
apiKeys:
  - key: "Qw8$mN3!xR7vKp2#LsY9fT0uJ6bD5hWa"
```

The old key is revoked on the next reconciliation.

## Close an API Key subscription

Deleting the Subscription resource closes the subscription and revokes all associated API keys. Consumers are rejected with a 401 status on subsequent calls to the Gateway.

```bash
kubectl delete -f resources/subscription.yml
```
