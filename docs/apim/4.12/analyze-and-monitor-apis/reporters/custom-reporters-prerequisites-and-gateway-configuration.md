# Custom Reporters Prerequisites and Gateway Configuration

## Prerequisites

Before configuring Custom Reporters, ensure the following requirements are met:

* Enterprise license with tier `galaxy` or `universe`
* `customReporters` feature flag enabled in the `release_toggles` collection
* RSA public key configured for password encryption (see [Encryption Key](#encryption-key))
* Account member role with permissions to manage custom reporters

## Gateway Configuration

### Encryption Key

Custom Reporters use RSA-OAEP/SHA-256 encryption to protect keystore and truststore passwords. Configure the platform's RSA public key using the `platform.encryption.public-key` property or the `gravitee_platform_encryption_public-key` environment variable.

| Property | Description | Example |
|:---------|:------------|:--------|
| `platform.encryption.public-key` | Base64-encoded DER RSA public key for encrypting keystore and truststore passwords (RSA-OAEP/SHA-256). Generate with: `openssl genrsa 2048 \| openssl rsa -pubout -outform DER \| base64 -w0` | `MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...` |

**Example (gravitee.yml)**:

```yaml
platform:
  encryption:
    public-key: <your-base64-encoded-der-public-key>
```

**Example (docker-compose.yml)**:

```yaml
- gravitee_platform_encryption_public-key=${GRAVITEE_PLATFORM_ENCRYPTION_PUBLIC_KEY}
```

### Data Plane Reporter Deployment

When a reporter is linked to a gateway, the platform deploys a configuration payload to the data plane. The payload includes TCP connection settings, TLS credentials (if enabled), and data type exclusions. The `log` and `request` sections exclude all types by default, allowing only the selected data types to be forwarded.

**Example Payload**:

```json
{
  "tcp": {
    "enabled": true,
    "host": "tcp-reporter.example.com",
    "port": 8514,
    "output": "json",
    "connectTimeout": 1000,
    "reconnectAttempts": 10,
    "reconnectInterval": 500,
    "retryTimeout": 5000,
    "tls": {
      "enabled": true,
      "verifyClient": true,
      "keystore": {
        "type": "JKS",
        "password": "changeit",
        "content": "base64=="
      },
      "truststore": {
        "type": "PKCS12",
        "password": "secret",
        "content": "base64ts=="
      }
    },
    "log": { "exclude": ["*"] },
    "request": { "exclude": ["*"] }
  }
}
```

