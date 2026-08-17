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

## Keeping your own broker numbering

If the rewritten IDs do not fit a DNS convention you already run, you can give Virtual Clusters their own broker hostname scheme with `virtualClusterBrokerDomainPattern`. It applies **only** to APIs backed by a Virtual Cluster, so the Kafka APIs already running on that Gateway keep their hostnames — and their DNS entries and certificate SANs — untouched.

Three placeholders are available, in either pattern:

| Placeholder      | Value                                                            |
| ---------------- | ---------------------------------------------------------------- |
| `{brokerId}`     | the advertised ID — rewritten on a Virtual Cluster (the default) |
| `{realBrokerId}` | the ID as configured on the backend broker                       |
| `{clusterIndex}` | the backend's zero-based position in the Virtual Cluster         |

```yaml
kafka:
  enabled: true

  routingMode: host
  routingHostMode:
    defaultDomain: "mycompany.org"

    # Plain Kafka APIs: unchanged. broker 3 stays broker3-myapi.mycompany.org
    brokerDomainPattern: "broker{brokerId}-{apiHost}.{defaultDomain}"

    # Virtual Cluster APIs only: broker 3 of the second backend becomes
    # broker3-c1-mymesh.mycompany.org
    virtualClusterBrokerDomainPattern: "broker{realBrokerId}-c{clusterIndex}-{apiHost}.{defaultDomain}"
```

Brokers then keep the numbers your operators know, and the backend gets its own label. The placeholders can appear in any order in the pattern.

`virtualClusterBrokerDomainPattern` is optional. Left unset, Virtual Clusters follow `brokerDomainPattern` like every other API, and their hostnames carry the rewritten IDs described above.

{% hint style="info" %}
A Virtual Cluster hostname **must** distinguish the backends, either through `{brokerId}` (which encodes the backend) or through `{clusterIndex}`. A pattern built only from `{realBrokerId}` would send broker 3 of the first backend and broker 3 of the second to the same hostname, and the Gateway could no longer tell them apart.
{% endhint %}

{% hint style="warning" %}
Both settings are Gateway-wide, so `virtualClusterBrokerDomainPattern` applies to **every** Virtual Cluster API on that Gateway. Changing it after Virtual Clusters are in production moves their DNS entries and certificate SANs.
{% endhint %}

This override does not apply to Gateways using access points, where the broker domain comes from the access point rather than from configuration.

## Clients reaching an unadvertised broker hostname

A client connecting on a broker hostname whose ID falls outside every advertised block — an entry left over from a single-backend deployment, most often — is served as a bootstrap connection: it receives the merged metadata and re-targets itself at the correct broker. The Gateway logs a warning naming the ID it received and the range it advertises:

```
Client connected on a broker host carrying id 0, which this virtual cluster never advertised
(it advertises 10000..29999 across 2 backends). Serving the connection as bootstrap so the client
can re-target itself; check the broker DNS records point at the ids the mesh advertises.
```

Treat that warning as a DNS mismatch to fix rather than a supported mode: the extra round trip is paid on every connection.

## Backend broker ID limit

Every backend broker ID must be **below 10000**, otherwise it collides with the next backend's block. Higher IDs are rejected at runtime. Single- and double-digit broker IDs are the convention in most deployments, and Kafka's own generated IDs start at 1001, so this rarely applies — but check it if you are onboarding a cluster with hand-assigned high IDs.

## Troubleshooting

| Symptom                                                                | Likely cause                                                                                                                                                                       |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bootstrap and topic listing work, but producing and consuming time out | The DNS entries for the advertised IDs do not exist. Clients resolve the bootstrap fine, then fail on the per-broker hostnames returned in metadata.                                |
| `Client connected on a broker host carrying id N` warnings in the logs | Clients are still using the broker DNS entries of a single-backend deployment.                                                                                                     |
| Connections fail only for one backend's brokers                        | That backend's block of entries is missing. Check the position of the backend in the Virtual Cluster configuration, since the block follows the listed order.                       |
| TLS handshake failures on reconnect                                    | The per-broker hostnames are missing from the SAN of the Gateway certificate. See [Configure the Kafka Client & Gateway](configure-the-kafka-client-and-gateway.md).                |
