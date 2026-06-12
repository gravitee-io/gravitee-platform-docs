# Migrate from Redis Cache Resource 4.x to 5.x

## Migrating from Redis Cache Resource 4.x

### Update Gateway Configuration

Move pool and timeout settings from per-resource configuration to `gravitee.yml`:

1. Open `gravitee.yml` on each gateway node.
2. Add the `resources.cacheRedis` section with pool and timeout properties:

   ```yaml
   resources:
     cacheRedis:
       maxPoolSize: 60
       maxPoolWaiting: 1024
       poolCleanerInterval: 30000
       poolRecycleTimeout: 180000
       maxWaitingHandlers: 1024
       connectTimeout: 2000
   ```

3. Restart the gateway to apply the new settings.

Per-resource pool settings are ignored in resource definitions. The following form fields have been removed from the resource configuration UI:

* Max total
* Max pool size
* Max pool waiting
* Pool cleaner interval (ms)
* Pool recycle timeout (ms)
* Max waiting handlers
* Connect timeout (ms)

Retained form fields include:

* Host
* Port
* Password
* Use SSL
* SSL options
* Sentinel options
* Release the cache when API is stopped
* Time to live (in seconds)
* Timeout (in milliseconds)

### Harden SSL Configuration

If `useSsl=true` but no `ssl` options are configured, the resource falls back to `trustAll=true` and `hostnameVerificationAlgorithm=NONE`. To harden production deployments:

1. Navigate to **APIs > [Your API] > Configuration > Resources > [Redis Cache Resource]**.
2. Expand the **SSL** section.
3. Select a **Trust Store Type** (PEM recommended for certificate files).
4. Enter the **Trust Store Path** to your CA certificate file.
5. Toggle **Verify Host** to enable hostname verification.
6. (Optional) Restrict **TLS Protocols** to TLSv1.3 and specify allowed **TLS Ciphers**.
7. Click **Save** and redeploy the API.

### Verify Cache Entry Migration

Legacy cache entries are served read-only during rolling upgrades. Entries migrate to the binary frame format on TTL expiry. To verify migration:

1. Monitor cache hit rates in gateway logs or metrics.
2. After the TTL period has elapsed, all entries should be in binary format.
3. If tooling parses cached values directly (e.g., via `redis-cli`), update it to decode the binary frame format. Cache keys are unchanged; cache values are no longer human-readable in `redis-cli`.

The `policy.cache.serialization` property in `gravitee.yml` has no effect in Cache policy 4.x and should be removed.

### Data Cache Policy Upgrade

The Data Cache policy 2.x requires APIM 4.12 or later. Version 1.x supports APIM 4.5 to 4.11. All cache operations are now asynchronous and non-blocking. No configuration changes are required, but custom integrations that invoke the cache API directly must migrate from synchronous methods (`get`, `put`, `evict`) to asynchronous methods (`getAsync`, `putAsync`, `evictAsync`) that return `Future` objects.

### OAuth2 Policy Cache Behavior

The OAuth2 policy now uses asynchronous cache operations for token introspection results. Cache read failures are logged and fall back to OAuth2 resource introspection without interrupting the request. Cache write operations are fire-and-forget with `onFailure` logging. Cache write failures are logged but do not affect the request flow.

### Synchronous API Deadlock Prevention

Synchronous cache methods (`get`, `put`, `evict`) invoked from a Vert.x event-loop thread return `null` and log a warning to avoid deadlock. Use asynchronous methods (`getAsync`, `putAsync`, `evictAsync`) in reactive contexts.

### Cache Clear Behavior

When `releaseCache=false`, the `clear()` operation is a no-op to avoid wiping the full `"gravitee:*"` namespace (which would delete other APIs' entries). When `releaseCache=true` AND the `ATTR_API_DEPLOYED_AT` attribute is present, the clear operation deletes only keys matching the pattern `"gravitee:*:<deployAt>"`. When `releaseCache=true` AND the `ATTR_API_DEPLOYED_AT` attribute is missing, the clear operation skips the clear and logs a warning.
