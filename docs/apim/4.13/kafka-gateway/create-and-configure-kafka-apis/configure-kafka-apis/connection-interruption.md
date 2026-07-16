# Connection interruption in the Entrypoint Connect phase

## Template engine variables

Policies in the Entrypoint Connect phase have access to the following Expression Language (EL) variables:

| Variable | Description | Example |
|:---------|:------------|:--------|
| `connection.id` | Unique connection identifier | `"conn-12345"` |
| `connection.remoteAddress` | Client remote IP and port | `"192.168.1.100:54321"` |
| `connection.localAddress` | Gateway local IP and port | `"10.0.0.5:9092"` |
| `ssl` | TLS session information (if SSL configured) | Certificate chain, protocol version |
| `context.attributes` | Execution context attributes | Custom attributes set by policies |
| `context.remoteAddress` | Alias for `connection.remoteAddress` | `"192.168.1.100:54321"` |
| `context.localAddress` | Alias for `connection.localAddress` | `"10.0.0.5:9092"` |

The `principal` variable is not available because authentication has not occurred yet.
