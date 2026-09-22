---
description: API Management 4.13 applies its JDBC schema at startup unless you turn that off. Learn which components own a schema and how to apply the migrations yourself.
---

# Apply schema migrations manually

APIM applies its JDBC schema with Liquibase when it starts. An installation that sets `management.jdbc.liquibase` to `false` applies the migrations by hand instead, and that covers every Gamma module that stores data, not only APIM itself.

## When you need this

This page applies to the JDBC management repository only, and only when `management.jdbc.liquibase` is `false`. The setting defaults to `true` for APIM and for each Gamma module, so an installation that leaves it alone needs nothing here.

Turning it off hands you the timing. Nothing changes the schema on its own, so each change lands in a window you choose.

## What owns a schema

APIM isn't the only component that migrates the management database. Each Gamma module that stores data keeps its own migration history, in its own tracking tables, independently of APIM and of every other module. Running APIM's changelog doesn't migrate the modules, so each one is a separate run.

<table>
    <thead>
        <tr>
            <th width="220">Component</th>
            <th width="215">Changelog</th>
            <th>Tracking tables</th>
            <th width="175">Prefix parameter</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>APIM</td>
            <td><code>liquibase/master.yml</code></td>
            <td><code>{prefix}databasechangelog</code> and <code>{prefix}databasechangeloglock</code></td>
            <td><code>gravitee_prefix</code> and <code>gravitee_rate_limit_prefix</code></td>
        </tr>
        <tr>
            <td>Event Stream Management</td>
            <td><code>liquibase/esm/master.yml</code></td>
            <td><code>{prefix}esm_databasechangelog</code> and <code>{prefix}esm_databasechangeloglock</code></td>
            <td><code>esm_prefix</code></td>
        </tr>
        <tr>
            <td>AI Management</td>
            <td><code>liquibase/aim/master.yml</code></td>
            <td><code>{prefix}aim_databasechangelog</code> and <code>{prefix}aim_databasechangeloglock</code></td>
            <td><code>aim_prefix</code></td>
        </tr>
    </tbody>
</table>

`{prefix}` is the value of `management.jdbc.prefix`, which is empty unless you set one. See [Use a custom prefix](jdbc.md#use-a-custom-prefix).

The modules bundled with this release follow the same shape. A module with the id `<id>` keeps its changelog at `liquibase/<id>/master.yml`, tracks it in `{prefix}<id>_databasechangelog` and `{prefix}<id>_databasechangeloglock`, and takes an `<id>_prefix` parameter. Nothing enforces that shape, and a module that stores nothing owns no changelog and needs no run. Take the list of entry points, and the arguments each one takes, from the `README` of the archive described below rather than from this table.

## Get the changelogs

The migrations ship as one archive, `gravitee-apim-jdbc-migrations-<version>.zip`, published with each APIM release under [Resources](https://download.gravitee.io/#graviteeio-apim/resources/gravitee-apim-jdbc-migrations/) on the Gravitee download website. The version in the filename is the APIM version the archive was built from. The archive carries the changelogs of APIM and of the Gamma modules bundled with that release, at the versions that release bundles. Collecting them from each installed plugin yourself isn't necessary.

The archive carries its own `README` at its root, and that `README` lists the entry points that ship in the archive and holds the Liquibase commands for reviewing and applying each one. Read it before you run anything.

{% hint style="warning" %}
The archive describes one combination of APIM and module versions. If you upgraded a module on its own, use the changelogs of the version you actually run, which ship inside that plugin's own archive.
{% endhint %}

## Pass the prefix parameters

Almost every migration names its tables through a parameter rather than a literal, and Liquibase doesn't stop when a parameter is missing. What happens instead depends on whether the database was already migrated:

* On a first run against a database that has never been migrated, Liquibase leaves the placeholder in place and creates objects whose names contain it literally, such as a table named `${esm_prefix}kafka_explorer_connections`. The run reports success, the module then reports its table as missing, as described in [Symptoms of a skipped migration](#symptoms-of-a-skipped-migration), and the misnamed table is yours to drop.
* On a run against a database that the application already migrated, the unresolved placeholder changes the checksum of every entry, and Liquibase reports a long list of checksum validation failures against a database that isn't corrupt.

Pass every prefix parameter on every run. When you use no prefix, pass an empty value.

The tracking table names carry the prefix too. The application derives them from `management.jdbc.prefix`, so a run that leaves them at Liquibase's default opens a different table from the one the application writes to. It then finds that table empty and repeats every migration against an already-migrated database.

{% hint style="danger" %}
Don't move the files inside the archive's `liquibase/` directory. Liquibase identifies each migration partly by the path of the changelog it came from, and it stores that path in the tracking table. The paths in the archive are the ones the application records when it migrates itself. Re-rooting them makes your run record different paths, after which the application treats nothing as applied and repeats everything. Nothing reports an error at the time of your run.
{% endhint %}

## What Event Stream Management adds

Event Stream Management stores the saved Kafka Explorer connections, and nothing else, in one table named `{prefix}kafka_explorer_connections`. Its changelog is `liquibase/esm/master.yml` and its parameter is `esm_prefix`.

Each stored connection includes its security overlay, which isn't encrypted at rest. That covers the SASL passwords, OAuth client secrets, bearer tokens, and store passwords entered when the connection was created. Treat the management database, and its backups, as holding Kafka credentials, and restrict access to them accordingly.

## Recover a stale changelog lock

Liquibase takes a lock in the component's lock table before it applies anything, so that two instances migrating the same database at once can't collide. An instance that dies mid-migration leaves that lock held, and every later instance waits behind it.

The wait is bounded rather than indefinite. Event Stream Management waits up to five minutes for the lock, and makes three attempts in all before it gives up. A lock nobody is going to release therefore delays the module by around fifteen minutes. The module then fails to start, and the Management API logs `Unable to apply ESM liquibase changelogs`. Neither the wait nor the attempt count is configurable. The rest of the Management API keeps running, but the module doesn't recover on its own. Its pages stay unavailable until you clear the lock and restart the Management API.

To find out whether a lock is stale, read the component's lock table. With no prefix configured, the Event Stream Management lock table is named `esm_databasechangeloglock`:

```sql
SELECT * FROM esm_databasechangeloglock;
```

When `management.jdbc.prefix` is set, prepend its value to the table name.

A locked row means either that a migration is running or that the instance holding it is gone. The row records which host took the lock and when, so compare that against the instances you're actually running, and their start times, before you decide.

To clear a lock you've confirmed is stale, use Liquibase's own `release-locks` command against the same lock table name, rather than editing the row by hand. See the [Liquibase documentation](https://docs.liquibase.com/commands/maintenance/release-locks.html). Then restart the Management API, because a module that gave up on the lock doesn't retry until it starts again.

## Symptoms of a skipped migration

A module whose migration was skipped still starts. Nothing fails at boot, the skip is recorded in the Management API log, and the tables simply aren't there.

The failure surfaces later, when someone uses the feature. For Event Stream Management, the Kafka Explorer pages return an error that names the missing table and the setting that skipped it:

```
ESM table [kafka_explorer_connections] does not exist. This is the expected symptom of the
module's own liquibase migration having been skipped (jdbc.liquibase=false /
repositories.management.jdbc.liquibase=false): apply the ESM changelog
(liquibase/esm/master.yml) against this datasource manually, or re-enable jdbc.liquibase
and restart.
```

A database the Management API can't reach at all reports a different error, which names the table but not the database's address.

## Verification

To verify a component's schema is applied, follow these steps:

1. Connect to the management database as a user that can read its tables.
2. Confirm the component's tracking table exists and holds one row per applied migration. For Event Stream Management, that's `{prefix}esm_databasechangelog`.
3. Confirm the component's own tables exist. For Event Stream Management, that's `{prefix}kafka_explorer_connections`.
4. Open the feature in the console and confirm it loads. For Event Stream Management, open the Kafka Explorer and confirm the connection list renders instead of returning an error.
