---
hidden: true
noIndex: true
---

# Test the election of a new master node

## Overview&#x20;

## Prerequisites&#x20;

## Test the election of a new master node&#x20;

1.  Start all services expect the secondary gateway using the following command:<br>

    ```
    export APIM_REGISTRY=graviteeio.azurecr.io && export APIM_VERSION=master-latest && docker compose up -d redis-stack mongodb elasticsearch gateway_primary management_api management_ui
    ```
2.  Start secondary Gateway using the following command:<br>

    ```
    export APIM_REGISTRY=graviteeio.azurecr.io && export APIM_VERSION=master-latest && docker compose up -d gateway_secondary
    ```

<figure><img src="../../../.gitbook/assets/unknown (6).png" alt=""><figcaption></figcaption></figure>

3.  Verify that the primary gateway has become the master node using the following command:<br>

    ```
    ```

    \
    You see the following output:<br>

    ```
    2025-10-21 13:41:13 08:11:13.810 [hz.gio-cluster-hz-instance.event-3] [] INFO  i.g.n.p.c.h.HazelcastClusterManager - A node joined the cluster: MembershipEvent {member=Member [gio_apim_gateway_secondary]:5701 - 30256095-b544-4cfb-9eea-2e25538ab863, type=added, members=[Member [gio_apim_gateway_primary]:5701 - c8de5ab9-1a84-4bac-971b-c0fc46068dcf this, Member [gio_apim_gateway_secondary]:5701 - 30256095-b544-4cfb-9eea-2e25538ab863]}
    ```



4.  Verify that the secondary gateway is syncing with Redis using the following command:<br>

    ```
    ```

    \
    You see the following output<br>

    ```
    2025-10-21 13:41:15 08:11:15.747 [gio.sync-deployer-0] [] INFO  i.g.g.s.s.p.d.s.AbstractDistributedSynchronizer - 1 api(s) synchronized in 155ms
    2025-10-21 13:41:15 08:11:15.748 [gio.sync-deployer-0] [] INFO  i.g.g.s.s.p.d.s.AbstractDistributedSynchronizer - 0 subscription(s) synchronized in 0ms
    2025-10-21 13:41:15 08:11:15.749 [gio.sync-deployer-0] [] INFO  i.g.g.s.s.p.d.s.AbstractDistributedSynchronizer - 0 api_key(s) synchronized in 0ms
    2025-10-21 13:41:15 08:11:15.749 [gio.sync-deployer-0] [] INFO  i.g.g.s.s.p.r.DefaultSyncManager - Sync service has been scheduled with delay [5000 MILLISECONDS]
    ```
5.  Verify that the master node wrote to Redis using the following command:<br>

    ```
    ```

    \
    You see the following output:<br>

    ```
    ```
6.  Stop the master gateway using the following command:<br>

    ```
    ```
7. Check the logs of secondary Gateway to ensure that the secondary Gateway left the cluster. This indicates that it has become the Master node.<br>

<figure><img src="../../../.gitbook/assets/unknown (7).png" alt=""><figcaption></figcaption></figure>

4.  Call your API through the secondary company using the following command:<br>

    ```
    ```

    \
    You see the following response:<br>

    ```
    ```
5.  Restart the the first Gateway using the following command:<br>

    ```
    ```

## Verification

Verify the logs of the first Gateway using the the following command:<br>

```
```

\
You see the following logs:

```
 a node joined the cluster
```
