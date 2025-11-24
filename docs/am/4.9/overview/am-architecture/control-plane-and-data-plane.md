---
description: Overview of Control Plane.
---

# Control Plane & Data Plane

Gravitee provides the flexibility to choose the type of database for each specific use case, referred to as the "scope," to distribute the load and reduce pressure on a single storage point.

The scopes provided by Access Management include:

* **Management**: Data essential for the operation of the Access Management platform, such as security domains, applications, and identity providers. This scope is named Control Plane.
* **OAuth 2.0**: Access tokens and OAuth 2.0 authorization codes.
* **Gateway**: Data managed by the Access Management runtime (the Gateway) such as user profiles, scope approval, and webauthn credentials. This scope as the OAuth2 scope are managed by the Data Plane

Most deployments use a single database to host the information for both the control plane and the data plane. However, it may be beneficial to isolate the two instances in order to distribute the load more effectively.

{% hint style="warning" %}
**Note:** Prior to version 4.7, the separation of data between the control plane and the data plane was not properly implemented, and certain entities, such as user profiles, were handled within the management scope. If you had configured dedicated databases for each scope prior to upgrading to version 4.7, please refer to the [upgrade documentation](../../getting-started/install-and-upgrade-guides/4.7-upgrade-guide.md).
{% endhint %}

Starting from version 4.7.0, it is possible to define multiple Data Planes to distribute the load of different security domains across dedicated databases. This requires specifying the list of Data Planes in the configuration of the Access Management Management API. For each entry in the list, the connection details to the database associated with the scope gateway of the Gateway linked to the Data Plane must be included. When creating a security domain, you are asked to choose a Data Plane for assignment. Once the domain has been created, this choice cannot be modified.

{% hint style="info" %}
The configuration of the Gateway service remains the same, the only requirement is to provide the Data Plane id manage by the Gateway
{% endhint %}

If you wish to deploy Access Management on a single database, simply define a single entry in the Data Planes list with the identifier "default". The configuration elements for this Data Plane must correspond to the elements of the "gateway" scope. When using a single database, all three scopes should have the same connection parameters. The connection elements in the Data Planes list follow the same structure as for the [repositories](../../getting-started/configuration/configure-repositories.md). Here is an example of the configuration for such a setup:

{% tabs %}
{% tab title="MongoDB" %}
Management API configuration:

```yaml
repositories:
  # specify which scope is used as reference
  # to initialize the IdentityProviders with the "use system cluster"
  # option enabled (only management and gateway scopes are allowed as value)
  system-cluster: management
  # Management repository is used to store global configuration such as domains, clients, ...
  # This is the default configuration using MongoDB (single server)
  # For more information about MongoDB configuration, please have a look to:
  # - http://api.mongodb.org/java/current/com/mongodb/MongoClientOptions.html
  management:
    type: mongodb
    mongodb:
      dbname: gravitee-am
      host: mongohost
      port: 27017
  #    username:
  #    password:
  #    connectTimeout: 500
  #    ...
  gateway:
    type: mongodb
    use-management-settings: true
    mongodb:
      dbname: gravitee-am
      host: mongohost
      port: 27017

  oauth2:
    type: mongodb
    use-management-settings: true
    mongodb:
      dbname: gravitee-am
      host: mongohost
      port: 27017
  
dataPlanes:
  - id: default
    name: Legacy domains
    type: mongodb
    mongodb:
      dbname: gravitee-am
      host: mongohost
      port: 27017
  #    uri:
  #    username:
  #    password:
  #    connectTimeout: 500
  #    ...

```

Gateway Configuration:

```yaml
repositories:
  management:
    type: mongodb
    mongodb:
      dbname: gravitee-am
      host: mongohost
      port: 27017
      
  gateway:
    type: mongodb
    use-management-settings: true
    mongodb:
      dbname: gravitee-am
      host: mongohost
      port: 27017
      # Gateway needs to know which dataPlane to manage
      dataPlane:
        id: default

  oauth2:
    type: mongodb
    use-management-settings: true
    mongodb:
      dbname: gravitee-am
      host: mongohost
      port: 27017
```
{% endtab %}

{% tab title="RDBMS" %}
{% hint style="warning" %}
As for [reporitory](../../guides/identity-providers/database-identity-providers/jdbc.md) plugin, place the drivers in `$GRAVITEE_HOME/plugins/ext/dataplane-am-jdbc`
{% endhint %}

Management API configuration:

<pre class="language-yaml"><code class="lang-yaml">repositories:
<strong>  management:
</strong>    type: jdbc             # repository type
    jdbc:                  # jdbc/r2dbc repository
      driver:              # jdbc driver
      host:                mydbserver
      port:                1234
      database:            gravitee_am
      username:            amuser
      password:            xxxxx
      
  gateway:
    type: jdbc
    use-management-settings: true
    jdbc:                  # jdbc/r2dbc repository
      driver:              # jdbc driver
      host:                mydbserver
      port:                1234
      database:            gravitee_am
      username:            amuser
      password:            xxxxx
      
  oauth2:
    type: jdbc
    use-management-settings: true
    jdbc:                  # jdbc/r2dbc repository
      driver:              # jdbc driver
      host:                mydbserver
      port:                1234
      database:            gravitee_am
      username:            amuser
      password:            xxxxx
      
      
dataPlanes:
  - id: default
    name: Legacy domains
    type: jdbc
    jdbc:                  # jdbc/r2dbc repository
      driver:              # jdbc driver
      host:                mydbserver
      port:                1234
      database:            gravitee_am
      username:            amuser
      password:            xxxxx
</code></pre>

Gateway configuration:

```yaml
repositories:
  management:
    type: jdbc             # repository type
    jdbc:                  # jdbc/r2dbc repository
      driver:              # jdbc driver
      host:                mydbserver
      port:                1234
      database:            gravitee_am
      username:            amuser
      password:            xxxxx
      
  gateway:
    type: jdbc
    use-management-settings: true
    jdbc:                  # jdbc/r2dbc repository
      driver:              # jdbc driver
      host:                mydbserver
      port:                1234
      database:            gravitee_am
      username:            amuser
      password:            xxxxx
      # Gateway needs to know which dataPlane to manage
      dataPlane:
        id: default
        
  oauth2:
    type: jdbc
    use-management-settings: true
    jdbc:                  # jdbc/r2dbc repository
      driver:              # jdbc driver
      host:                mydbserver
      port:                1234
      database:            gravitee_am
      username:            amuser
      password:            xxxxx
```
{% endtab %}
{% endtabs %}

For more details on how to configure AM with multiple DataBase or multiple Data Planes, please refer to the [Configure Multiple Data Planes](../../getting-started/install-and-upgrade-guides/configure-multiple-data-planes.md) page.

<figure><img src="../../../4.7/.gitbook/assets/am-multi-dataplane (1).svg" alt=""><figcaption><p>Multiple DataPlane deployment</p></figcaption></figure>
