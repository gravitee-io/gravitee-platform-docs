# Subscription

The `Subscription` custom resource definition (CRD) is the GKO equivalent of the Gravitee subscriptions that can be managed in the API Management Console.

In Gravitee, a subscription is what allows a consumer to obtain access to an API. With a valid subscription, a consumer's application can obtain the credentials to consume the underlying API plan. The credentials used depend on the type of the plan, and the Gravitee Gateway verifies that the credentials match a valid subscription.

GKO supports all four Gravitee subscription types: JWT, OAuth, mTLS, and API Key.

For GKO to be able to create a subscription, the corresponding application and API must also be managed by GKO using the dedicated CRDs.

{% hint style="info" %}
GKO-managed subscriptions only work when GKO is configured to sync APIs with a Gravitee API management control plane (i.e. local=false for v2 APIs, or syncFrom=MANAGEMENT for v4 APIs). See [api-storage-and-control-options](../../getting-started/api-storage-and-control-options/ "mention") for more information about these configuration options.
{% endhint %}

## Example subscription with GKO

The example below is based on three prerequisites:

* GKO is already managing an API whose **metadata.name** is `petstore-api`
* The API has a plan called `petstore-jwt-plan` (as defined by the key for this plan in the API's **plans** map)
* GKO is already managing an application whose **metadata.name** is `petstore-consumer`

{% code lineNumbers="true" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: Subscription
metadata:
  name: petstore-consumer-subscription
  namespace: gravitee
spec:
  api:
    name: petstore-api
  plan: petstore-jwt-plan
  application: 
    name: petstore-consumer
```
{% endcode %}

Below is a snippet to illustrate what the corresponding API definition CRD would look like:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiV4Definition
metadata:
  name: petstore-api
  namespace: gravitee
spec:
  ...
  plans:
    petstore-jwt-plan:
      name: "Petstore JWT plan"
      security:
        type: "JWT"
      ...
```

And here is the matching application:

<pre class="language-yaml"><code class="lang-yaml"><strong>apiVersion: gravitee.io/v1alpha1
</strong>kind: Application
metadata:
  name: petstore-consumer
  ...
</code></pre>

## API Key subscriptions with multiple keys

API Key subscriptions support multiple active API keys per subscription with optional expiry dates. This feature replaces the single `customApiKey` field with an `apiKeys` array, allowing gradual key rotation without service interruption.

### Multiple API keys

Each subscription to an API_KEY plan can now define multiple active keys simultaneously. Each key is specified as an object containing a `key` value (32–256 characters) and an optional `expireAt` timestamp in RFC3339 format (e.g., `2040-12-25T09:12:28Z`). This enables gradual rotation: add a new key with a future expiry, migrate clients, then remove the old key from the spec.

### Reconciliation behavior

The platform reconciles the `apiKeys` array against the current state in APIM using the following rules:

| Condition | Action |
|:----------|:-------|
| Key in spec, active in APIM | Update `expireAt` if changed |
| Key in spec, revoked in APIM | Reactivate it |
| Key in spec, not in APIM | Create it |
| Key not in spec, active in APIM | Revoke immediately |
| Key not in spec, revoked in APIM | No-op |

Keys not listed in the `apiKeys` array are revoked immediately, including when restoring a closed subscription.

### API key specification

Each entry in the `apiKeys` array follows the `ApiKeySpec` schema:

| Property | Type | Required | Description | Example |
|:---------|:-----|:---------|:------------|:--------|
| `key` | string | Yes | The custom API key value (32–256 characters) | `my-custom-api-key-at-least-32c` |
| `expireAt` | string (date-time) | No | Optional expiry date in RFC3339 format | `2040-12-25T09:12:28Z` |

### Prerequisites

- Subscription must target a plan with `securityType: API_KEY`
- Each API key must be between 32 and 256 characters in length
- All keys within a single subscription must be unique

### Creating API Key subscriptions

To create a subscription with custom API keys, include the `apiKeys` array in the subscription spec. The first key in the array is used as the initial custom key during subscription creation. Each key must be 32–256 characters and unique within the subscription. Optionally, set `expireAt` for any key to define an expiry date.

**Before:**

```yaml
spec:
  customApiKey: my-custom-api-key
```

**After:**

```yaml
spec:
  apiKeys:
    - key: my-custom-api-key
```

**Example with expiry:**

```yaml
spec:
  apiKeys:
    - key: my-custom-api-key-with-at-least-32c
      expireAt: "2040-12-25T09:12:28Z"
```

You can also provide your own API key values using the `apiKeys` field. This is useful when you need deterministic, pre-shared keys rather than auto-generated ones.

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

### Rotating API keys

To rotate keys without downtime, add the new key to the `apiKeys` array alongside the existing key, optionally setting a short `expireAt` on the old key. After clients migrate to the new key, remove the old key from the array. The platform will revoke any key not present in the spec immediately upon reconciliation. When restoring a closed subscription, revoked keys listed in the spec are reactivated.

**Gradual rotation pattern:**

```yaml
apiKeys:
  - key: old-key-value-at-least-32-chars!!
    expireAt: "2024-12-31T23:59:59Z"  # Short expiry
  - key: new-key-value-at-least-32-chars!!
```

After migration:

```yaml
apiKeys:
  - key: new-key-value-at-least-32-chars!!
```

### Restrictions

- `apiKeys` field is only valid for subscriptions to plans with `securityType: API_KEY`; setting it on other plan types returns error `"apiKeys is only allowed for API_KEY plans (plan: %s)"`
- Each key must be between 32 and 256 characters; shorter or longer keys return error `"key length must be between 32 and 256 characters, got %d"`
- All keys within a single subscription must be unique; duplicate keys return error `"duplicate key [%s] in apiKeys"`
- Empty keys return error `"apiKeys entries must have a non-empty key"`
- Invalid `expireAt` format returns error `"invalid expireAt for key [%s]: %s"`
- Keys not listed in the `apiKeys` array are immediately revoked upon reconciliation
- When restoring a closed subscription with custom API keys, revoked keys are reactivated if still present in the spec
- The first key in the `apiKeys` array is used as the initial custom key during subscription creation

{% hint style="info" %}
**For more information**

* For a detailed guide on managing JWT subscriptions with GKO, see [manage-jwt-subscriptions-with-gko.md](../../guides/manage-jwt-subscriptions-with-gko.md "mention").
* For a detailed guide on managing API Key subscriptions with GKO, including key rotation and sourcing keys from Kubernetes Secrets, see [manage-api-key-subscriptions-with-gko.md](../../guides/manage-api-key-subscriptions-with-gko.md "mention").
* The `Subscription` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/subscription_types.go).
* The `Subscription` CRD API reference is documented [here](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/docs/api/reference.md#subscription).
{% endhint %}
