# Configure Repositories

## Overview

AM uses repositories to store different types of data (known as _scopes_).

You configure repositories in the `gravitee.yml` configuration file. The configuration can be different for each scope. AM supports the following repositories:

* [MongoDB](configure-repositories.md#mongodb)
* [JDBC](configure-repositories.md#jdbc)

For information on how to install and configure the repositories, see the relevant configuration section.

### Scopes

Examples of scopes are:

* Management: All the data needed to manage the Access Management platform, including security domains, clients, identity providers, and so on
* OAuth2: Tokens generated for OAuth2

### Supported storage

The following matrix shows the compatibility between scopes and implementations:

| Scope      | MongoDB | Redis | Elasticsearch | Cassandra |
| ---------- | ------- | ----- | ------------- | --------- |
| Management | X       | -     | -             | -         |
| OAuth2     | X       | -     | -             | -         |

* **Management:** All Access Management platform data, such as security domains, clients and identity providers.
* **OAuth2:** Tokens generated for OAuth2.

## MongoDB

The [MongoDB](https://www.mongodb.org/) repository is included with AM by default. 

{% hint style="info" %}
AM has been tested using Mongo DB in version **4.4** up to **7.0**
{% endhint %}

### Configuration

```yaml
# ===================================================================
# MINIMUM MONGO REPOSITORY PROPERTIES
#
# This is a minimal sample file declaring connection to MongoDB
# ===================================================================
management:
  type: mongodb             # repository type
  mongodb:                  # mongodb repository
    dbname:                 # mongodb name (default gravitee)
    host:                   # mongodb host (default localhost)
    port:                   # mongodb port (default 27017)
```

This is the minimum configuration you need to get started with MongoDB. You can also configure a number of other properties to fine-tune the behavior of your MongoDB database:

```yaml
# ===================================================================
# MONGO REPOSITORY PROPERTIES
#
# This is a sample file declaring all properties for MongoDB Repository
# ===================================================================
management:
  type: mongodb                 # repository type
  mongodb:                      # mongodb repository
    dbname:                     # mongodb name (default gravitee)
    host:                       # mongodb host (default localhost)
    port:                       # mongodb port (default 27017)
    username:                   # mongodb username (default null)
    password:                   # mongodb password (default null)
    connectionPerHost:          # mongodb connection per host (default 10)
    connectTimeOut:             # mongodb connection time out (default 0 -> never)
    maxWaitTime:                # mongodb max wait time (default 120000)
    socketTimeout:              # mongodb socket time out (default 0 -> never)
    maxConnectionLifeTime:      # mongodb max connection life time (default null)
    maxConnectionIdleTime:      # mongodb max connection idle time (default null)
    minHeartbeatFrequency:      # mongodb min heartbeat frequency (default null)
    description:                # mongodb description (default null)
    heartbeatConnectTimeout:    # mongodb heartbeat connection time out (default null)
    heartbeatFrequency:         # mongodb heartbeat frequency (default null)
    heartbeatsocketTimeout:     # mongodb heartbeat socket time out (default null)
    localThreshold:             # mongodb local threshold (default null)
    minConnectionsPerHost:      # mongodb min connections per host (default null)
    sslEnabled:                 # mongodb ssl mode (default false)
    threadsAllowedToBlockForConnectionMultiplier: # mongodb threads allowed to block for connection multiplier (default null)
    cursorFinalizerEnabled:     # mongodb cursor finalizer enabled (default false)
#    keystore:
#      path:                      # Path to the keystore (when sslEnabled is true, default null)
#      type:                      # Type of the keystore, supports jks, pem, pkcs12 (when sslEnabled is true, default null)
#      password:                  # KeyStore password (when sslEnabled is true, default null)
#      keyPassword:               # Password for recovering keys in the KeyStore (when sslEnabled is true, default null)
#    truststore:
#      path:                      # Path to the truststore (when sslEnabled is true, default null)
#      type:                      # Type of the truststore, supports jks, pem, pkcs12 (when sslEnabled is true, default null)
#      password:                  # Truststore password (when sslEnabled is true, default null)
```

{% hint style="info" %}
**Support for databases with MongoDB compatibility**\
Some databases are almost fully compatible with MongoDB, such as:

* DocumentDB (AWS)
* Azure Cosmos DB for MongoDB (Azure)

However, some features may not be supported, or may exhibit unexpected behavior or performance. Consequently, **MongoDB is currently the only officially supported database**.
{% endhint %}

## JDBC

You can deploy this repository plugin in AM to use the most common databases, including:

* PostgreSQL 11+
* MySQL 8.0+
* Microsoft SQL Server 2017-CU12+
* MariaDB 10.3+

{% hint style="info" %}
AM uses the JDBC and R2DBC drivers together, since AM uses [liquibase](https://www.liquibase.org/) to manage the database schema. You need to deploy the correct JDBC and R2DBC drivers for your database in your AM instance’s `plugins/ext/repository-am-jdbc` directory.
{% endhint %}

| Database             | Version tested | JDBC Driver                                                                                                                           | R2DBC Driver                                                                                                               |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Postgresql           | 11             | [Download page](https://jdbc.postgresql.org/download/)                                                                                | [Download page](https://repo1.maven.org/maven2/io/r2dbc/r2dbc-postgresql/0.8.5.RELEASE/r2dbc-postgresql-0.8.5.RELEASE.jar) |
| MySQL                | 8.0            | [Download page](https://dev.mysql.com/downloads/connector/j/)                                                                         | [Download page](https://repo1.maven.org/maven2/dev/miku/r2dbc-mysql/0.8.2.RELEASE/r2dbc-mysql-0.8.2.RELEASE.jar)           |
| MariaDB              | 10.3           | [Download page](https://downloads.mariadb.org/connector-java/)                                                                        | [Download page](https://repo1.maven.org/maven2/org/mariadb/r2dbc-mariadb/0.8.4-rc/r2dbc-mariadb-0.8.4-rc.jar)              |
| Microsoft SQL Server | 2017-CU12      | [Download page](https://docs.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server?view=sql-server-2017) | [Download page](https://repo1.maven.org/maven2/io/r2dbc/r2dbc-mssql/0.8.4.RELEASE/r2dbc-mssql-0.8.4.RELEASE.jar)           |

### Install the JDBC plugin

You need to repeat the following steps for each component (AM Gateway and AM API) where the SQL database is used.

1. Download the plugin applicable to your version of AM (take the latest maintenance release).
2. Place the zip file in the plugins directory for each component (`$GRAVITEE_HOME/plugins`).
3. Remove the `gravitee-am-repository-mongodb` zip file from the plugins directory for each component.
4. Download the JDBC and R2DBC drivers for your database version.
5. Place the drivers in `$GRAVITEE_HOME/plugins/ext/repository-am-jdbc`.
6.  Configure `gravitee.yml`:

    ```yaml
    # ===================================================================
    # MINIMUM JDBC REPOSITORY PROPERTIES
    #
    # This is a minimal sample file declaring connection to relational database
    # ===================================================================
    management:
      type: jdbc             # repository type
      jdbc:                  # jdbc/r2dbc repository
        driver:              # jdbc driver
        host:                # database hostname or IP
        port:                # database listening port
        database:            # database name to connect to
        username:            # username
        password:            # password
    ```

    This is the minimum configuration you need to get started with a relational database. You can also configure a number of other properties to fine-tune the behavior of your database:

    ```yaml
    # ===================================================================
    # JDBC REPOSITORY PROPERTIES
    #
    # This is a sample file declaring all properties for a relational database
    # ===================================================================
    management:
      type: jdbc                    # repository type
      jdbc:                         # jdbc/r2dbc repository
        driver:                     # jdbc driver
        host:                       # database hostname or IP
        port:                       # database listening port
        database:                   # database name to connect to
        username:                   # username
        password:                   # password
        acquireRetry:               # Number of retries if the first connection acquiry attempt fails (default: 1)
        initialSize:                # Initial pool size (default: 10)
        maxSize:                    # Maximum pool size (default: 10)
        maxIdleTime:                # Maximum idle time of the connection in the pool in millis (default: 1800000)
        maxLifeTime:                # Maximum life time of the connection in the pool in millis (default: 0)
        maxAcquireTime:             # Maximum time to acquire connection from pool in millis (default: 0)
        maxCreateConnectionTime:    # Maximum time to create a new connection in millis (default: 0)
        validationQuery:            # Query that will be executed to validate that a connection to the database is still alive.
        sslEnabled:                 # Enable SSL/TLS
        sslMode:                    # SSL Requirements
        sslServerCert:              # Path to Server Certificate or CA certiticate (pem format)
        tlsProtocol:                # version of TLS Protocole (TLSv1.2 or TLSv1.3)
        truststore:                 #
          path:                     # path to the truststore file (PCKS12 format)
          password:                 # password to access the truststore
    ```

#### Secured Connections

{% hint style="info" %}
AM doesn’t support client authentication using SSL Certificates.
{% endhint %}

According to the RDBMS, some SSL settings are useless or have different possible values. In this section, we will describe what parameters are possible based on the RDBMS.

{% code title="Postgres" %}
```
    sslEnabled: true                    # Enable SSL/TLS
    sslMode: verify-ca                  # SSL Requirements:
                                        # require: Encryption, but no certificate and hostname validation
                                        # verify-ca: Encryption, certificates validation, BUT no hostname validation
                                        # verify-full: Encryption, certificate validation and hostname validation
    sslServerCert: /path/to/cert.pem    # Path to Server Certificate or CA certiticate (pem format)
```
{% endcode %}

{% code title="MySQL" %}
```
    sslEnabled: true                    # Enable SSL/TLS
    sslMode: REQUIRED                   # SSL Requirements:
                                        # REQUIRED: Encryption, but no certificate and hostname validation
                                        # VERIFY_CA: Encryption, certificates validation, BUT no hostname validation
                                        # VERIFY_IDENTITY: Encryption, certificate validation and hostname validation
    sslServerCert: /path/to/cert.pem    # Path to Server Certificate or CA certiticate (pem format)
    tlsProtocol: TLSv1.2                # version of TLS Protocole (TLSv1.2 or TLSv1.3)
    truststore:                         #
      path: /path/to/ca.p12             # path to the truststore file (PCKS12 format)
      password: ******                  # password to access the truststore
```
{% endcode %}

{% code title="MariaDB" %}
```
    sslEnabled: true                    # Enable SSL/TLS
    sslMode: ENABLE_TRUST               # SSL Requirements:
                                        # ENABLE_TRUST: Encryption, but no certificate and hostname validation
                                        # ENABLE_WITHOUT_HOSTNAME_VERIFICATION: Encryption, certificates validation, BUT no hostname validation
                                        # ENABLE: Encryption, certificate validation and hostname validation
    sslServerCert: /path/to/cert.pem    # Path to Server Certificate or CA certiticate (pem format)
    tlsProtocol: TLSv1.2                # version of TLS Protocole (TLSv1.2 or TLSv1.3)
```
{% endcode %}

{% code title="SQLServer" %}
```
    sslEnabled: true                    # Enable SSL/TLS
    trustServerCertificate: false       #
    truststore:                         #
      path: /path/to/ca.p12             # path to the truststore file (PCKS12 format)
      password: ******                  # password to access the truststore
```
{% endcode %}

#### Expired Data

Some tables contain data with an expiration date. The AM management service provides a scheduled task in order to execute periodically a purge on related tables. To configure this task, you can complete the `services` section of the `gravitee.yml` AM management file.

```yaml
services:
  purge:
    enabled: true                               # enable the JDBC purge task (default: true)
    cron: 0 0 23 * * *                          # configure the frequency (default: every day at 11 PM)
    #exclude: login_attemps, refresh_token      # coma separated list of table to exclude from the purge process
```

Temporary data are stored into the following tables:

* access\_tokens,
* authorization\_codes,
* refresh\_tokens,
* scope\_approvals,
* request\_objects,
* login\_attempts,
* uma\_permission\_ticket,
* auth\_flow\_ctx

{% hint style="info" %}
If you want to clean data by yourself, please use the field `expire_at` to know if the row of the table must be deleted.
{% endhint %}

### Liquibase

AM uses [liquibase](https://www.liquibase.org/) to manage database schemas on startup of the AM services.

If you want to disable automatic update, you’ll need to add this section to your `gravitee.yml` file.

```yaml
liquibase:
  enabled: false
```

### JDBC Reporter

When AM is configured with JDBC repositories, JDBC reporter is required. You can download the reporter plugin [here](https://download.gravitee.io/#graviteeio-am/plugins/reporters/gravitee-reporter-jdbc/). To install the jdbc reporter plugin you need to repeat the following steps for each component (AM Gateway and AM API) where the SQL database is used.

1. Download the plugin applicable to your version of AM (take the latest maintenance release).
2. Place the zip file in the plugins directory for each component (`$GRAVITEE_HOME/plugins`).
3. Download the R2DBC drivers for your database version.
4. Place the drivers in `$GRAVITEE_HOME/plugins/ext/reporter-am-jdbc`.

{% hint style="info" %}
The Reporter plugin uses the `management.jdbc` configuration section to connect to the database. The user declared in the `management.jdbc` section needs the relevant permissions to create a table.
{% endhint %}

### Auto provisioning of IdentityProvider schema

Since AM 3.5, a default table may be created automatically with the following fields :

* id
* username
* password
* email
* metadata

By consequence, the user declared into the `management.jdbc` section of the `gravitee.yml` the file needs the relevant permissions to create a table. If you don’t want to generate the schema of the default JDBC IdentityProvider, you can disable this feature by setting the following property to false :

```yaml
management:
  type: jdbc
  jdbc:
    identityProvider:
      provisioning: false

```
