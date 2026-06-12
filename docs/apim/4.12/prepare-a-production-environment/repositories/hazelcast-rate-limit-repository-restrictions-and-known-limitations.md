---
hidden: true
noIndex: true
---

# Hazelcast Rate-Limit Repository Restrictions and Known Limitations

## Restrictions

- **Configuration file formats:** Only XML (`.xml`) and YAML (`.yaml`, `.yml`) Hazelcast configuration file formats are supported. Other formats throw an error.
- **Scope restriction:** The repository supports only `Scope.RATE_LIMIT`. Attempting to use it for other scopes (e.g., `Scope.MANAGEMENT`) throws an error.
- **RBAC requirement in Kubernetes:** If `apim.managedServiceAccount: false` in Helm and RBAC permissions are not granted manually, each gateway pod forms a single-member Hazelcast cluster. Rate-limit budgets are multiplied by the replica count (each pod enforces the limit independently).
- **Port collision avoidance:** When running multiple Hazelcast subsystems (cluster, cache, rate-limit) in the same JVM, each must use a distinct `<port>` range and `<cluster-name>` in its XML configuration to avoid collisions. The default configurations use port 5701 (cluster), 5801 (cache), 5901 (rate-limit) with `auto-increment="true"`.
- **Failure propagation:** The repository propagates Hazelcast failures to the calling rate-limit policy. The policy's own configuration determines whether to allow (fail-open) or reject (fail-closed) requests on error.
- **TTL edge case:** Entries with `resetTime <= 0` are assigned a TTL of 1ms (immediate eviction) instead of infinite retention.
- **AP-mode split-brain limitation:** During a network partition, both sides count independently, resulting in up to 2× over-quota until the partition heals. This behavior is inherent to AP mode.
- **Embedded JVM footprint:** The rate-limit Hazelcast instance runs embedded in each gateway JVM, consuming approximately 16MB (`hazelcast-5.5.0.jar`) plus threads, direct memory, and a port (5901 by default).

## Related Changes

The Helm chart now creates a ClusterIP service (`{{ .Release.Name }}-gateway-hz`) exposing port 5901 (or the configured `gateway.ratelimit.hazelcast.port`) when `ratelimit.type=hazelcast`, and adds a Role and RoleBinding to grant the gateway ServiceAccount permissions for Hazelcast Kubernetes discovery. The chart renders a `hazelcast-ratelimit.xml` ConfigMap with auto-configured Kubernetes join settings and mounts it in gateway pods (skipped if `gateway.extraVolumes` defines an external configuration). A warning appears in `NOTES.txt` if Hazelcast is enabled but `apim.managedServiceAccount=false`, instructing administrators to grant RBAC permissions manually. The `gravitee-apim-repository-hazelcast` plugin is now bundled in the gateway distribution as a runtime dependency (type: zip) with all transitive dependencies packaged in the `lib/` directory.
