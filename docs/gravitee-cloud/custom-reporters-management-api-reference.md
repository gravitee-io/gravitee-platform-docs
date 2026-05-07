
# Custom Reporters Management API Reference

### Management API

The following endpoints enable programmatic management of Custom Reporters:

| Method | Path | Description |
|:-------|:-----|:------------|
| POST | `/cloud/accounts/{accountId}/custom-reporters` | Create a custom reporter |
| GET | `/cloud/accounts/{accountId}/custom-reporters` | List all custom reporters |
| GET | `/cloud/accounts/{accountId}/custom-reporters/{customReporterId}` | Get a custom reporter by ID |
| PUT | `/cloud/accounts/{accountId}/custom-reporters/{customReporterId}` | Update a custom reporter |
| DELETE | `/cloud/accounts/{accountId}/custom-reporters/{customReporterId}` | Delete a custom reporter |
| PATCH | `/gateways/{accountId}/{gatewayId}/reporters` | Link a reporter to a gateway |
| DELETE | `/gateways/{accountId}/{gatewayId}/reporters/{reporterId}` | Unlink a reporter from a gateway |

### Reporter Configuration Properties

The following properties define a Custom Reporter configuration:

| Property | Description | Example |
|:---------|:------------|:--------|
| `name` | Reporter name (2-128 characters, pattern: `^[a-zA-Z0-9\s\-_.]+$`) | `Production TCP Reporter` |
| `reporterType` | Reporter type (currently only `TCP_REPORTER`) | `TCP_REPORTER` |
| `configuration.output` | Output format (currently only `json`) | `json` |
| `configuration.host` | Target hostname or IP (max 255 characters, no protocol prefix or path) | `tcp-reporter.example.com` |
| `configuration.port` | Target port (1-65535) | `8514` |
| `configuration.connectTimeout` | Connection timeout in milliseconds | `1000` |
| `configuration.reconnectAttempts` | Number of reconnect attempts | `10` |
| `configuration.reconnectInterval` | Interval between reconnect attempts in milliseconds | `500` |
| `configuration.retryTimeout` | Retry timeout in milliseconds | `5000` |
| `configuration.tlsEnabled` | Enable TLS (`true` or `false`) | `true` |
| `configuration.tlsVerifyClient` | Enable mutual TLS (`true` or `false`) | `true` |
| `configuration.keystoreType` | Keystore type (`JKS` or `PKCS12`) | `JKS` |
| `configuration.keystorePassword` | Keystore password (encrypted) | `changeit` |
| `configuration.keystoreContent` | Base64-encoded keystore file | `base64==` |
| `configuration.truststoreType` | Truststore type (`JKS` or `PKCS12`) | `PKCS12` |
| `configuration.truststorePassword` | Truststore password (encrypted) | `secret` |
| `configuration.truststoreContent` | Base64-encoded truststore file | `base64ts==` |
| `dataSelection` | Array of data types to forward | `["V2_LOGS", "V4_METRICS"]` |
| `gatewayIds` | Array of gateway IDs to link | `["gw-123", "gw-456"]` |
