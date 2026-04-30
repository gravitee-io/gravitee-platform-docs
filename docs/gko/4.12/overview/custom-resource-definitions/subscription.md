# Subscription

The `Subscription` custom resource definition (CRD) is the GKO equivalent of the Gravitee subscriptions that can be managed in the API Management Console.

In Gravitee, a subscription is what allows a consumer to obtain access to an API. With a valid subscription, a consumer's application can obtain the credentials to consume the underlying API plan. The credentials used depend on the type of the plan, and the Gravitee Gateway verifies that the credentials match a valid subscription.&#x20;

GKO supports all four Gravitee subscription types: JWT, OAuth, mTLS, and API Key. API Key subscriptions accept multiple custom keys per subscription with optional expiry dates, and the operator handles key rotation through the `apiKeys` array in the `Subscription` spec.

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

{% hint style="info" %}
**For more information**

* For a detailed guide on managing subscriptions with GKO, see [manage-jwt-subscriptions-with-gko.md](../../guides/manage-jwt-subscriptions-with-gko.md "mention").
* The `Subscription` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/subscription_types.go).
* The `Subscription` CRD API reference is documented [here](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/docs/api/reference.md#subscription).
{% endhint %}

## API key subscriptions

GKO supports subscriptions to plans whose security type is `API_KEY`. The `Subscription` spec accepts an `apiKeys` array, where each entry sets a custom key value and an optional expiry date. The operator forwards the desired keys to the APIM Automation API, and APIM reconciles them against the keys it already holds for the subscription.

{% hint style="warning" %}
The `customApiKey` field is removed from the `Subscription` CRD in 4.12. Update existing manifests to the new `apiKeys` array format before upgrading.
{% endhint %}

### Schema

| Field | Type | Description | Required |
|---|---|---|---|
| `apiKeys` | array of `ApiKeySpec` | Custom API keys assigned to the subscription. Only valid when the target plan's security type is `API_KEY`. | Optional |
| `apiKeys[].key` | string | Custom API key value. Length: 32-256 characters. | Required |
| `apiKeys[].expireAt` | string | RFC 3339 date-time at which the key expires. Keys without `expireAt` don't expire. | Optional |

### Example

The example below subscribes the `petstore-consumer` application to a plan named `petstore-api-key-plan` with two custom keys:

{% code lineNumbers="true" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: Subscription
metadata:
  name: petstore-consumer-api-key-subscription
  namespace: gravitee
spec:
  api:
    name: petstore-api
  plan: petstore-api-key-plan
  application:
    name: petstore-consumer
  apiKeys:
    - key: "primary-api-key-at-least-32-characters"
      expireAt: "2026-12-31T23:59:59Z"
    - key: "secondary-api-key-at-least-32-character"
```
{% endcode %}

The matching plan in the API definition uses `API_KEY` security:

```yaml
plans:
  petstore-api-key-plan:
    name: "Petstore API key plan"
    security:
      type: API_KEY
```

### Reconciliation behavior

When you apply a `Subscription` whose `apiKeys` array is non-empty, APIM compares each desired key against its existing record for the subscription and applies the following rules:

| Key in spec | State in APIM | Action |
|---|---|---|
| Yes | Active | Update `expireAt` if it has changed. |
| Yes | Revoked | Reactivate the key, applying any `expireAt` from the spec. |
| Yes | Not in APIM | Create the key. |
| No | Active | Revoke the key immediately. |
| No | Revoked | No action. |

To rotate a key without downtime, add the replacement key alongside the old key, deploy the updated manifest, then remove the old key in a follow-up deployment.

Reconciliation runs on every apply of the `Subscription` resource. Frequent updates trigger multiple reconciliation cycles, so batch related changes into a single apply where possible.

When you restore a previously closed subscription, the operator forwards the spec's `apiKeys` to APIM and reactivates any revoked keys whose values still match entries in the spec.

Revoked keys remain attached to the subscription with `Revoked` status and aren't automatically deleted. They stay visible on the subscription page in the API Management Console for audit.

{% hint style="warning" %}
Reconciliation runs only when `apiKeys` is non-empty on the apply. Removing the field or supplying an empty array on update leaves existing keys untouched. To revoke every key on a subscription, close the subscription instead.
{% endhint %}

### Validation

The GKO admission webhook rejects a `Subscription` when:

* The target plan's security type isn't `API_KEY`.
* Any `apiKeys[].key` is shorter than 32 or longer than 256 characters.
* Two entries in `apiKeys` share the same `key` value.
* Any `apiKeys[].expireAt` isn't a valid RFC 3339 date-time.

