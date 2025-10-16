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
