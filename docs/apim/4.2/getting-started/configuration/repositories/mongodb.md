---
description: This article explains how to configure a MongoDB repository
---

# MongoDB

## Overview

The MongoDB plugin is part of the default APIM distribution.

## Supported databases

| Database | Version tested                       |
| -------- |--------------------------------------|
| MongoDB  | 4.4.x / 5.0.x / 6.0.x / 7.0.x |

{% hint style="info" %}
**Support for databases with MongoDB compatibility**

Some databases are almost fully compatible with MongoDB, e.g.:

* DocumentDB (AWS)
* Azure Cosmos DB for MongoDB (Azure)

However, some features may not be supported, or may behave or perform differently. Consequently, MongoDB is currently the only officially supported database.
{% endhint %}

## Configuration

[MongoDB](https://www.mongodb.org/) is the default repository implementation used by APIM.

### Mandatory configuration

The example below shows the minimum configuration needed to get started with a MongoDB database.

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

### Optional configuration

You can configure the following additional properties to customize the behavior of a MongoDB database.

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

## Use a custom prefix

You can use a custom prefix for your collection names. For example, this is useful if you want to use the same databases for APIM and AM.

### Use a custom prefix on a new installation

If you are installing APIM for the first time, you need to update the following two values in the APIM Gateway and APIM API `gravitee.yml` files:

* `management.mongodb.prefix`
* `ratelimit.mongodb.prefix`

By default, these values are empty.

### Migrating an existing installation

Before running any scripts, you must create a dump of your existing database. You need to repeat these steps on both APIM Gateway and APIM API.

To prefix your collections, you need to rename them. You can use [this script](https://gh.gravitee.io/gravitee-io/gravitee-api-management/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/3.7.0/1-rename-collections-with-prefix.js), which renames all the collections by adding a prefix and rateLimitPrefix of your choice.

Then, update the values of `management.mongodb.prefix` and `ratelimit.mongodb.prefix` in the `gravitee.yml` file.

## Index

You can create an index using the [script](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/create-index.js) available from our MongoDB GitHub repository. You must use the correct version of this script for the version of APIM you are running. If you use a custom prefix for collections, do not forget to set it on the first line of the script.

## Security

You may need to apply specific security constraints and rules to users accessing your database. The following table summarizes how to define granular constraints per collection.

| Component    | Read-only                           | Read-write                       |
| ------------ | ----------------------------------- | -------------------------------- |
| APIM Gateway | apis - keys - subscriptions - plans | events - ratelimit - commands    |
| APIM API     | -                                   | all collections except ratelimit |
