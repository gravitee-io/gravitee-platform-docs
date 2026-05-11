# Gateway Configuration for Custom Reporters

## Gateway Configuration

### Encryption Key

The gateway requires a public encryption key to process sensitive reporter fields before deployment. Configure this property in the gateway's environment configuration.

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee_platform_encryption_public-key` | RSA-OAEP/SHA-256 public key in Base64 DER format for encrypting sensitive reporter fields | `MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...` |


