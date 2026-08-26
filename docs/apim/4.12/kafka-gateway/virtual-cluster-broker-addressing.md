---
description: >-
  How the Kafka Gateway rewrites broker IDs when a Kafka API is backed by a Virtual Cluster, and
  which DNS entries and certificate SANs that requires.
---

# Virtual Cluster Broker Addressing

## Overview

A Virtual Cluster presents several backend Kafka clusters to clients as one. Kafka requires every broker in a cluster to have a unique ID, but two backends will happily both have a `broker.id=0`. The Gateway therefore rewrites broker IDs before advertising them, which means **the IDs clients see are not the IDs configured on your brokers**.

This changes which DNS entries you need. It is the one part of the [Kafka Gateway host routing setup](configure-the-kafka-client-and-gateway.md) that a Virtual Cluster does not inherit unchanged, so read this page before exposing a Kafka API backed by a Virtual Cluster.

## How broker IDs are rewritten

Each backend cluster is assigned a block of 10,000 IDs, in the order the backends are listed in the Virtual Cluster configuration:

```
advertised broker ID = (backend position + 1) × 10000 + real broker ID
```

`backend position` is zero-based, so:

| Backend position | Real broker IDs | Advertised IDs         |
| ---------------- | --------------- | ---------------------- |
| 0 (first listed) | 0, 1, 2, …      | 10000, 10001, 10002, … |
| 1                | 0, 1, 2, …      | 20000, 20001, 20002, … |
| 2                | 0, 1, 2, …      | 30000, 30001, 30002, … |

The same rewriting applies everywhere a broker ID is visible to a client: `Metadata` responses, `DescribeCluster`, partition leaders and replicas, `FindCoordinator`, and the `resourceName` of a `BROKER` config resource.

## DNS entries

The broker hostname pattern is unchanged — by default `{brokerPrefix}{brokerId}{domainSeparator}{apiHost}.{defaultDomain}` — but `{brokerId}` carries the **advertised** ID, not the real one.

For example, with two backends of 75 brokers each (real IDs 0–74), a Kafka API whose host prefix is `myapi`, and a default domain of `mycompany.org`:

| Entry                                                                     | Resolves to             |
| ------------------------------------------------------------------------- | ----------------------- |
| `myapi.mycompany.org`                                                     | the Gateway (bootstrap) |
| `broker-10000-myapi.mycompany.org` … `broker-10074-myapi.mycompany.org`   | the Gateway (backend 0) |
| `broker-20000-myapi.mycompany.org` … `broker-20074-myapi.mycompany.org`   | the Gateway (backend 1) |

All of them resolve to the same Gateway address — the Gateway tells the backends apart from the SNI, not from the IP. The same hostnames must also appear in the SAN of the certificate the Gateway presents.

{% hint style="info" %}
A wildcard DNS entry and a wildcard certificate covering `*.mycompany.org` cover every broker at once and keep working when you add a backend or scale one out. With per-broker entries, you must create new ones each time the topology changes. Use wildcards wherever your DNS and certificate policy allow it.
{% endhint %}

If you are moving an existing single-backend Kafka API to a Virtual Cluster, the broker entries you already have (`broker-0-…` through `broker-74-…`) no longer match anything the Virtual Cluster advertises. You must **add** the rewritten ones.

## Clients reaching an unadvertised broker hostname

A client connecting on a broker hostname whose ID falls outside every advertised block — an entry left over from a single-backend deployment, most often — cannot be placed on any backend. The connection is closed without a response, and the client waits out its own timeout rather than failing fast.

This is the usual shape of "bootstrap works, producing does not": producing is the first operation that needs a per-broker connection, so a stale set of broker entries surfaces there and nowhere earlier.

Fix the DNS entries rather than the clients: they must carry the rewritten IDs the Virtual Cluster advertises, as described above.

## Backend broker ID limit

Every backend broker ID must be **below 10000**, otherwise it collides with the next backend's block. Higher IDs are rejected at runtime. Single- and double-digit broker IDs are the convention in most deployments, and Kafka's own generated IDs start at 1001, so this rarely applies — but check it if you are onboarding a cluster with hand-assigned high IDs.

## Troubleshooting

| Symptom                                                                | Likely cause                                                                                                                                                                       |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bootstrap and topic listing work, but producing and consuming time out | The DNS entries for the advertised IDs do not exist, or still carry the numbering of a single-backend deployment. Clients resolve the bootstrap fine, then fail on the per-broker hostnames returned in metadata. |
| Connections fail only for one backend's brokers                        | That backend's block of entries is missing. Check the position of the backend in the Virtual Cluster configuration, since the block follows the listed order.                       |
| TLS handshake failures on reconnect                                    | The per-broker hostnames are missing from the SAN of the Gateway certificate. See [Configure the Kafka Client & Gateway](configure-the-kafka-client-and-gateway.md).                |
