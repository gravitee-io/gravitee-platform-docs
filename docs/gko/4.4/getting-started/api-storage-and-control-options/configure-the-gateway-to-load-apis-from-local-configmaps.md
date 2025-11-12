# Configure the Gateway to load APIs from local ConfigMaps

The Gravitee Gateway can load API definitions from two places:

1. The Gateway can load APIs from a central repository (e.g. APIM's MongoDB database). This is the classic approach used for Gravitee API Management.&#x20;
2. The Gateway can load APIs from Kubernetes ConfigMaps local to the cluster on which the Gateway is running. These ConfigMaps are managed by GKO.

The default behaviour is for the gateway to load its API definitions from a central repository, as described in option 1 above. This is the most common approach used, as described in the [Example Architecture](docs/gko/4.4/overview/example-architecture.md).

## Set the Gateway to load APIs from local ConfigMaps

To load APIs from local ConfigMAps, in the Gateway's configuration, ensure that `services.sync.kubernetes` is set to `true`. This property is disabled by default.

* If your Gateway is deployed using a Helm Chart, you can enable the Kubernetes Operator option [through Helm values](docs/gko/4.4/getting-started/installation/install-with-helm.md).
* For other deployment strategies (e.g., deployment using a VM), you can update the configuration:
  * By setting an environment variable: `GRAVITEE_SERVICES_SYNC_KUBERNETES_ENABLED=true`
  *   Directly in the [`gravitee.yml`](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml#L264) file:

      {% code title="gravitee.yml" %}
      ```yaml
      # Enable Kubernetes Synchronization
      # This sync service requires to install Gravitee Kubernetes Operator
      #    kubernetes:
      #      enabled: false
      ```
      {% endcode %}

The Gateway can be configured to both load APIs from a central repository as well as from local ConfigMaps. This means that some API definitions can come from the APIM Console, and others from the Gravitee Kubernetes Operator.&#x20;

For the Operator to create APIs as local ConfigMaps, the ApiV4Definition and ApiDefinition resources need to be configured accordingly, as is described [on this page](store-apis-in-local-configmaps.md).
