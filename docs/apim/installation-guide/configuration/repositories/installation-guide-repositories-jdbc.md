# Overview

This repository plugin is for connecting to SQL databases.

# Supported databases

<table>
<colgroup>
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
<col style="width: 25%" />
</colgroup>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p>Database</p></td>
<td style="text-align: left;"><p>Version tested</p></td>
<td style="text-align: left;"><p>APIM Plugin</p></td>
<td style="text-align: left;"><p>JDBC Driver</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Postgresql</p></td>
<td style="text-align: left;"><p>9 / 10 / 11 / 12 / 13</p></td>
<td style="text-align: left;"><p><a
href="https://download.gravitee.io/#graviteeio-apim/plugins/repositories/gravitee-apim-repository-jdbc/">Download
the same version as your APIM platform</a></p></td>
<td style="text-align: left;"><p><a
href="https://jdbc.postgresql.org/download.html">Download
page</a></p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>MySQL</p></td>
<td style="text-align: left;"><p>5.6 / 5.7 / 8.0</p></td>
<td style="text-align: left;"><p><a
href="https://dev.mysql.com/downloads/connector/j/">Download
page</a></p></td>
<td></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>MariaDB</p></td>
<td style="text-align: left;"><p>10.1 / 10.2 / 10.3 / 10.4</p></td>
<td style="text-align: left;"><p><a
href="https://downloads.mariadb.org/connector-java/">Download
page</a></p></td>
<td></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Microsoft SQL Server</p></td>
<td style="text-align: left;"><p>2017-CU12</p></td>
<td style="text-align: left;"><p><a
href="https://docs.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server?view=sql-server-2017">Download
page</a></p></td>
<td></td>
</tr>
</tbody>
</table>

# Install the JDBC plugin

Because the plugin is part of the default distribution from APIM version
3.5, you only need to complete these steps for version 3.4 or earlier.

Repeat these steps on each component (APIM Gateway and APIM API) where
the SQL database is used.

1.  Download the plugin corresponding to your APIM version (take the
    latest maintenance release).

2.  Place the zip file in the plugin directory for each component
    (`$GRAVITEE_HOME/plugins`).

3.  Download the JDBC driver corresponding to your database version.

4.  Place the driver in `$GRAVITEE_HOME/plugins/ext/repository-jdbc`.

5.  Configure your `gravitee.yml` files, as described in the next
    section.

# Configuration

## Mandatory configuration

    management:
      type: jdbc             # repository type
      jdbc:                  # jdbc repository
        url:                 # jdbc url

## Optional configuration

The example above shows the minimum configuration needed to get started
with a JDBC database. You can configure the following additional
properties to fine-tune your JDBC connection and control the behavior of
your JDBC database.

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

# Use a custom prefix

From APIM 3.7, you can use a custom prefix for your table names. This is
useful if you want to use the same databases for APIM and AM, for
example.

The following steps explain how to rename your tables with a custom
prefix, using the prefix `prefix_` as an example.

## On a new installation

If you are installing APIM for the first time, you need to update the
following two values in the APIM Gateway and APIM API `gravitee.yml`
files:

-   `management.jdbc.prefix`

-   `ratelimit.jdbc.prefix`

By default, these values are empty.

## Migrating an existing installation

Before running any scripts, you need to create a dump of your existing
database. You need to repeat these steps on both APIM Gateway and APIM
API.

1.  Update values `management.jdbc.prefix` and `ratelimit.jdbc.prefix`
    in your `gravitee.yml` configuration file.

2.  Run the application on a new database to generate
    `prefix_databasechangelog`.

3.  Replace the content of the `databasechangelog` table with the
    content you generated from `prefix_databasechangelog`.

4.  Rename your tables using format `prefix_tablename`.

5.  Rename your indexes using format `idx_prefix_indexname`.

6.  Rename your primary keys using format `pk_prefix_pkname`.
