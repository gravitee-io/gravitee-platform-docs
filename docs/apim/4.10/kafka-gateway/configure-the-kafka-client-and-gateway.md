## Technical Prerequisites

For mTLS to work correctly, both the Kafka Gateway and Kafka clients must be configured with specific SSL components.

### Gateway Requirements

The Kafka Gateway must be configured with:

- **Keystore**: Contains the Gateway private key and certificate
- **Truststore**: Contains the Certificate Authorities (CAs) that signed client certificates
- **Client authentication**: Must be enabled

### Client Requirements

The Kafka client must be configured with:

- **Keystore**: Contains the client private key and certificate
- **Truststore**: Contains the CA that signed the Gateway certificate

### Required SSL Files

<!-- GAP: The source mentions "Required SSL Files" as a section heading but provides no content under it. Clarification needed on what specific files or file formats should be documented here. -->

## Configure Gateway for mTLS

To enable mTLS for native Kafka APIs, configure the Gateway's SSL settings in `gravitee.yml`. This configuration defines the keystore, truststore, and client authentication mode.

### Gateway SSL configuration

Add the following configuration to the `kafka.ssl` section of `gravitee.yml`:

```yaml
kafka:
  ssl:
    # Gateway keystore
    # Contains the Gateway private key and certificate
    keystore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.keystore.jks
      password: gravitee

    # Gateway truststore
    # Contains the CAs that signed client certificates
    truststore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.truststore.jks
      password: gravitee

    # Client authentication mode
    clientAuth: required             # required | request | none
```

### Configuration parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `keystore.type` | Keystore format: `jks`, `pkcs12`, or `pem` | Yes |
| `keystore.path` | Path to the Gateway keystore file | Yes |
| `keystore.password` | Password for the Gateway keystore | Yes |
| `truststore.type` | Truststore format: `jks`, `pkcs12`, or `pem` | Yes |
| `truststore.path` | Path to the Gateway truststore file | Yes |
| `truststore.password` | Password for the Gateway truststore | Yes |
| `clientAuth` | Client authentication mode: `required`, `request`, or `none` | Yes |

{% hint style="warning" %}
Set `clientAuth` to `required` to enforce mTLS. The Gateway will reject any client connection without a valid certificate.
{% endhint %}

### SSL file requirements

The Gateway requires the following SSL files:

- **Keystore**: Contains the Gateway's private key and certificate
- **Truststore**: Contains the certificate authorities (CAs) that signed the client certificates

Ensure these files are accessible at the paths specified in `gravitee.yml` and that the Gateway process has read permissions.