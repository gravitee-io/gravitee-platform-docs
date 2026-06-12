---
hidden: true
noIndex: true
---

# API Model Object Reference for Portal Templates

## API model object

The `api` variable is an instance of one of three concrete model classes, selected based on the API's definition version:

| API Type | Definition Version | Model Class |
|:---------|:-------------------|:------------|
| V2 (proxy-based) | `V1`, `V2` | `io.gravitee.rest.api.model.ApiModel` |
| V4 HTTP / Async | `V4` | `io.gravitee.rest.api.model.v4.api.ApiModel` |
| V4 Native (Kafka) | `V4` | `io.gravitee.rest.api.model.v4.nativeapi.NativeApiModel` |
| Federated / Federated-Agent | `FEDERATED`, `FEDERATED_AGENT` | `io.gravitee.rest.api.model.v4.api.ApiModel` (subset of fields populated) |

All classes implement the `GenericApiModel` interface, which guarantees the common fields listed below.

### Common API Fields

The following fields are available on all API types:

| FreeMarker Expression | Type | Description |
|:----------------------|:-----|:------------|
| `${api.id}` | String | Technical UUID of the API |
| `${api.name}` | String | Display name |
| `${api.description}` | String | Short description; may be empty |
| `${api.version}` | String | API version string (e.g., `v1.0`). Alias for `apiVersion` on V4; on V2 this is the native field name |
| `${api.apiVersion}` | String | V4 / Federated preferred accessor for the version string |
| `${api.definitionVersion}` | Enum | `V1`, `V2`, `V4`, `FEDERATED`, `FEDERATED_AGENT` |
| `${api.createdAt}` | Date | Creation timestamp |
| `${api.updatedAt}` | Date | Last modification timestamp |
| `${api.deployedAt}` | Date | Last deployment timestamp; may be `null` if never deployed |
| `${api.state}` | Enum | `STARTED` or `STOPPED` |
| `${api.lifecycleState}` | Enum | `CREATED`, `PUBLISHED`, `UNPUBLISHED`, `DEPRECATED`, `ARCHIVED` |
| `${api.visibility}` | Enum | `PUBLIC` or `PRIVATE` |
| `${api.tags}` | Set\<String\> | Deployment tag names; iterable |
| `${api.groups}` | Set\<String\> | Group IDs the API belongs to |
| `${api.categories}` | Set\<String\> | Category slugs; iterable |
| `${api.picture}` | String | Base64-encoded picture data URI; may be `null` |
| `${api.primaryOwner}` | Object | See Primary Owner sub-object below |
| `${api.disableMembershipNotifications}` | boolean | `true` if membership notifications are suppressed |
| `${api.metadata}` | Map\<String, String\> | Key/value API metadata; see API Metadata section below |

### Primary Owner Sub-Object

Accessible on all API types as `${api.primaryOwner.<field>}`:

| Expression | Type | Description |
|:-----------|:-----|:------------|
| `${api.primaryOwner.id}` | String | UUID of the owning user or group |
| `${api.primaryOwner.email}` | String | Email address |
| `${api.primaryOwner.displayName}` | String | Human-readable name (e.g., "John Doe") |
| `${api.primaryOwner.type}` | String | `"USER"` or `"GROUP"` |

### Version-Specific Fields

The following fields are available only on specific API definition versions:

| FreeMarker Expression | Type | V2 | V4 HTTP | V4 Native | Federated | Description |
|:----------------------|:-----|:--:|:-------:|:---------:|:---------:|:------------|
| `${api.proxy}` | Proxy | ✅ | — | — | — | HTTP proxy config (virtual hosts, load-balancer, endpoints) — V2 only |
| `${api.executionMode}` | Enum | ✅ | — | — | — | `V3` or `V4_EMULATION_ENGINE` — V2 only |
| `${api.properties}` | Properties (V2) / List\<Property\> (V4) | ✅ | ✅ | ✅ | — | API-level properties; structure differs between V2 and V4 |
| `${api.services}` | Services (V2) / ApiServices (V4) / NativeApiServices (V4 Native) | ✅ | ✅ | ✅ | — | Health-check, discovery, and other service configs |
| `${api.type}` | Enum | — | ✅ | ✅ | — | `SYNC`, `ASYNC`, or `NATIVE` |
| `${api.listeners}` | List\<Listener\> / List\<NativeListener\> | — | ✅ | ✅ | — | Configured listeners (HTTP, TCP, Kafka, etc.); iterable |
| `${api.endpointGroups}` | List\<EndpointGroup\> / List\<NativeEndpointGroup\> | — | ✅ | ✅ | — | Endpoint groups; iterable |
| `${api.failover}` | Failover | — | ✅ | — | — | Failover configuration; present only on V4 HTTP APIs |

## API Metadata

`${api.metadata}` is a map populated from the API's configured metadata entries. The values are pre-resolved through the template engine before being exposed, so metadata values may themselves contain FreeMarker expressions referencing `${api.*}`.

Access individual entries with bracket notation:

```
${api.metadata['email-support']}
${api.metadata['custom-key']}
```

**Special key — `email-support`:** If `api.metadata['email-support']` is blank after resolution, it is automatically replaced with the primary owner's email address.
