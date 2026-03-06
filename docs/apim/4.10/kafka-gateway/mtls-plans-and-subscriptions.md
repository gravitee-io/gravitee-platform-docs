### Gateway Configuration

Configure the gateway to require and validate client certificates for Kafka connections.

| Property | Description | Example |
|:---------|:------------|:--------|
| `kafka.ssl.clientAuth` | Require client certificate authentication | `"required"` |
| `kafka.ssl.truststore.type` | Truststore format for verifying client certificates | `"jks"` |
| `kafka.ssl.truststore.password` | Password for the truststore | `"gravitee"` |
| `kafka.ssl.truststore.path` | Path to truststore file containing client CA certificates | `/path/to/server.truststore.jks` |

### Creating an mTLS Plan

Define a plan with security type `"mtls"` and an empty configuration object:

```json
{
  "id": "plan-mtls-id",
  "name": "mTLS plan",
  "security": {
    "type": "mtls",
    "configuration": {}
  },
  "mode": "standard",
  "status": "published"
}
```

Publish the plan through the management console or API. The system validates that no conflicting plan types (Keyless or Authentication) are currently published. If conflicts exist, you are prompted to confirm automatic closure of the conflicting plans. Once published, the plan enforces certificate validation for all client connections, matching the client certificate digest against active subscriptions.

### Creating a Subscription with mTLS

Generate or obtain a client certificate signed by a CA trusted by the gateway. Encode the certificate in Base64 format and include it in the subscription request under the `clientCertificate` field. The gateway stores the certificate digest and uses it to authorize connections during the TLS handshake.

Configure the Kafka client with the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.keystore.location` | Path to client keystore file | `/path/to/client.keystore.jks` |
| `ssl.keystore.type` | Keystore format | `"JKS"` |
| `ssl.keystore.password` | Password for the keystore | `"gravitee"` |

When the client connects, the gateway extracts the certificate from the TLS session, computes its digest, and matches it against the subscription record.

### Restrictions

* Kafka APIs cannot have Keyless, mTLS, and Authentication (OAuth2, JWT, API Key) plans published simultaneously.
* Publishing a plan in one authentication category automatically closes all published plans in other categories.
