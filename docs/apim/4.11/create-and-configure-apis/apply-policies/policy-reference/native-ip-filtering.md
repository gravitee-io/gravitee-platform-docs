# Native IP Filtering Policy Reference

## Overview

The Native IP Filtering policy controls client access to Native Kafka APIs by matching client IP addresses against whitelist and blacklist rules. The policy supports IPv4, IPv6, CIDR notation, IP ranges, and Expression Language for dynamic filtering. It executes during the entrypoint connection phase.

## Key Concepts

### Whitelist and Blacklist Logic

A client is allowed to connect only if both conditions are satisfied:

1. At least one whitelist rule matches the client IP **or** the whitelist is empty
2. No blacklist rule matches the client IP

If either condition fails, the connection is rejected with `CLUSTER_AUTHORIZATION_FAILED`.

### IP Address Formats

The policy accepts multiple formats in a single `clientAddress` field. Comma-separated values are evaluated individually; any match succeeds. Whitespace is automatically removed.

| Format | Example | Description |
|:-------|:--------|:------------|
| Single IP (IPv4) | `192.168.1.1` | Exact match |
| Single IP (IPv6) | `fd12:3456:789a::1` | Exact match |
| CIDR (IPv4) | `192.168.1.0/24` | Network range |
| CIDR (IPv6) | `fd12:3456:789a::/64` | Network range |
| IP Range (IPv4) | `192.168.1.1 - 192.168.1.10` | Inclusive range |
| IP Range (IPv6) | `fd12:3456:789a::1 - fd12:3456:789a::a` | Inclusive range |
| Comma-separated | `192.168.1.1, 192.168.2.0/24` | Multiple values |
| Expression Language | `{#api.properties['list_of_allowed_ips']}` | Evaluated at runtime |

### IPv4-Mapped IPv6 Normalization

IPv4-mapped IPv6 addresses (e.g., `::ffff:192.168.1.1`) are automatically normalized to their IPv4 equivalents (`192.168.1.1`) and will match against regular IPv4 rules.

## Prerequisites

* Gravitee APIM 4.11.x or above
* Native Kafka API configured in the gateway
* Client IP addresses must be resolvable by the gateway

## Gateway Configuration

### Policy Configuration

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `whitelist` | array of `Client` | List of clients allowed to connect. Empty array permits all IPs (unless blacklisted). | See examples below |
| `blacklist` | array of `Client` | List of clients disallowed to connect. | See examples below |

### Client Object

| Property | Type | Description | Example |
|:---------|:-----|:------------|:--------|
| `label` | string (required, minLength: 1) | Human-readable label for the rule | `"clients from network A"` |
| `clientAddress` | string (required, minLength: 1) | IP address, CIDR, or IP range. Supports IPv4 and IPv6. Whitespaces are removed. | `"192.168.1.0/24"` |

## Creating a Whitelist Rule

To allow specific clients, add entries to the `whitelist` array in the policy configuration:

1. Set a descriptive `label` for the rule.
2. Specify the `clientAddress` using any supported format (single IP, CIDR, range, or comma-separated list).
3. If the whitelist is non-empty, only clients matching at least one rule will be permitted.
4. Combine with blacklist rules to exclude specific IPs from an allowed range.

**Example: Single IP Whitelist (IPv4)**

```json
{
    "whitelist": [
        {
            "label": "clients from networks A",
            "clientAddress": "192.168.1.1, 192.168.2.0/24, 192.168.3.1-192.168.3.10"
        }
    ],
    "blacklist": []
}
```

## Creating a Blacklist Rule

To block specific clients, add entries to the `blacklist` array:

1. Set a descriptive `label` for the rule.
2. Specify the `clientAddress` using any supported format.
3. Blacklist rules are evaluated after whitelist rules; if a client matches any blacklist entry, the connection is rejected regardless of whitelist status.

**Example: CIDR-Based Whitelist with Blacklisted IPs**

```json
{
    "whitelist": [
        {
            "label": "clients from network A",
            "clientAddress": "192.168.1.0/24"
        },
        {
            "label": "clients from network B",
            "clientAddress": "192.168.2.0/24"
        }
    ],
    "blacklist": [
        {
            "label": "blocked host from network A",
            "clientAddress": "192.168.1.10"
        }
    ]
}
```

## Using Expression Language for Dynamic Filtering

To reference API properties or context variables, use Expression Language in the `clientAddress` field:

1. Define the property in the API configuration (e.g., `list_of_allowed_ips`).
2. Reference it using `{#api.properties['list_of_allowed_ips']}`.
3. The expression is evaluated at runtime; the result is treated as a comma-separated list of IPs, CIDRs, or ranges.
4. If the expression resolves to an empty string, the entry is ignored.

**Example: Expression Language-Based Filtering**

```json
{
    "whitelist": [
        {
            "label": "clients from network A",
            "clientAddress": "{#api.properties['list_of_allowed_ips']}"
        }
    ],
    "blacklist": [
        {
            "label": "clients from network B",
            "clientAddress": "{#api.properties['list_of_forbidden_ips']}"
        }
    ]
}
```

## Restrictions

* Policy applies only to Native Kafka APIs (`NATIVE_KAFKA` type)
* Executes during the `ENTRYPOINT_CONNECT` phase only
* Invalid IP formats (e.g., malformed CIDR, invalid range syntax) cause policy instantiation to fail with `ClientAddressFilterInstantiationException`
* Rejected connections return error key `CLUSTER_AUTHORIZATION_FAILED` with message `"IP not allowed"`
* Expression Language values that resolve to empty strings are silently ignored
* Requires Gravitee APIM 4.11.x or above

## Related Changes

The policy includes a JSON schema (`schema-form.json`) for UI-based configuration in the Gravitee Console. The schema provides inline help text explaining supported IP formats (IPv4, IPv6, CIDR, IP-Range) and automatic whitespace removal. The policy is categorized under "others" in the policy catalog and uses the `ip-filtering.svg` icon. The feature flag `apim-native-policy-ip-filtering` controls availability.
