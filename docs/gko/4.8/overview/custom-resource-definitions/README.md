# Custom Resource Definitions

The Gravitee Kubernetes Operator (GKO) comes with several custom resource definitions (CRDs):

* [`ManagementContext`](managementcontext.md)
* [`ApiV4Definition`](apiv4definition.md) and [`ApiDefinition`](apidefinition.md)
* [`Application`](application.md)
* [`ApiResource`](apiresource.md)
* [`Subscription`](subscription.md)
* [`Group`](group.md)

{% hint style="info" %}
Sample CRDs are available in the GKO GitHub [repository](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/4.5.x/examples).
{% endhint %}

The `ApiV4Definition` and `ApiDefinition` custom resources are used to define individual APIs that run on the Gateway. APIs are the most important resource that GKO manages. `ApiV4Definition` is used to define v4 Gravitee APIs. It supports both traditional proxy APIs and event APIs and was introduced in GKO 4.4. `ApiDefinition` is used to define v2 Gravitee APIs.

`Resources` are objects that allow you to define pointers to external resources, such as authentication providers and caches, that can then be referenced from an API definition's policies. For example, an OAuth2 provider can be referenced from an API's OAuth2 authentication policy by pointing to the right `Resource`. Resources are referenced from `ApiV4Definitions` and `ApiDefinitions`.

The `Application` custom resource represents the configuration for an application. Applications are used to identify the consumer of an API, and to carry subscriptions and credentials.

Finally, the purpose of the `ManagementContext` is to provide a connection from GKO to your Gravitee API Management installation. GKO uses this connection to synchronize the resources it manages (APIs, applications, ...) with the Gravitee Console, Developer Portal, and Gateway.

In the following sections, we run through each CRD one by one.
