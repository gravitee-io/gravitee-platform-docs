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

### Elasticsearch HA Deployment

<details>

<summary>Expand to read more information on Elasticsearch HA Deployment</summary>

For production, Gravitee recommends a minimum 3-node Elasticsearch cluster with `master`, `data`, and `ingest` roles. The gateway's [Elasticsearch Reporter](../analyze-and-monitor-apis/reporters/elasticsearch-reporter.md) uses the HTTP bulk API to write to the cluster. Multiple endpoints configured in Gravitee are treated as nodes of the same cluster - Elasticsearch itself handles internal failover and load-balancing across those nodes. &#x20;

{% code title="gravitee.yml / values.yml" %}
```yaml
reporters:
  elasticsearch:
    enabled: true
    endpoints:
      - http://elasticsearch-node1:9200
      - http://elasticsearch-node2:9200
      - http://elasticsearch-node3:9200
    index: gravitee
```
{% endcode %}

#### **DR Options for Elasticsearch**

There are two supported approaches:

| Approach                                   | Description                                                                                                                                                                                                                                            | Requirement                |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| **ES Cross-Cluster Replication ("CCR")**   | Replicate Gravitee's ES indices to a secondary cluster at the Elastic level. Gravitee is untouched.                                                                                                                                                    | Elastic Enterprise license |
| **Accept analytics gap**                   | Run independent ES instances per region/DC. Analytics from the failed region will be missing for the downtime window, but new calls in the DR region will be recorded.                                                                                 | No extra cost              |
| **TCP Reporter → Logstash → secondary ES** | Keep the primary [Elasticsearch Reporter](../analyze-and-monitor-apis/reporters/elasticsearch-reporter.md), add a [TCP Reporter](../analyze-and-monitor-apis/reporters/tcp-reporter.md) → _Logstash_ pipeline to forward data to a second ES instance. | Logstash infrastructure    |

The officially recommended approach is: _keep Gravitee pointing to one ES cluster and use Elastic-level replication (CCR or Cross-Cluster Search) to aggregate data elsewhere._

</details>

### Redis HA Deployment

<details>

<summary>Expand to read more information on Redis HA Deployment</summary>

Redis is a soft dependency used for:

* **Rate limiting counters** (shared across all gateway instances)
* **Caching** (e.g., JWT token caching, Data Cache policy)
* **Distributed synchronisation** (as of APIM 4.12 - API definitions shared across gateways via Redis)

If Redis goes down, gateways continue to serve API traffic - rate limiting simply stops being enforced for the downtime window. This is a less critical failure mode than losing MongoDB.

**Supported Topologies**

For APIM, three Redis topologies are supported:

<table><thead><tr><th width="154.02685546875">Mode</th><th width="171.376708984375">HA?</th><th>Notes</th></tr></thead><tbody><tr><td><strong>Standalone</strong></td><td>No</td><td>Simple single instance; for dev/test</td></tr><tr><td><strong>Sentinel</strong></td><td>Yes</td><td>Most common HA pattern in production; master/replica with automatic failover</td></tr><tr><td><strong>Cluster</strong></td><td>Yes (APIM 4.12+)</td><td>Horizontally scalable; mutually exclusive with Sentinel</td></tr></tbody></table>

**Cross-Region Redis: Not Recommended**

Redis should be co-located with the gateway cluster in each region. Cross-region Redis synchronisation is not recommended due to latency, and splitting Sentinel nodes across regions is explicitly discouraged. If gateways fail over to a secondary region with its own Redis instance, rate limit counters simply reset to zero - the counters from the primary region are not carried over.&#x20;

**Redis Backup**

Redis holds ephemeral state (rate limit counters, cache entries). There is no official Gravitee guidance for backing up Redis data as part of a DR procedure - the expectation is that counter state is lost during a failover and counters simply restart. This is acceptable for most deployments since the impact is a temporary relaxation of rate limits.

</details>

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

<details>

<summary>Expand for more information on Elasticsearch/OpenSearch Backup</summary>

### Elasticsearch/OpenSearch Backup

Elasticsearch/OpenSearch only contains analytics data, such as API request logs, metrics, and health checks. It does not store API configuration or subscription data. This is a critical distinction for DR prioritization: if Elasticsearch/OpenSearch goes down, gateways continue to serve traffic; only the analytics UI stops showing data.

Elasticsearch indices are not included in the MongoDB/PostgreSQL database backup. You should use Elasticsearch's native [snapshot and restore](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshot-restore.html) functionality if analytics data retention across a DR event is required.&#x20;



</details>

<details>

<summary>Expand for more information on Redis Backup</summary>

### Redis Backup

Redis holds ephemeral state (rate limit counters, cache entries). There is no official Gravitee guidance for backing up Redis data as part of a DR procedure - the expectation is that counter state is lost during a failover and counters simply restart. This is acceptable for most deployments since the impact is a temporary relaxation of rate limits.



</details>

***

## Recovery Procedures

### Critical Order of Operations

{% hint style="danger" %}
**Do not start Gravitee components against an empty database first, then restore on top.**&#x20;

The correct order is: **restore the database first, then start the Gravitee components.**
{% endhint %}

If components start against an empty DB, they pre-populate it with new unique IDs. Restoring on top of that creates duplicate, broken references.

### Recovery Procedure Sequence

1. Restore MongoDB/PostgreSQL with `gravitee` metadata database
2. Start Management API (one instance first)
3. Start Gateway instances (they will reload config from DB)
4. Start/failover Redis (Sentinel or Cluster)&#x20;
   1. Rate limiting resumes; counters restart from zero
5. Start/failover Elasticsearch cluster
   1. Analytics resume for new traffic
   2. Historical analytics gap during downtime (unless Elasticsearch CCR was active)
6. Update environment-specific URLs (entrypoints, callbacks)
7. Restart portal/console pods if needed
8. Validate end-to-end (APIs, auth flows, analytics)

### APIM Step-by-Step Recovery

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
