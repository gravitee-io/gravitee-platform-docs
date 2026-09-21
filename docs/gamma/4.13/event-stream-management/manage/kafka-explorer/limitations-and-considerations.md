---
hidden: false
noIndex: false
description: What Kafka Explorer connections store, which node reaches your brokers, how a security overlay combines with the target's own security, and what the explorer can't read. Read this before you connect to a production cluster.
---

# Limitations and considerations

Kafka Explorer reads a live Kafka cluster from the Management API, through a connection that stores its own credentials. This page covers what that implies for your network and your secrets, and what the explorer can't do.

## Which node connects to your brokers

The **Management API** opens every explorer connection. Not the Kafka gateway, and not the browser.

* Your brokers must be reachable from the Management API nodes. A cluster that only the gateway can reach isn't explorable.
* A **Kafka Service** target still goes through the gateway addresses the service exposes, so the Management API reaches the gateway, and the gateway reaches the brokers.
* A `…with path` truststore or key store is read from the Management API's own filesystem. See [Where credentials are stored](#where-credentials-are-stored).

A **Direct Broker** target takes the bootstrap addresses you type, with no registered cluster or Kafka Service in between. Anyone who can create a connection can therefore make the Management API open a TCP connection to any `host:port` it can reach on your network, and learn whether it answers. That's the point of the target type, and it's the reason to grant the `EXPLORER` **Create** permission narrowly. See [Who can do what](manage-kafka-explorer-connections.md#who-can-do-what).

## Where credentials are stored

A connection's security overlay is stored in the APIM management database, alongside the rest of the connection. It isn't encrypted at rest.

That covers every secret you enter in the **Security** step: SASL passwords, OAuth client secrets, bearer tokens, truststore and key store passwords, and the contents of a store you paste in.

The Management API never returns a secret once it's saved. A password, client secret, or token comes back blank on the **Configuration** page, and leaving it blank keeps the stored value. The protection is on the API, not on the database, so:

* Treat the management database, and its backups, as holding Kafka credentials. Restrict access to it accordingly.
* Prefer a dedicated, least-privileged Kafka principal for an explorer connection over an existing application credential.
* For a truststore or key store, prefer a `…with path` option over a `…with content` one.

### Stores by path and stores by content

Each of **Truststore** and **Key store** offers both forms:

| Form | Where the store lives |
| --- | --- |
| `JKS with path`, `PKCS#12 / PFX with path`, `PEM with path` | A file on the Management API's filesystem. Only the path is stored in the database. The file must exist at the same path on **every** Management API node. |
| `JKS with content`, `PKCS#12 / PFX with content`, `PEM with content` | The store itself, stored in the database. It's written to a temporary file each time the connection is used, and deleted afterwards. |

A path-based store keeps the key material out of the database and its backups, where file permissions protect it instead. Its **password** is still part of the overlay, so it's still stored in the database either way.

## TLS verification

**Verify Host** and **Trust all** both relax the same check: the verification that the broker's certificate matches the host you connected to. Neither one skips validation of the certificate chain.

A broker presenting a self-signed certificate, or one issued by a private CA, therefore needs a **Truststore** holding that certificate or its CA. Turning **Trust all** on instead leaves the connection failing on the certificate chain, and the error points at the TLS handshake rather than at the missing truststore.

Relax either switch only against a cluster you control, such as a local or test broker.

## How an overlay combines with the target's security

The overlay means two different things depending on the target, and this is the most common source of surprise:

| Target | What the overlay does |
| --- | --- |
| **Cluster**, **Direct Broker** | **Replaces** the target's security entirely. It's never merged field by field. |
| **Kafka Service** | **Adds to** the plan's security. The plan imposes the authentication, and the overlay supplies only what the plan leaves open, such as the protocol variant or a truststore. |

The replacement case is the one to watch. When you turn **Override the cluster security** on for a Cluster target, the named connection's own protocol, SASL mechanism, credentials, and stores all stop applying — the overlay is the whole security. If the cluster used SASL with a truststore, you must restate both in the overlay, not just the part you wanted to change.

Turning the override back off, with **Remove security overlay** on the **Configuration** page, restores the target's own security.

## What the explorer can't read

* **Binary and schema-encoded payloads.** Message keys, values, and headers are read as text. An Avro, Protobuf, or otherwise binary payload is shown as the text its bytes decode to, which is unreadable. There's no schema registry integration and no way to choose a deserializer.
* **A cluster using a SASL mechanism the explorer doesn't model.** A registered cluster's named connection resolves for `PLAIN`, `SCRAM-SHA-256`, `SCRAM-SHA-512`, and no authentication. A connection to a cluster configured with anything else fails to resolve unless you override its security with an overlay the explorer supports.
* **A Virtual Cluster.** Virtual Clusters aren't explorable.

## What the explorer never writes

Every page reads. The explorer creates no topic, writes no message, commits no consumer offset, and changes no broker or topic configuration. Browsing and tailing a topic doesn't join a consumer group, so it doesn't appear in the group list and doesn't move anyone's offsets.

## Accuracy of the counters

* A topic's **Messages** count adds up the end offset of each partition. It counts everything ever written to the topic, so on a topic with retention or log compaction it's higher than the number of messages actually retained.
* The **Consumer Groups** page paginates by group ID, so clicking a column header reorders the rows on the current page only, not the whole result set.

## Volume and timing

* A browse reads at most the limit from each selected partition in a single read, then applies the filters and keeps at most the limit. The read waits at most five seconds by default, raised by the Management API's `kafka.timeout.seconds` setting. A slow or large topic can return fewer messages than the limit.
* A live tail runs for at most 300 seconds and delivers at most 5000 messages, and its table keeps the newest 500 on screen.
* Each Management API instance serves at most 256 live tails at a time. Past that, starting one fails with **Too many active tail streams**.

See [Browse and tail topic messages](browse-and-tail-topic-messages.md).
