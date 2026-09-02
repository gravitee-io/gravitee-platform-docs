---
description: >-
  Describes disaster recovery deployment options and backup & restore
  procedures, for a fully self-hosted Gravitee APIM deployment.
---

# Disaster Recovery (Backup and Restore)

## Disaster Recovery Deployment Options

Gravitee APIM (both control plane and data plane) can be deployed in active/active or active/passive deployments:

### Active/Active

* Multiple gateway instances run simultaneously across regions or data centres, all serving live traffic.
* A global load balancer distributes traffic across all active gateways.
* If one gateway or region fails, the load balancer routes all traffic to remaining instances - near-zero downtime.
* Gravitee Gateways cache their API configuration at startup and can continue serving traffic even if temporarily disconnected from the database/control plane.
* For the management plane (UI Console, Management API, and Developer Portal), you can also run Active/Active with a shared replicated database.

### Active/Passive

* A primary environment serves all traffic; a secondary (passive/standby) environment is kept in sync but idle.
* On primary failure, traffic is rerouted to the passive environment.
* The passive environment comes online after a switchover - involves some downtime (RTO depends on your routing automation).
* Kept in sync via database replication or periodic restore from backups.

***

## Backup Procedures

### What to Back Up

All Gravitee configuration is stored in the database. For a complete backup of a fully self-hosted Gravitee APIM platform, you need to back up:

* `gravitee` - the Gravitee APIM metadata database

You do not need to back up MongoDB system databases (`admin`, `config`, `local`).&#x20;

{% hint style="info" %}
Ensure you back up the installation method, such as the Helm `values.yml` file, as well as any additional plugins added to either the Management API or Gateway nodes.
{% endhint %}

#### MongoDB (`mongodump`)

```bash
mongodump --uri=mongodb://<host>:27017/gravitee
```

#### PostgreSQL (`pg_dump`)

```bash
pg_dump \
  -U <db_user> gravitee \
  -h $HOST \
  -p 5432 \
  -Fd \
  -j 3 \
  --no-owner \
  --no-privileges \
  --verbose \
  -f /backup/gravitee_pgdump
```

### Backup Strategy Recommendations

* Full backup frequency: at minimum daily; ideally every few hours for lower RPO.
* For PostgreSQL, `pg_dump` exports schema and index definitions, so no manual re-indexing is needed after restore.
* For disaster recovery scenarios, backup the DB at the database/volume level (e.g., VM snapshots, RDS snapshots, or Kubernetes PV snapshots) in addition to logical dumps.

***

## Recovery Procedures

### Critical Order of Operations

{% hint style="danger" %}
**Do not start Gravitee components against an empty database first, then restore on top.**&#x20;

The correct order is: **restore the database first, then start the Gravitee components.**
{% endhint %}

If components start against an empty DB, they pre-populate it with new unique IDs. Restoring on top of that creates duplicate, broken references.

### Step-by-Step Recovery

1. Create the target database and user with the required permissions.
2.  Restore the dump into the target database:

    MongoDB:

    ```bash
    mongorestore --drop \
      --uri=mongodb://<target-host>:27017/?replicaset=rs0 \
      --nsInclude gravitee.*
    ```

    PostgreSQL:

    ```bash
    pg_restore \
      -U <db_user> \
      -d gravitee \
      -h <target-host> \
      --no-owner --no-acl \
      /backup/gravitee_pgdump
    ```
3.  Point Gravitee components at the restored database by updating the DB connection URI in your `gravitee.yml` or Helm `values.yml`:

    ```yaml
    gravitee_management_mongodb_uri: mongodb://<new-host>:27017/gravitee
    gravitee_ratelimit_mongodb_uri: mongodb://<new-host>:27017/gravitee
    ```
4. Start only one Management API instance first during cutover to avoid concurrent schema changes.
5. Update environment-specific URLs: update callback URLs, entrypoints, and backend URLs that reference the old environment to reflect the new region/host.
6. Restart pods/services: after a DB restore, the UI Console or Developer Portal may enter maintenance mode; a pod restart brings it back to normal.
7. Validate end-to-end: confirm APIs are visible, applications are functional, and authentication/token flows work correctly.

### Tip for Helm-Based Deployments

If you need to restore before components start, temporarily disable all non-DB components in your Helm `values.yml`, restore, then re-enable:

```yaml
api:
  enabled: false
gateway:
  enabled: false
ui:
  enabled: false
portal:
  enabled: false
```

Run `helm upgrade` (not `helm uninstall`) after restore to bring components back.
