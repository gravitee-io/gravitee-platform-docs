### Gateway SSL Configuration

Configure the Gravitee gateway to require client certificate authentication for Native Kafka APIs. Set the following properties in the gateway configuration:

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.clientAuth` | Require client certificate authentication | `required` |
| `kafka.ssl.truststore.type` | Truststore format | `jks` |
| `kafka.ssl.truststore.path` | Path to truststore file | `/path/to/server.truststore.jks` |
| `kafka.ssl.truststore.password` | Truststore password | `gravitee` |

### Shared Configuration for Native Kafka Endpoint

Set the security protocol in the API's shared configuration. For mTLS, use `PLAINTEXT` as the protocol:

```json
{
    "security": {
        "protocol": "PLAINTEXT"
    }
}
```

### Client Configuration

Kafka clients must provide a keystore containing their certificate and private key. Configure the client with the following SSL properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.keystore.location` | Path to client keystore | `/path/to/client.keystore.jks` |
| `ssl.keystore.type` | Keystore format | `JKS` |
| `ssl.keystore.password` | Keystore password | `client-password` |

### Restrictions

mTLS plans cannot be published alongside Keyless plans or authentication plans (OAuth2, JWT, API Key) on the same Native Kafka API.
