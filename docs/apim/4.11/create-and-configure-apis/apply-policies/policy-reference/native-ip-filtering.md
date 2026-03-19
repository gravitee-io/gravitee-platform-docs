# Native IP filtering

## Overview

The Native IP Filtering policy controls client access to Native Kafka APIs by matching client IP addresses against whitelist and blacklist rules. It supports IPv4, IPv6, CIDR notation, IP ranges, and Expression Language for dynamic filtering. The policy executes during the entrypoint connection phase (`ENTRYPOINT_CONNECT`).

{% hint style="warning" %}
This policy requires an Enterprise Edition license with the `apim-native-policy-ip-filtering` feature. It applies to Native Kafka APIs only.
{% endhint %}

For HTTP proxy and v4 message APIs, use the [IP Filtering](ip-filtering.md) policy instead.

## Whitelist and blacklist logic

A client connects only when both conditions are met:

1. At least one whitelist rule matches the client IP, **or** the whitelist is empty
2. No blacklist rule matches the client IP

If either condition fails, the gateway calls `ctx.interrupt("IP not allowed")`, which returns the Kafka protocol error `CLUSTER_AUTHORIZATION_FAILED` to the client.

## IP address formats

The `clientAddress` field accepts multiple formats. Comma-separated values are evaluated individually — any match succeeds. Whitespace is automatically removed.

<table>
    <thead>
        <tr>
            <th width="200">Format</th>
            <th width="300">Example</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Single IP (IPv4)</td>
            <td><code>192.168.1.1</code></td>
            <td>Exact match</td>
        </tr>
        <tr>
            <td>Single IP (IPv6)</td>
            <td><code>fd12:3456:789a::1</code></td>
            <td>Exact match</td>
        </tr>
        <tr>
            <td>CIDR (IPv4)</td>
            <td><code>192.168.1.0/24</code></td>
            <td>Network range</td>
        </tr>
        <tr>
            <td>CIDR (IPv6)</td>
            <td><code>fd12:3456:789a::/64</code></td>
            <td>Network range</td>
        </tr>
        <tr>
            <td>IP range (IPv4)</td>
            <td><code>192.168.1.1-192.168.1.10</code></td>
            <td>Inclusive range</td>
        </tr>
        <tr>
            <td>IP range (IPv6)</td>
            <td><code>fd12:3456:789a::1-fd12:3456:789a::a</code></td>
            <td>Inclusive range</td>
        </tr>
        <tr>
            <td>Comma-separated</td>
            <td><code>192.168.1.1,192.168.2.0/24</code></td>
            <td>Multiple values evaluated individually</td>
        </tr>
        <tr>
            <td>Expression Language</td>
            <td><code>{#api.properties['allowed_ips']}</code></td>
            <td>Evaluated at runtime</td>
        </tr>
    </tbody>
</table>

### IPv4-mapped IPv6 normalization

IPv4-mapped IPv6 addresses (for example, `::ffff:192.168.1.1`) are automatically resolved to their IPv4 equivalents (`192.168.1.1`) through Java's built-in IP address parsing and match against regular IPv4 rules.

## Configuration

### Policy configuration

<table>
    <thead>
        <tr>
            <th width="150">Property</th>
            <th width="150">Type</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>whitelist</code></td>
            <td>array of <code>Client</code></td>
            <td>List of clients allowed to connect. An empty array permits all IPs (unless blacklisted).</td>
        </tr>
        <tr>
            <td><code>blacklist</code></td>
            <td>array of <code>Client</code></td>
            <td>List of clients blocked from connecting.</td>
        </tr>
    </tbody>
</table>

### Client object

<table>
    <thead>
        <tr>
            <th width="180">Property</th>
            <th width="180">Type</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>label</code></td>
            <td>string (required, minLength: 1)</td>
            <td>Human-readable label for the rule</td>
        </tr>
        <tr>
            <td><code>clientAddress</code></td>
            <td>string (required, minLength: 1)</td>
            <td>IP address, CIDR, or IP range. Supports IPv4 and IPv6. Whitespace is removed.</td>
        </tr>
    </tbody>
</table>

## Create a whitelist rule

To allow specific clients, add entries to the `whitelist` array:

1. Set a descriptive `label` for the rule.
2. Specify the `clientAddress` using any supported format (single IP, CIDR, range, or comma-separated list).
3. If the whitelist is non-empty, only clients matching at least one rule are permitted.
4. Combine with blacklist rules to exclude specific IPs from an allowed range.

**Example: whitelist with multiple formats**

```json
{
    "whitelist": [
        {
            "label": "clients from networks A",
            "clientAddress": "192.168.1.1,192.168.2.0/24,192.168.3.1-192.168.3.10"
        }
    ],
    "blacklist": []
}
```

## Create a blacklist rule

To block specific clients, add entries to the `blacklist` array:

1. Set a descriptive `label` for the rule.
2. Specify the `clientAddress` using any supported format.
3. Blacklist rules are evaluated alongside whitelist rules. If a client matches any blacklist entry, the connection is rejected regardless of whitelist status.

**Example: CIDR-based whitelist with blacklisted IPs**

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

## Use Expression Language for dynamic filtering

To reference API properties or context variables, use Expression Language in the `clientAddress` field:

1. Define the property in the API configuration (for example, `list_of_allowed_ips`).
2. Reference it using `{#api.properties['list_of_allowed_ips']}`.
3. The expression is evaluated at runtime. The result is treated as a comma-separated list of IPs, CIDRs, or ranges.
4. If the expression resolves to an empty string, the entry is ignored.

**Example: Expression Language-based filtering**

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

## Errors

<table>
    <thead>
        <tr>
            <th width="300">Kafka error code</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>CLUSTER_AUTHORIZATION_FAILED</code></td>
            <td>The client IP doesn't match any whitelist rule, or it matches a blacklist rule. The gateway interrupts the connection with the message <code>"IP not allowed"</code>.</td>
        </tr>
    </tbody>
</table>

## Limitations

* Applies to Native Kafka APIs only — executes during the `ENTRYPOINT_CONNECT` phase
* Unrecognized IP formats (for example, malformed CIDR or invalid range syntax) cause a `ClientAddressFilterInstantiationException` error for that filter entry
* Expression Language values that resolve to empty strings are silently ignored
* Requires Enterprise Edition license
