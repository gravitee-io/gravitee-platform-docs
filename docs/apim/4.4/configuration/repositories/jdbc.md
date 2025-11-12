---
description: This article explains how to configure a JDBC repository
---

# Configuring JDBC for Gravitee API Management

## Overview

The JDBC plugin is part of the default distribution of APIM. However, you must install the correct database driver to use JDBC as a repository.

## Supported databases

<table><thead><tr><th width="211.66666666666666">Database</th><th>Version tested</th><th>JDBC Driver</th></tr></thead><tbody><tr><td>PostgreSQL</td><td>13.x / 14.x / 15.x / 16.x / 17.x</td><td><a href="https://jdbc.postgresql.org/download/">Download page</a></td></tr><tr><td>MySQL</td><td>5.7.x / 8.0.x</td><td><a href="https://dev.mysql.com/downloads/connector/j/">Download page</a></td></tr><tr><td>MariaDB</td><td>10.4.x / 10.5.x / 10.6.x / 10.10.x / 10.11.x / 11.x</td><td><a href="https://downloads.mariadb.org/connector-java/">Download page</a></td></tr><tr><td>Microsoft SQL Server</td><td>2017-x / 2019-x / 2022-x</td><td><a href="https://docs.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server?view=sql-server-2017">Download page</a></td></tr></tbody></table>

## Install the JDBC driver

Repeat these steps for each component (APIM Gateway and APIM API) where the SQL database is used:

1. Download the JDBC driver corresponding to your database version
2. Place the driver in `$GRAVITEE_HOME/plugins/ext/repository-jdbc`
3. Configure your `gravitee.yml` files, as described in the next section

{% hint style="info" %}
**Before moving on**

If you are using Docker to install and run APIM, you should place the driver in the `plugins-ext` folder and configure it by using the Docker Compose file or command line arguments. For more information, see [Further Customization](docs/apim/4.4/getting-started/install-gravitee-api-management/installing-gravitee-api-management-on-premise/install-on-docker/further-customization.md) of a Docker installation.
{% endhint %}

## Configuration

### Mandatory configuration

Below is the minimum configuration needed to get started with a JDBC database.

```
management:
  type: jdbc             # repository type
  jdbc:                  # jdbc repository
    url:                 # jdbc url
```

### Optional configuration

You can configure the following additional properties to fine-tune your JDBC connection and control the behavior of your JDBC database.

```yaml
management:
  type: jdbc                    # repository type
  jdbc:                         # jdbc repository
    prefix:                     # tables prefix
    url:                        # jdbc url
    username:                   # jdbc username
    password:                   # jdbc password
    pool:
        autoCommit:             # jdbc auto commit (default true)
        connectionTimeout:      # jdbc connection timeout (default 10000)
        idleTimeout:            # jdbc idle timeout (default 600000)
        maxLifetime:            # jdbc max lifetime (default 1800000)
        minIdle:                # jdbc min idle (default 10)
        maxPoolSize:            # jdbc max pool size (default 10)
```

## Use a custom prefix

You can use a custom prefix for your table names. This is useful if you want to use the same databases for APIM and AM.

The following steps explain how to rename your tables with a custom prefix, using the example prefix `prefix_`.

### Use a custom prefix on a new installation

If you are installing APIM for the first time, you need to update the following two values in the APIM Gateway and APIM API `gravitee.yml` files:

* `management.jdbc.prefix`
* `ratelimit.jdbc.prefix`

By default, these values are empty.

### Migrating an existing installation

{% hint style="info" %}
**Before moving on**

Before running any scripts, you need to create a dump of your existing database. You need to repeat these steps on both APIM Gateway and APIM API.
{% endhint %}

If you are migrating an existing installation, follow these steps:

1. Update values `management.jdbc.prefix` and `ratelimit.jdbc.prefix` in your `gravitee.yml` configuration file.
2. Run the application on a new database to generate `prefix_databasechangelog`.
3. Replace the content of the `databasechangelog` table with the content you generated from `prefix_databasechangelog`.
4. Rename your tables using format `prefix_tablename`.
5. Rename your indexes using format `idx_prefix_indexname`.
6. Rename your primary keys using format `pk_prefix_pkname`.

### Database enforcing use of primary key on all tables

Some databases have an option to enforce the use of a primary key on all tables, e.g., MySQL 8.0.13+ with `sql_require_primary_key` set to `true`.

If you are using a database with such an option activated, you will need to do the following **during the installation of APIM**:

1. Disable this option.
2. Start APIM Management API to allow the database migration tool, Liquibase, to create the APIM tables and add the primary keys.
3. Re-enable this option.

{% hint style="info" %}
**APIM does not currently set primary keys when creating tables**

By default, Liquibase creates 2 tables without primary keys for its own use. To avoid a compatibility issue with Liquibase, Gravitee does not override the creation of these tables. See [here](https://forum.liquibase.org/t/why-does-databasechangelog-not-have-a-primary-key/3270) for more information.
{% endhint %}
