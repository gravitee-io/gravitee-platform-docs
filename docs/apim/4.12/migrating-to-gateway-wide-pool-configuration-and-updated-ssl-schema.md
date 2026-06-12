# Migrating to Gateway-Wide Pool Configuration and Updated SSL Schema

## Migrating to Gateway-Wide Pool Configuration

### AI Vector Store Redis Migration

Move pool and timeout configuration from per-API resource definitions to `gravitee.yml`. Old 4.x API definitions that still carry pool sizing parameters in the resource configuration are silently ignored (the field is marked with `@JsonIgnoreProperties(ignoreUnknown = true)`). No deployment failure occurs, but the field has no effect. Operators must configure pool sizing in `gravitee.yml` under `resources.aiVectorStoreRedis.*` instead.

**Before (per-API configuration, deprecated)**:

```json
{
  "type": "ai-vector-store-redis",
  "configuration": {
    "host": "redis.example.com",
    "port": 6379,
    "maxPoolSize": 10
  }
}
```

**After (gateway-wide configuration)**:

```yaml
# gravitee.yml
resources:
  aiVectorStoreRedis:
    maxPoolSize: 10
    maxPoolWaiting: 1024
    poolCleanerInterval: 30000
    poolRecycleTimeout: 180000
    maxWaitingHandlers: 1024
    connectTimeout: 2000
```

### Cache Redis Migration

Configure gateway-wide pool settings in `gravitee.yml` under `resources.cacheRedis.*`. Remove pool sizing parameters from per-API cache-redis resource configurations; they are ignored if present.

**gravitee.yml example**:

```yaml
resources:
  cacheRedis:
    maxPoolSize: 6
    maxPoolWaiting: 1024
    poolCleanerInterval: 30000
    poolRecycleTimeout: 180000
    maxWaitingHandlers: 1024
    connectTimeout: 2000
```

### Multi-Certificate PEM Keystore Migration

Replace singular **Key Path**/**Cert Path** fields with **Key Paths**/**Cert Paths** lists when presenting more than one keypair (e.g., RSA + ECDSA) for TLS negotiation.

**Before (single certificate)**:

```json
{
  "ssl": {
    "keyStore": {
      "type": "pem",
      "certPath": "/etc/gravitee/cert.pem",
      "keyPath": "/etc/gravitee/key.pem"
    }
  }
}
```

**After (multiple certificates)**:

```json
{
  "ssl": {
    "keyStore": {
      "type": "pem",
      "certPaths": [
        "/etc/gravitee/rsa-cert.pem",
        "/etc/gravitee/ecdsa-cert.pem"
      ],
      "keyPaths": [
        "/etc/gravitee/rsa-key.pem",
        "/etc/gravitee/ecdsa-key.pem"
      ]
    }
  }
}
```

### SSL Keystore/Truststore Type Migration

Update JSON schema references from empty string `""` to `"NONE"` for the "None" option in keystore/truststore type selection.

**Before**:

```json
{
  "trustStore": {
    "type": ""
  }
}
```

**After**:

```json
{
  "trustStore": {
    "type": "NONE"
  }
}
```

### Sentinel Enabled Default Change

The `sentinel.enabled` field now defaults to `true` (changed from `false`). Existing configurations that activated sentinel mode by providing `nodes` and **Master Id** without explicitly setting `enabled=true` continue to work. The mapper only switches to SENTINEL mode when `enabled` is true **and** `nodes` is non-empty.
