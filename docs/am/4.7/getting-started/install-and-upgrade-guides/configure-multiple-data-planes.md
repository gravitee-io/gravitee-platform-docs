# Configure Multiple Data Planes

## Overview

Gravitee provides the flexibility to choose the type of database for each specific use case, referred to as the "scope," in order to distribute the load and reduce pressure on a single storage point.

The scopes provided by Access Management include:

* **Management**: Data essential for the operation of the Access Management platform, such as security domains, applications, identity providers, etc. This scope is named Control Plane
* **OAuth 2.0**: Access tokens and OAuth 2.0 authorization codes, etc.
* **Gateway**: Data managed by the Access Management runtime (the Gateway) such as user profiles, scope approval, webauthn credentials, etc. This scope as the OAuth2 scope are managed by the Data Plane

As specify in the [Control Plane & Data Plane](docs/am/4.7/overview/am-architecture/control-plane-and-data-plane.md) page prior to version 4.7, the separation of data between the control plane and the data plane was not properly implemented, and certain entities, such as user profiles, were handled within the management scope. In addition to enhancing the distribution of data between the control plane and the data plane, you can now have multiple data planes for a single control plane. In this section, we set up a deployment in a new environment with two data planes.&#x20;

This deployment will include a Management API with a database for the Control Plane (CP) and two Gateways, each dedicated to a Data Plane (DataPlane\_1 & DataPlane\_2). The security domains associated with DataPlane\_1  handled only by the Gateway assigned to that data plane, and the same applies for the domains associated with DataPlane\_2. Each DataPlane has its own data cluster to isolate workloads and prevent a global service disruption if one of the databases becomes unavailable. In this deployment, if the Control Plane becomes inaccessible, the Gateways are still able to authenticate users because the necessary runtime information is now carried by the Data Plane. Similarly, if the data cluster of DataPlane\_1 is not accessible, only the Gateways of that data plane are impacted.

&#x20;

<figure><img src="../../.gitbook/assets/am-multi-dataplane (1).svg" alt=""><figcaption><p>Multi Data Plane deployment</p></figcaption></figure>

## Configure the Management API

The Management API service now depends solely on the `management` repository scope. It is still necessary to specify the `gateway` and `oauth2` scopes for technical reasons, but eventually, these declarations will be removed. As a result, the settings for these three scopes can be identical. The Management API will access data from the DataPlane through a new DataPlane-type plugin. This plugin must have a data plane identifier, along with the connection parameters for the data backend, which is also known as the DataPlane.

First, let's configure the repositories:&#x20;

```yaml
repositories:
  # specify which scope is used as reference
  # to initialize the IdentityProviders with the "use system cluster"
  # option enabled (only management and gateway scopes are allowed as value)
  system-cluster: gateway
  # Management repository is used to store global configuration such as domains, clients, ...
  # This is the default configuration using MongoDB (single server)
  # For more information about MongoDB configuration, please have a look to:
  # - http://api.mongodb.org/java/current/com/mongodb/MongoClientOptions.html
  management:
    type: mongodb
    mongodb:
      uri: mongodb+srv://am-user:xxxxxxxxx@my.cp.mongodb.atlas/gravitee-am-cp?...
  
  gateway:
    type: mongodb
    use-management-settings: true
    mongodb:
      uri: mongodb+srv://am-user:xxxxxxxxx@my.cp.mongodb.atlas/gravitee-am-cp?...

  oauth2:
    type: mongodb
    use-management-settings: true
    mongodb:      
      uri: mongodb+srv://am-user:xxxxxxxxx@my.cp.mongodb.atlas/gravitee-am-cp?...
```

As mentioned previously, the three scopes have the same settings as the Management API does not rely on the `gateway` and `oauth2` scopes. The use-management-settings allows to instantiate only one connection pool to the cluster based on the `management` scope settings.

Next, let's configure the list of data planes.

```yaml
# configure the DataPlane plugin
dataPlanes:
  - id: default
    name: DataPlane_1
    gateway:
      url: https://my.dataplane1.io/
    type: mongodb
    mongodb:
      uri: mongodb+srv://am-user:xxxxxxxxx@my.dp1.mongodb.atlas/gravitee-am-dp1?...
  - id: dataplane2
    name: DataPlane_2
    gateway:
      url: https://my.dataplane2.io/
    type: mongodb
    mongodb:
      uri: mongodb+srv://am-user:xxxxxxxxx@my.dp2.mongodb.atlas/gravitee-am-dp2?...
  
```

In this configuration example, two data planes, `DataPlane_1` and `DataPlane_2`, are defined. It is important to note that a data plane with the identifier `default` is required. When a domain is created, it is assigned to a data plane and cannot be changed. The `default` identifier is necessary to allow the assignment of existing domains to a data plane during an upgrade from a version prior to 4.7. The `name` attribute is a label that can be modified. This label is passed to the console by the Management API to facilitate the selection process for users wishing to create a domain. The `gateway.url` element specifies the base URL of the Gateway for this particular data plane. It is used, for example, to display endpoints in the UI with the correct URL or to send user registration confirmation emails generated by the Management API. Apart from these few parameters, the configuration is identical to a repository configuration, with a type and associated connection elements.

## Configure the Gateways

The configuration of the gateways does not require much specific configuration. Only the repository scopes require our attention. For the `management` scope, it is necessary to specify the database configured in the `gravitee.yaml` of the Management API in order to address the same control plane. The `gateway` and `oauth2` scopes must specify the connection parameters to the data plane associated with the Gateway.

{% tabs %}
{% tab title="Data Plane 1" %}
<pre class="language-yaml"><code class="lang-yaml"><strong>repositories:
</strong>  # specify which scope is used as reference
  # to initialize the IdentityProviders with the "use system cluster"
  # option enabled (only management and gateway scopes are allowed as value)
  system-cluster: gateway
  # Management repository is used to store global configuration such as domains, clients, ...
  # This is the default configuration using MongoDB (single server)
  # For more information about MongoDB configuration, please have a look to:
  # - http://api.mongodb.org/java/current/com/mongodb/MongoClientOptions.html
  management:
    type: mongodb
    mongodb:
      uri: mongodb+srv://am-user:xxxxxxxxx@my.cp.mongodb.atlas/gravitee-am-cp?...
  
  gateway:
    type: mongodb
    use-management-settings: false
    dataPlane:
      id: default
      url: https://my.dataplane1.io/
    mongodb:
      uri: mongodb+srv://am-user:xxxxxxxxx@my.dp1.mongodb.atlas/gravitee-am-dp1?...

  oauth2:
    type: mongodb
    use-management-settings: false
    use-gateway-settings: true
    mongodb:      
      uri: mongodb+srv://am-user:xxxxxxxxx@my.dp1.mongodb.atlas/gravitee-am-dp1?...
</code></pre>
{% endtab %}

{% tab title="Data Plane 2" %}
<pre class="language-yaml"><code class="lang-yaml"><strong>repositories:
</strong>  # specify which scope is used as reference
  # to initialize the IdentityProviders with the "use system cluster"
  # option enabled (only management and gateway scopes are allowed as value)
  system-cluster: gateway
  # Management repository is used to store global configuration such as domains, clients, ...
  # This is the default configuration using MongoDB (single server)
  # For more information about MongoDB configuration, please have a look to:
  # - http://api.mongodb.org/java/current/com/mongodb/MongoClientOptions.html
  management:
    type: mongodb
    mongodb:
      uri: mongodb+srv://am-user:xxxxxxxxx@my.cp.mongodb.atlas/gravitee-am-cp?...
  
  gateway:
    type: mongodb
    use-management-settings: false
    dataPlane:
      id: dataplane2
      url: https://my.dataplane2.io/
    mongodb:
      uri: mongodb+srv://am-user:xxxxxxxxx@my.dp2.mongodb.atlas/gravitee-am-dp2?...

  oauth2:
    type: mongodb
    use-management-settings: false
    use-gateway-settings: true
    mongodb:      
      uri: mongodb+srv://am-user:xxxxxxxxx@my.dp2.mongodb.atlas/gravitee-am-dp2?...
</code></pre>
{% endtab %}
{% endtabs %}

In this configuration example, each deployment targets a specific data cluster for the data plane in the `gateway` and `oauth2` scopes. The `use-management-settings` parameter is set to prevent reusing the connection pool from the `management` scope. The `use-gateway-settings` parameter is set to true so that the `oauth2` scope uses the same connection pool as the `gateway` scope, as both scopes target the same instance. The `dataPlane` section in the gateway scope specifies which data plane this deployment should support, along with the associated base URL.

The final element to specify is to request the loading of domain roles into memory via the synchronization process, so that the Gateways do not depend on the Control Plane during authentications to retrieve the roles associated with users or groups.

```yaml
# synchronize roles defined for each domain
# to load them in the Gateway heap
services:
  sync:
    permissions: true
```

## Focus on Helm

The Helm chart has been modified to accept the same `repositories` and `dataPlanes` configuration structure as the **gravitee.yaml** in the **values.yaml**. The previous example also applies to the chart. However, a deployment per component has to be manage as only one repositories section is possible per values.yaml and we have three services to deploy.

In the `values.yaml` of the Management API, the gateways need to be disabled.

```yaml
api:
  enabled: true
  
  
gateway:
  enabled: false
```

In the `values.yaml` of the Gateway, the Management API needs to be disabled.

```yaml
api:
  enabled: false
  
gateway:
  enabled: true
```

{% hint style="success" %}
It is worth noting that the gateways also have an upgrade mechanism in the same way as for the Management API.
{% endhint %}



