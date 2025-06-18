# TCP Reporter

## Configuration

The TCP reporter has the following configuration parameters:

| Parameter name            | Description                                                                                                                                                           | Default value |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `enabled`                 | This setting determines whether the TCP reporter should be started or not. The default value is `false`.                                                              | false         |
| `output`                  | Format of the data written to the TCP socket - json, message\_pack, elasticsearch, csv.                                                                               | json          |
| `host`                    | The TCP host where the event should be published. This can be a valid host name or an IP address.                                                                     | localhost     |
| `port`                    | The TCP port used to connect to the host.                                                                                                                             | 8123          |
| `connectTimeout`          | Maximum time allowed to establish the TCP connection in milliseconds.                                                                                                 | 10000         |
| `reconnectAttempts`       | This setting determines how many times the socket should try to establish a connection in case of failure.                                                            | 10            |
| `reconnectInterval`       | Time (in milliseconds) between socket connection attempts.                                                                                                            | 500           |
| `retryTimeout`            | If the max reconnect attempts have been reached, this setting determines how long (in milliseconds) the reporter should wait before trying to connect again.          | 5000          |
| `tls.enabled`             | Enable TLS                                                                                                                                                            | false         |
| `tls.verifyClient`        | If true, client certificate will be sent for mutual TLS negotiation. When enabling this, providing a key-store is required so that mutual TLS negotiation can happen. | false         |
| `tls.keystore.type`       | The type of key-store to use (either PEM, JKS or PFX)                                                                                                                 | null          |
| `tls.keystore.password`   | The password to use for the key-store (only for JKS and PFX types)                                                                                                    | null          |
| `tls.keystore.certs`      | The list of certificates used, when type is PEM                                                                                                                       | null          |
| `tls.keystore.keys`       | The list of keys used, when type is PEM                                                                                                                               | null          |
| `tls.truststore.type`     | The type of trust-store to use (either PEM, JKS or PFX)                                                                                                               | null          |
| `tls.truststore.password` | The password to use for the trust-store (only for JKS and PFX types)                                                                                                  | null          |
| `tls.truststore.certs`    | The list of certificates to trust, when type is PEM                                                                                                                   | null          |

## Example

The following example uses the same configuration as the file reporter example above, but writes the events to a TCP socket instead of a file:

```yaml
reporters:
  tcp:
    enabled: true
    host: localhost
    port: 9001
    output: json
    request:
      exclude:
        - "*"
      include:
        - api
        - application
      rename:
        application: app
    log:
      exclude:
        - "*"
    node:
      exclude:
        - "*"
    health-check:
      exclude:
        - "*"
    tls:
      enabled: true
      verifyClient: true
      keystore: 
        type: pem
        keys:
        - client.key
        certs:
        - client.crt
      truststore:
        type: pem 
        certs:
        - logstash.crt
```
