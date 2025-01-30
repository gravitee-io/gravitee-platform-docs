# Subscription

The `Subscription` Custom Resource Definition (CRD) is GKO's equivalent to the concept of subscriptions as can been seen in the Gravitee API Management console.

Subscriptions are how applications obtain access to API plans. With a valid subscription, an application can obtain credentials and consume the underlying API's plan. The Gravitee gateway will verify that the credentials match a valid subscription. The credentials used depend on the type of the plan.

GKO supports three of the four Gravitee subscription types: JWT, OAuth, and mTLS. API key subscriptions are not currently supported by GKO but will be added in a future release.JWT

For GKO to be able to create a subscription, the corresponding application and API must also be managed by GKO using the dedicated CRDs.

## Example Subscription with GKO

The example below is based on three prerequisites:

* GKO is already managing an API whose **metadata.name** is `petstore-api`
* my-api has a plan called `petstore-jwt-plan` (as defined by the key for this plan in the API's **plans** map)
* GKO is already managing an application whose **metadata.name** is `petstore-consumer`.

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

And the matching application:

<pre class="language-yaml"><code class="lang-yaml"><strong>apiVersion: gravitee.io/v1alpha1
</strong>kind: Application
metadata:
  name: petstore-consumer
  ...
</code></pre>

For more information:

* For a detailed guide on managing subscriptions with GKO, see [manage-jwt-subscriptions-with-gko.md](../../guides/manage-jwt-subscriptions-with-gko.md "mention").
* The `Subscription` CRD code is available on [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/api/v1alpha1/subscription_types.go).
* The `Subscription` CRD API reference is documented [here](https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/docs/api/reference.md#subscription).
