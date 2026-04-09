---
description: An overview about jdbc.
metaLinks:
  alternates:
    - jdbc.md
---

# JDBC

## Overview

Gravitee APIM can use a variety of JDBC repositories for its Configuration Database, instead of the default MongoDB service.

From Gravitee APIM v4.11, the default images now include the following JDBC drivers:

* PostgreSQL JDBC Driver (42.7.7+)
* MariaDB Connector/J (3.5.6+), and&#x20;
* Microsoft JDBC Driver for SQL Server (12.10.2.jre11+)

{% hint style="warning" %}
Due to licensing restrictions, MySQL drivers are intentionally not bundled in the default images.  You must follow these [steps](jdbc.md#install-the-mysql-jdbc-driver) to manually include the relevant MySQL Connector/J driver.
{% endhint %}

## Supported Databases

In addition to the default MongoDB service, Gravitee supports other JDBC drivers for its Configuration Database.

<table><thead><tr><th width="211.66666666666666">Database</th><th>Versions tested</th><th>JDBC Driver</th></tr></thead><tbody><tr><td>MariaDB</td><td>10.4.x / 10.5.x / 10.6.x / 10.10.x / 10.11.x / 11.x</td><td><a href="https://mariadb.org/download/?t=connector&#x26;p=connector-java&#x26;r=3.5.8&#x26;os=source">Download page</a></td></tr><tr><td>Microsoft SQL Server</td><td>2017-x / 2019-x / 2022-x</td><td><a href="https://docs.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server">Download page</a></td></tr><tr><td>MySQL</td><td>8.0.x/8.2.x</td><td><a href="https://dev.mysql.com/downloads/connector/j/">Download page</a></td></tr><tr><td>PostgreSQL</td><td>11.x / 12.x / 13.x / 14.x / 15.x/ 16.x/ 17.x</td><td><a href="https://jdbc.postgresql.org/download/">Download page</a></td></tr></tbody></table>

## Install the MySQL JDBC driver

{% hint style="info" %}
This section only applies if you want to use MySQL as the Configuration Database for Gravitee APIM.
{% endhint %}

Because licensing restrictions prevent the inclusion of the MySQL JDBC driver in the default Gravitee images, you must manually include the driver.

If you are configuring Gravitee with the Helm chart and using the MySQL JDBC, please refer to these [steps](jdbc.md#mysql-configuration-with-gravitee-helm-chart).  Otherwise, repeat these steps for each component (APIM Gateway and APIM Management API) where the MySQL database is used:

1. Download the JDBC driver corresponding to your database version
2. Place the driver in `$GRAVITEE_HOME/plugins/ext/repository-jdbc`
3. Configure your `gravitee.yml` files, as described in the next section

{% hint style="info" %}
**Before moving on**

If you're using Docker to install and run APIM, place the driver in the `plugins/ext/repository-jdbc/` subfolder of the container's `GRAVITEEIO_HOME` directory (`/opt/graviteeio-gateway/plugins/ext/repository-jdbc/` for the Gateway and `/opt/graviteeio-management-api/plugins/ext/repository-jdbc/` for the Management API), and configure it through the Docker Compose file or command-line arguments. For more information, see [Customize you Installation](/broken/pages/SoPPbC6OYm5BmOUdYZYR).
{% endhint %}

## Configuration

### Mandatory configuration

Below is the minimum configuration needed to get started with a JDBC database.

{% code title="gravitee.yml" %}
```yaml
management:
  type: jdbc             # repository type
  jdbc:                  # jdbc repository
    url:                 # jdbc url
```
{% endcode %}

### Optional configuration

You can configure the following additional properties to fine-tune your JDBC connection and control the behavior of your JDBC database.

{% code title="gravitee.yml" %}
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
{% endcode %}

## Gravitee Helm chart JDBC configuration details

{% hint style="info" %}
This section only applies if you are using the Gravitee Helm chart to install a self-hosted instance of Gravitee APIM.
{% endhint %}

From Gravitee APIM v4.11, the Gravitee Helm chart now includes additional startup behavior to auto-select the appropriate JDBC driver, and is derived from `jdbc.url` and `jdbc.driverSource`:

* `jdbc.driverSource=auto` uses bundled PostgreSQL, MariaDB, and Microsoft SQL Server drivers, but uses _startup download_ for MySQL and any other custom JDBC family
* `jdbc.driverSource=download` always downloads the driver from `jdbc.driver` at startup
* `jdbc.driverSource=image` copies the driver at startup from a dedicated customer-provided JDBC image (from `/drivers/mysql-connector-j.jar`).

When `jdbc.driverSource=auto`:

* MySQL still requires `jdbc.driver`
* PostgreSQL, MariaDB, and SQL Server do not use `jdbc.driver`

### PostgreSQL Configuration (with Gravitee Helm Chart)

For PostgreSQL, use the information below in `values.yml` and replace the `username`, `password`, `URL` and `database name` with details for your specific instance.

{% code title="values.yml" %}
```yaml
jdbc:
  driverSource: auto
  url: jdbc:postgresql://postgres-apim-postgresql:5432/graviteeapim
  username: postgres
  password: P@ssw0rd
management:
  type: jdbc
```
{% endcode %}

### MariaDB Configuration (with Gravitee Helm Chart)

{% code title="values.yml" %}
```yaml
jdbc:
  driverSource: auto
  url: jdbc:mariadb://mariadb-apim-mariadb:3306/graviteeapim
  username: gravitee
  password: P@ssw0rd
management:
  type: jdbc
```
{% endcode %}

### Microsoft SQL Server Configuration (with Gravitee Helm Chart)

{% code title="values.yml" %}
```yaml
jdbc:
  driverSource: auto
  url: jdbc:sqlserver://sqlserver-apim-mssql:1433;databaseName=graviteeapim
  username: sa
  password: P@ssw0rd
management:
  type: jdbc
```
{% endcode %}

### MySQL Configuration (with Gravitee Helm Chart)

For MySQL, the recommended path is a minimal JDBC image. This avoids outbound downloads at startup without requiring custom API or Gateway application images. The dedicated image must contain the MySQL driver at `/drivers/mysql-connector-j.jar`.

```
FROM busybox:1.36
COPY mysql-connector-j-<version>.jar /drivers/mysql-connector-j.jar
```

The copied file must be readable by UID `1001`. Pod image pull secrets already apply to initContainers, so private registries for this JDBC image use the existing API and Gateway image pull secret configuration.

{% code title="values.yml" %}
```yaml
jdbc:
  driverSource: image
  url: jdbc:mysql://mysql-apim-mysql:3306/graviteeapim
  username: gravitee
  password: P@ssw0rd
  image:
    repository: customer/mysql-jdbc
    tag: 9.3.0
    pullPolicy: IfNotPresent
management:
  type: jdbc
```
{% endcode %}

The API upgrader follows the same JDBC behavior automatically.

For MySQL fallback mode, keep the current startup download path:

{% code title="values.yml" %}
```yaml
jdbc:
  driverSource: download
  url: jdbc:mysql://mysql-apim-mysql:3306/graviteeapim
  driver: https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/9.3.0/mysql-connector-j-9.3.0.jar
  username: gravitee
  password: P@ssw0rd
management:
  type: jdbc
```
{% endcode %}

### Other Configuration (with Gravitee Helm Chart)

For any other JDBC driver, keep `jdbc.driver` set to a URL that can be downloaded at startup:

{% code title="values.yml" %}
```yaml
jdbc:
  driverSource: auto
  url: jdbc:customdb://customdb:1234/graviteeapim
  driver: https://artifacts.example.com/jdbc/customdb-driver.jar
  username: gravitee
  password: P@ssw0rd
management:
  type: jdbc
```
{% endcode %}

## Other Important Information

### Use a custom prefix

You can use a custom prefix for your table names. This is useful if you want to use the same databases for APIM and AM.

The following steps explain how to rename your tables with a custom prefix, using the example prefix `prefix_`.

#### Use a custom prefix on a new installation

If you are installing APIM for the first time, you need to update the following two values in the APIM Gateway and APIM API `gravitee.yml` files:

* `management.jdbc.prefix`
* `ratelimit.jdbc.prefix`

By default, these values are empty.

### Migrating an existing installation

{% hint style="info" %}
**Before moving on**

Before running any scripts, you need to create a dump of your existing database. You need to repeat these steps on both APIM Gateway and APIM Management API.
{% endhint %}

If you are migrating an existing installation, follow these steps:

1. Update values `management.jdbc.prefix` and `ratelimit.jdbc.prefix` in your `gravitee.yml` configuration file.
2. Run the application on a new database to generate `prefix_databasechangelog`.
3. Replace the content of the `databasechangelog` table with the content you generated from `prefix_databasechangelog`.
4. Rename your tables using format `prefix_tablename`.
5. Rename your indexes using format `idx_prefix_indexname`.
6. Rename your primary keys using format `pk_prefix_pkname`.

### Database enforcing use of primary key on all tables

{% hint style="warning" %}
**APIM does not currently set primary keys when creating tables**

By default, Liquibase creates 2 tables without primary keys for its own use. To avoid a compatibility issue with Liquibase, Gravitee does not override the creation of these tables. See [here](https://forum.liquibase.org/t/why-does-databasechangelog-not-have-a-primary-key/3270) for more information.
{% endhint %}

Some databases have an option to enforce the use of a primary key on all tables, e.g., MySQL 8.0.13+ with `sql_require_primary_key` set to `true`.

**Option 1:** If you are using a database with such an option activated, you will need to do the following during the installation of APIM:

1. Disable this option.
2. Start APIM Management API to allow the database migration tool, Liquibase, to create the APIM tables and add the primary keys.
3. Re-enable this option.

**Option 2:** Another option is to use _sessionVariables_ in your MySQL JDBC connection string:

> SUPER, SYSTEM\_VARIABLES\_ADMIN or SESSION\_VARIABLES\_ADMIN privilege(s) are required for this operation.

1. Before you attempt the installation, modify your `management: jdbc: url:` connection string to include `?sessionVariables=sql_require_primary_key=OFF`
   1. Example: `jdbc:mysql://hostname:3306/gravitee?sessionVariables=sql_require_primary_key=OFF`
2. After the installation and successful startup of all Gravitee components, you can then remove `?sessionVariables=sql_require_primary_key=OFF`

During future upgrades, you will need add back `?sessionVariables=sql_require_primary_key=OFF` during the upgrade only.

:information\_source: More information:  [https://dev.mysql.com/doc/connector-j/en/connector-j-connp-props-session.html](https://dev.mysql.com/doc/connector-j/en/connector-j-connp-props-session.html)

