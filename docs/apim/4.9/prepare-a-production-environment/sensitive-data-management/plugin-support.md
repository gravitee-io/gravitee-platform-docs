---
description: Configuration guide for plugin support.
---

# Plugin support

## Plugins that support secrets

### Native endpoints

| Endpoint | Configuration FIeld                                   |
| -------- | ----------------------------------------------------- |
| Kafka    | Bootstrap server list, JAAS config, TLS configuration |

### Endpoints

<table><thead><tr><th width="212">Endpoint</th><th>Configuration Field</th></tr></thead><tbody><tr><td>HTTP Proxy</td><td>Target URL, header value fields, proxy fields for client connection, TLS configuration</td></tr><tr><td>Kafka</td><td>Bootstrap server list, JAAS config, TLS configuration</td></tr><tr><td>MQTT</td><td>Server host and port, username, password, TLS configuration</td></tr><tr><td>RabbitMQ</td><td>Server host and port, username, password, TLS configuration</td></tr><tr><td>Solace</td><td>URL and VPN name, username, password, truststore configuration</td></tr></tbody></table>

### Resources

<table><thead><tr><th width="213">Resource</th><th>Configuration Field</th></tr></thead><tbody><tr><td>OAuth2</td><td>Client ID, client secret</td></tr><tr><td>Redis Cache</td><td>Password</td></tr><tr><td>LDAP</td><td>LDAP URL, base DN, username, password</td></tr></tbody></table>

### Policies

<table><thead><tr><th width="216">Policy</th><th>Configuration Field</th></tr></thead><tbody><tr><td>HTTP Callout</td><td>URL, header values</td></tr><tr><td>Assign attribute</td><td>Attribute value</td></tr><tr><td>Transform headers</td><td>Header value</td></tr><tr><td>Transform query param</td><td>Param value</td></tr><tr><td>Traffic shadowing</td><td>URL, header values</td></tr><tr><td>Any other that supports EL</td><td></td></tr></tbody></table>
