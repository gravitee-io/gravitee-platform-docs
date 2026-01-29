---
description: Configuration guide for plugin support.
---

# Plugins support

## Plugins that support secrets

### Certificates

| Plugin          | Plugin version | Fields                                                    |
| --------------- | -------------- | --------------------------------------------------------- |
| Java Keystore   | 4.10.0 +       | <ul><li>Keystore password</li><li>Key password</li></ul>  |
| PKCS 12         | 4.10.0 +       | <ul><li>Keystore password</li><li>Key password</li></ul>  |
| AWS Certificate | 3.1.0 +        | <ul><li>Access key id</li><li>Secret access key</li></ul> |
| AWS CloudHSM    | 2.6.0 +        | <ul><li>Username</li><li>Password</li></ul>               |

