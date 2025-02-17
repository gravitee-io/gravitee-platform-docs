---
description: This article explains how to configure a MongoDB repository
---

# Configuring MongoDB

## Overview

The MongoDB plugin is part of the default APIM distribution.

## Supported databases

| Database | Version tested                        |
| -------- |---------------------------------------|
| MongoDB  | 4.4.x / 5.0.x / 6.0.x / 7.0.x / 8.0.x |

{% hint style="info" %}
**Support for databases with MongoDB compatibility**

Some databases are almost fully compatible with MongoDB. For example:

* DocumentDB (AWS)
* Azure Cosmos DB for MongoDB (Azure)

However, some features might not be supported or might perform differently. Consequently, MongoDB is currently the only officially supported database.
{% endhint %}

## Configuration

MongoDB is the default repository implementation used by APIM. For more information about MongoDB, go to [MongoDB](https://www.mongodb.org/).

### Mandatory configuration

The following example shows the minimum configuration that you need to configure a MongoDB database.

```yaml
# ===================================================================
# MINIMUM MONGO REPOSITORY PROPERTIES
#
# This is a minimal sample file declared connection to MongoDB
# ===================================================================
management:
  type: mongodb             # repository type
  mongodb:                  # mongodb repository
    dbname:                 # mongodb name (default gravitee)
    host:                   # mongodb host (default localhost)
    port:                   # mongodb port (default 27017)
```

### (Optional) Customizing the behavior of a MongoDB database

You can configure the following additional properties to customize the behavior of a MongoDB database:

```yaml
# ===================================================================
# MONGO REPOSITORY PROPERTIES
#
# This is a sample file declared all properties for MongoDB Repository
# ===================================================================
management:
  type: mongodb                 # repository type
  mongodb:                      # mongodb repository
    prefix:                     # collections prefix
    dbname:                     # mongodb name (default gravitee)
    host:                       # mongodb host (default localhost)
    port:                       # mongodb port (default 27017)

## Client settings
    description:                # mongodb description (default gravitee.io)
    username:                   # mongodb username (default null)
    password:                   # mongodb password (default null)
    authSource:                 # mongodb authentication source (when at least a user or a password is defined, default gravitee)
    readPreference:              # possible values are 'nearest', 'primary', 'primaryPreferred', 'secondary', 'secondaryPreferred'
    readPreferenceTags:          # list of read preference tags (https://docs.mongodb.com/manual/core/read-preference-tags/#std-label-replica-set-read-preference-tag-sets)
### Write concern
    writeConcern:               # possible values are 1,2,3... (the number of node) or 'majority' (default is 1)
    wtimeout:                   # (default is 0)
    journal:                    # (default is true)

## Socket settings
    connectTimeout:             # mongodb connection timeout (default 1000)
    socketTimeout:              # mongodb socket timeout (default 1000)

## Cluster settings
    serverSelectionTimeout:     # mongodb server selection timeout (default 1000)
    localThreshold:             # mongodb local threshold (default 15)

## Connection pool settings
    maxWaitTime:                # mongodb max wait time (default 120000)
    maxConnectionLifeTime:      # mongodb max connection life time (default 0)
    maxConnectionIdleTime:      # mongodb max connection idle time (default 0)
    connectionsPerHost:         # mongodb max connections per host (default 100)
    minConnectionsPerHost:      # mongodb min connections per host (default 0)

    ## Server settings
    heartbeatFrequency:         # mongodb heartbeat frequency (default 10000)
    minHeartbeatFrequency:      # mongodb min heartbeat frequency (default 500)

## SSL settings (Available in APIM 3.10.14+, 3.15.8+, 3.16.4+, 3.17.2+, 3.18+)
    sslEnabled:                 # mongodb ssl mode (default false)
    keystore:
      path:                     # Path to the keystore (when sslEnabled is true, default null)
      type:                     # Type of the keystore, supports jks, pem, pkcs12 (when sslEnabled is true, default null)
      password:                 # KeyStore password (when sslEnabled is true, default null)
      keyPassword:              # Password for recovering keys in the KeyStore (when sslEnabled is true, default null)
    truststore:
      path:                     # Path to the truststore (when sslEnabled is true, default null)
      type:                     # Type of the truststore, supports jks, pem, pkcs12 (when sslEnabled is true, default null)
      password:                 # Truststore password (when sslEnabled is true, default null)
## Deprecated SSL settings that will be removed in 3.19.0
    sslEnabled:                 # mongodb ssl mode (default false)
    keystore:                   # path to KeyStore (when sslEnabled is true, default null)
    keystorePassword:           # KeyStore password (when sslEnabled is true, default null)
    keyPassword:                # password for recovering keys in the KeyStore (when sslEnabled is true, default null)
```

## Using a custom prefix

You can use a custom prefix for your collection names. For example, custom prefixes are useful if you want to use the same databases for APIM and Access Management (AM).

### Using a custom prefix on a new installation

If you install APIM for the first time, you must update the following two values in the APIM Gateway and APIM API `gravitee.yml` files:

* `management.mongodb.prefix`
* `ratelimit.mongodb.prefix`

By default, these values are empty.

### Migrating an existing installation

Before running any scripts, you must create a dump of your existing database. You need to repeat these steps for both APIM Gateway and APIM API.

To prefix your collections, complete the following steps:

1. &#x20;Rename the collections. You can use the following script to rename all the collections by adding a prefix and rateLimitPrefix that you choose:

```
print('Add a prefix to all collections');

const collections = [
    'apiqualityrules',
    'applications',
    'keys',
    'identity_provider_activations',
    'users',
    'tickets',
    'genericnotificationconfigs',
    'workflows',
    'environments',
    'invitations',
    'client_registration_providers',
    'page_revisions',
    'ratingAnswers',
    'apis',
    'rating',
    'themes',
    'metadata',
    'alert_triggers',
    'parameters',
    'dashboards',
    'events',
    'identity_providers',
    'audits',
    'categories',
    'tenants',
    'portalnotifications',
    'custom_user_fields',
    'alert_events',
    'roles',
    'entrypoints',
    'metadatas',
    'memberships',
    'dictionaries',
    'qualityrules',
    'pages',
    'groups',
    'portalnotificationconfigs',
    'installation',
    'notificationTemplates',
    'commands',
    'tokens',
    'apiheaders',
    'plans',
    'tags',
    'subscriptions',
    'organizations',
];

try {
    // Use your prefix here
    const prefix = "";
    const rateLimitPrefix = "";
    collections.forEach(collectionName => {
        db.getCollection(collectionName).renameCollection(`${prefix}${collectionName}`);
    })

    db.ratelimit.renameCollection(`${rateLimitPrefix}ratelimit`);
} catch(e) {
    print(`Error while renaming collection.\nError: ${e}`);
}
```

2. In the `gravitee.yml` file, update the values of `management.mongodb.prefix` and `ratelimit.mongodb.prefix`&#x20;

## Creating an Index

To create an index, use the script available from the Gravitee MongoDB GitHub repository. To view the script, go to the [Gravitee GitHub repository](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/create-index.js).

{% hint style="warning" %}
* Use the version of the script that matches your version of APIM.
* If you use a custom prefix, set the prefix on the first line of the script.
{% endhint %}

## Security

You might need to apply specific security constraints and rules to users accessing your database. The following table summarizes how to define granular constraints for each collection.

| Component    | Read-only                           | Read-write                       |
| ------------ | ----------------------------------- | -------------------------------- |
| APIM Gateway | apis - keys - subscriptions - plans | events - ratelimit - commands    |
| APIM API     | -                                   | all collections except ratelimit |
