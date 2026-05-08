# Custom Reporters Gateway Configuration

## Gateway Configuration

### Encryption Key

Configure the RSA public key for encrypting reporter passwords. The key must be a Base64-encoded DER-format RSA public key.

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee_platform_encryption_public-key` | RSA public key for encrypting sensitive reporter fields (RSA-OAEP/SHA-256) | `MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...` |
| `reporters.encryption.public-key` | RSA public key for encrypting reporter passwords | `MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...` |

Generate the key using:

```bash
openssl genrsa 2048 | openssl rsa -pubout -outform DER | base64 -w0
```

### Feature Flag

Enable the Custom Reporters feature using the `customReporters` release toggle. The default value is `false`.
