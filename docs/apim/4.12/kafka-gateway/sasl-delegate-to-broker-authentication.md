# SASL Delegate-to-Broker Authentication

### Standard Flow (Non-Delegate)

In the standard flow, the gateway authenticates to backend clusters using its own credentials configured in the Cluster entity's connection settings:

1. Client connects to gateway bootstrap SNI.
2. Gateway resolves virtual cluster endpoint from `virtualClusterCrossId`.
3. Gateway fetches metadata from all backend clusters in parallel.
4. Gateway merges metadata and caches result.
5. Gateway serves cached metadata to client (no backend connection).
6. Client reconnects to specific virtual broker SNI.
7. Gateway extracts cluster index from virtual broker ID.
8. Gateway connects to real broker in target cluster.
9. Gateway rewrites broker IDs in responses to virtual IDs.

### Delegate-to-Broker SASL Flow

In delegate mode, the gateway forwards the client's SASL credentials to backend clusters instead of using its own:

1. Client connects to gateway bootstrap SNI with SASL credentials.
2. Gateway fans out SASL to all backend clusters (every time).
3. Gateway fetches metadata only if cache is cold.
4. Gateway serves metadata from cache when warm.
5. Subsequent client requests (Metadata, ApiVersions) served from cache.
6. Client reconnects to specific virtual broker SNI.
7. Gateway validates credentials against one backend cluster.
8. Gateway serves cached responses for Metadata/ApiVersions.
9. Other requests forwarded to target cluster.

**Rationale**: SASL is fanned out to every backend so the gateway holds an authenticated connection to each cluster. This is required for post-bootstrap RPCs that route per-cluster (FIND_COORDINATOR, DESCRIBE_GROUPS probe).

### SASL Credential Capture

When the gateway operates in delegate mode, it introspects the client's SASL credentials during the initial handshake. For replay-safe mechanisms (currently PLAIN only), the gateway stores the credentials on the connection context. For non-replay-safe mechanisms (AWS_MSK_IAM, SCRAM, GSSAPI), the gateway does not capture credentials.

| Mechanism | Captured | Reason |
|:----------|:---------|:-------|
| `PLAIN` | Yes | Authentication payload is replay-safe (static username/password). |
| `AWS_MSK_IAM` | No | Signature is time-bound and broker-specific; cannot be reused. |
| `SCRAM` | No | Challenge-response; cannot be replayed. |
| `GSSAPI` | No | Kerberos tickets; cannot be replayed. |

### SASL Credential Replay on Cross-Cluster Sub-Connection

When the gateway needs to forward a request (e.g., FIND_COORDINATOR fan-out) to a backend the client never directly connected to, it retrieves the captured credentials from the connection context and replays them:

1. Gateway opens a fresh TCP connection to the target backend.
2. Gateway sends `SASL_HANDSHAKE` with the captured mechanism.
3. Gateway sends `SASL_AUTHENTICATE` with the captured `authBytes`.
4. Backend validates; if successful, gateway sends the actual request.
5. Gateway reads response, closes sub-connection, returns response to caller.

**Error Handling**:

* If backend rejects handshake: gateway returns `IllegalStateException("SASL handshake replay rejected by backend: <error>")`.
* If backend rejects authenticate: gateway returns `IllegalStateException("SASL authenticate replay rejected by backend: <error> (<message>)")`.

## Response Frame Rewrite Optimization

The gateway optimizes response frame rewriting for large payloads by checking whether rewrite is necessary before allocating buffers. For `FETCH` (v16+), `PRODUCE` (v10+), `SHARE_ACKNOWLEDGE`, and `SHARE_FETCH` responses, the gateway skips rewrite and re-serialization when the `nodeEndpoints` collection is empty (happy path). KIP-951 `nodeEndpoints` are only populated when the broker steers the client to a different node (e.g., `NotLeaderOrFollower`). This optimization avoids the multi-MB `ByteBuffer.allocate()` cost of re-serializing the records payload in the common case.
