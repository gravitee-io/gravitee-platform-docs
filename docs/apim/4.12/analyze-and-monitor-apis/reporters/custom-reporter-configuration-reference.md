# Custom Reporter Configuration Reference

## Gateway Configuration

### Encryption Key

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee_platform_encryption_public-key` | Base64-encoded DER RSA public key for encrypting keystore and truststore passwords | `MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...` |

### Reporter Deployment Payload

The gateway receives reporter configuration as a JSON payload with the following structure. Numeric timeout values are in milliseconds. Keystore Password and Truststore Password fields contain decrypted values.

```json
{
  "tcp": {
    "enabled": true,
    "host": "logs.example.com",
    "port": 8514,
    "output": "json",
    "connectTimeout": 1000,
    "reconnectAttempts": 10,
    "reconnectInterval": 500,
    "retryTimeout": 5000,
    "tls": {
      "enabled": true,
      "verifyClient": false,
      "keystore": {
        "type": "JKS",
        "password": "decrypted-password",
        "content": "base64-encoded-keystore"
      },
      "truststore": {
        "type": "PKCS12",
        "password": "decrypted-password",
        "content": "base64-encoded-truststore"
      }
    },
    "log": { "exclude": ["*"] },
    "request": { "exclude": ["*"] }
  }
}
```

## Creating a Custom Reporter

To create a custom reporter, navigate to the Custom Reporters page under account settings. Click **Create Custom Reporter** and complete the setup form.

1. Enter a unique name (2–128 characters, alphanumeric with spaces, hyphens, underscores, and periods).
2. Provide the TCP endpoint host (hostname or IP, no protocol prefix or path) and port (1–65535).
3. Configure connection behavior: Connection Timeout, Reconnect Attempts, Reconnect Interval, and Retry Timeout (all in milliseconds).
4. Select at least one data type to export.
5. Optionally enable TLS, upload keystore and truststore files (JKS or PKCS12, max 2 MB each), and provide passwords.
6. Optionally link the reporter to one or more gateways by selecting gateway IDs.
7. Click **Save** to create the reporter and deploy it to linked gateways asynchronously.

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-05.png" alt="Edit custom reporter page showing basic configuration, gateways section, connection settings, TLS configuration, and data selection"><figcaption></figcaption></figure>

## End-User Configuration

### Reporter Properties

| Property | Description | Example |
|:---------|:------------|:--------|
| Name | Reporter display name | `Production Logs` |
| Host | TCP server hostname or IP (no protocol, no path, max 255 characters) | `logs.example.com` |
| Port | TCP server port | `8514` |
| Output Format | Data serialization format (JSON only) | `json` |
| Connection Timeout | Connection timeout in milliseconds | `1000` |
| Reconnect Attempts | Number of reconnection attempts | `10` |
| Reconnect Interval | Reconnection interval in milliseconds | `500` |
| Retry Timeout | Retry timeout in milliseconds | `5000` |
| TLS Enabled | Enable TLS encryption | `true` |
| Verify Client | Require client certificate verification | `false` |
| Keystore Type | Keystore format | `JKS` or `PKCS12` |
| Keystore Password | Keystore password (encrypted at rest) | `********` |
| Keystore Content | Base64-encoded keystore file | `MIIKEQIBAzCCCd...` |
| Truststore Type | Truststore format | `JKS` or `PKCS12` |
| Truststore Password | Truststore password (encrypted at rest) | `********` |
| Truststore Content | Base64-encoded truststore file | `MIIKEQIBAzCCCd...` |

### Management API

| Method | Path | Description |
|:-------|:-----|:------------|
| POST | `/cloud/accounts/{accountId}/custom-reporters` | Create a custom reporter |
| GET | `/cloud/accounts/{accountId}/custom-reporters` | List all custom reporters for the account |
| GET | `/cloud/accounts/{accountId}/custom-reporters/{reporterId}` | Retrieve a specific custom reporter |
| PUT | `/cloud/accounts/{accountId}/custom-reporters/{reporterId}` | Update a custom reporter |
| DELETE | `/cloud/accounts/{accountId}/custom-reporters/{reporterId}` | Delete a custom reporter |
| PATCH | `/gateways/{accountId}/{gatewayId}/reporters` | Link a reporter to a gateway |
| DELETE | `/gateways/{accountId}/{gatewayId}/reporters/{reporterId}` | Unlink a reporter from a gateway |

## Restrictions

- Output format is restricted to JSON only (CSV, MessagePack, and Elasticsearch formats removed)
- Gateway Monitoring Metrics data type is always excluded from export, even if selected
- Keystore and truststore file uploads are limited to 2 MB each
- Requires enterprise license with Galaxy or Universe tier
- Host field must not include protocol prefixes (`http://`, `https://`, `tcp://`) or path segments
- Host field is limited to 255 characters and cannot contain whitespace or control characters
- Port must be between 1 and 65535
- At least one data type must be selected
- When keystore or truststore is configured, all three fields (type, password, content) are required
- Password fields in edit mode display a placeholder (`********`); actual values are not retrievable from the backend
- Gateway linking and reporter deployment are asynchronous; failures are logged but do not block create/update operations

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-07.png" alt="Gateway selection dialog showing no eligible gateways found message with eligibility requirements"><figcaption></figcaption></figure>

## Related Changes

Configuration key names changed from seconds-based to milliseconds-based:

| Old Key | New Key |
|:--------|:--------|
| `connectionTimeoutSeconds` | `connectTimeout` |
| `reconnectIntervalSeconds` | `reconnectInterval` |
| `retryTimeoutSeconds` | `retryTimeout` |

Sensitive fields (Keystore Password, Truststore Password) are encrypted at rest using RSA-OAEP/SHA-256. A new MongoDB collection (`account_reporters`) stores reporter configurations. A Liquibase changeset adds the `customReporters` feature toggle (default inactive).
