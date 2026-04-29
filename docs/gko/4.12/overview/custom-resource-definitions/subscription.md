# Subscription

The `Subscription` custom resource definition (CRD) is the GKO equivalent of the Gravitee subscriptions that can be managed in the API Management Console.

In Gravitee, a subscription is what allows a consumer to obtain access to an API. With a valid subscription, a consumer's application can obtain the credentials to consume the underlying API plan. The credentials used depend on the type of the plan, and the Gravitee Gateway verifies that the credentials match a valid subscription.&#x20;

GKO supports three of the four Gravitee subscription types: JWT, OAuth, and mTLS. API Key subscriptions are not currently supported by GKO, but will be added in a future release.

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

### Overview

API Key Rotation for Subscriptions enables administrators to manage multiple API keys per subscription with optional expiry dates. The feature replaces the single `customApiKey` field with an `apiKeys` array, allowing seamless key rotation without service interruption. It is available for API_KEY plan types via the Automation REST API and Kubernetes Operator.

#### Reconciliation Logic

The system applies the following rules during subscription updates:

| Condition | Action |
|:----------|:-------|
| Key in spec, active in APIM | Update `expireAt` if changed |
| Key in spec, revoked in APIM | Reactivate it |
| Key in spec, not in APIM | Create it |
| Key not in spec, active in APIM | Revoke immediately |
| Key not in spec, revoked in APIM | No-op |

{% hint style="info" %}
**Key** refers to an API key defined in the GKO resource specification. **Spec** refers to the desired state declared in the Kubernetes resource.
{% endhint %}

### Restrictions

- **Plan type compatibility**: The `apiKeys` array is only allowed for `API_KEY` plan types. Attempting to use it with other plan types (e.g., `JWT`) results in a validation error.
- **Key length**: Each API key must be 32–256 characters in length.
- **Duplicate prevention**: Duplicate keys within the `apiKeys` array are not permitted.
- **Schema migration**: The `customApiKey` field is removed from the schema. Existing subscriptions must migrate to the `apiKeys` array format.
- **Rotation behavior**: API key rotation requires updating the entire `apiKeys` array. Partial updates are not supported.
- **Revocation handling**: Revoked keys remain in APIM with `revoked: true` status and are not automatically deleted.
- **Restoration behavior**: When restoring a closed subscription with custom API keys, revoked keys are reactivated if present in the spec.
- **Expiration**: Keys without an `expireAt` value remain valid indefinitely.
- **Reconciliation frequency**: Key reconciliation occurs on every subscription update. Frequent updates may trigger multiple reconciliation cycles.

{% hint style="warning" %}
API key rotation requires replacing the entire `apiKeys` array. Partial updates are not supported.
{% endhint %}

### Rotating API Keys

Update the `SubscriptionSpec.apiKeys` array by adding new keys and optionally retaining old keys. The system reconciles the desired state by performing the following actions:

* Creating new keys not present in APIM
* Reactivating revoked keys present in the spec
* Revoking active keys not present in the spec
* Updating `expireAt` for keys with changed expiry

Old keys removed from the spec are revoked immediately. To rotate a key without downtime, add the new key to the array before removing the old key in a subsequent update.

{% hint style="warning" %}
Keys removed from the `apiKeys` array are revoked immediately and cannot be used for API access.
{% endhint %}

### Prerequisites

Before configuring API key subscriptions, ensure the following requirements are met:

* The subscription must target an `API_KEY` plan type.
* Each API key must be between 32 and 256 characters in length.
* The updated Kubernetes CRD (`gravitee.io_subscriptions.yaml`) must be applied before using `apiKeys` in Kubernetes resources.
* Automation REST API clients must use the updated `SubscriptionSpec` schema.

For example YAML syntax, see the "Creating a Subscription with Custom API Keys" section below.

