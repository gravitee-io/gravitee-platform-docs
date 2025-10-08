# MongoDB

## Overview

You can authenticate users in AM using your own MongoDB database.

## Create a MongoDB identity provider

1. Log in to AM Console.
2. Click **Settings > Providers**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Select **MongoDB** as your identity provider type and click **Next**.
5. Give your identity provider a name.
6. Configure the settings.
7. Click **Create**.

### Configuring an Identity Provider using a Data Source

### Configuring an Identity Provider using a Data Source

MongoDB Identity Providers can be configured using a Data Source defined within the Gravitee environment. For example, using the `gravitee.yaml` file or using environment variables.

Data Sources provide a reusable configuration which utilizes a shared connection for all Identity Providers using the same Data Source identifier.

{% hint style="info" %}
When a Data Source is used in the configuration of an Identity Provider, the database name always be taken from the Data Source configuration. The database name in the IDP configuration is ignored.
{% endhint %}

The following examples demonstrate an example Data Source configuration:

{% tabs %}
{% tab title="YAML" %}
```yaml
datasources:
  mongodb:
    - id: idp-connection-pool-1
      name: "IDP Connection 1" # Optional
      description: "Primary connection pool for IDP" # Optional
      settings:
        dbname: idp-db-1
        host: idp.db.host1
        port: 27016
    - id: idp-connection-pool-2
      settings:
        dbname: idp-db-2
        host: idp.db.host2
        port: 27017
```
{% endtab %}

{% tab title="Environment Variables" %}
```sh
DATASOURCES_MONGODB_0_ID=idp-connection-pool-1
DATASOURCES_MONGODB_0_NAME="IDP Connection 1"
DATASOURCES_MONGODB_0_DESCRIPTION="Primary connection pool for IDP"
DATASOURCES_MONGODB_0_SETTINGS_DBNAME=idp-db-1
DATASOURCES_MONGODB_0_SETTINGS_HOST=idp.db.host1
DATASOURCES_MONGODB_0_SETTINGS_PORT=27016

DATASOURCES_MONGODB_1_ID=idp-connection-pool-2
DATASOURCES_MONGODB_1_SETTINGS_DBNAME=idp-db-2
DATASOURCES_MONGODB_1_SETTINGS_HOST=idp.db.host2
DATASOURCES_MONGODB_1_SETTINGS_PORT=27017
```
{% endtab %}
{% endtabs %}

### Connection Precedence

The order in which Access Management decides which connection configuration to use is as follows:

1. Datasource gets the highest priority if present and possible.
2. DataPlane client for Gateway scope, if Gateway scope, DataPlane ID is set, and system cluster is used.
3. If you enable **use system cluster**, it takes precedence on the form settings.
4. If there is no datasource or you disable **use system cluster**, then the settings coming from the form are used and a specific MongoDB client with its own connection pool is created.

{% hint style="info" %}
Datasource and **use cluster system** are usable only if MongoDB is defined a backend.
{% endhint %}

## Test the connection

You can test your database connection using a web application created in AM.

1.  In AM Console, click **Applications** and select your MongoDB identity provider.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-social-idp-list.png" alt=""><figcaption><p>Select MongoDB IdP</p></figcaption></figure>
2.  Call the Login page (i.e `/oauth/authorize` endpoint) and try to sign in with the username/password form.

    If you are unable to authenticate your users, there may be a problem with the identity provider settings. Check the AM Gateway log and audit logs for more information.
