### Configuring Certificate-Based Authentication

Protected Resources support certificate-based JWT verification during token introspection. This enables secure signature validation when the token audience matches the Protected Resource's `clientId`.

#### Certificate Configuration Steps

1. Upload or reference a certificate in the domain's certificate store.
2. Assign the certificate to the Protected Resource by setting the `certificate` field.
   * **JDBC storage**: `nvarchar(64)`
   * **MongoDB storage**: `string`
3. During token introspection, if the audience matches the Protected Resource's `clientId` and a certificate is configured, the system uses the certificate for JWT signature verification.
4. If no certificate is configured, HMAC signing is assumed (represented as an empty certificate ID).

{% hint style="info" %}
Certificate assignment requires `PROTECTED_RESOURCE[UPDATE]` permission.
{% endhint %}

#### Certificate Deletion Restrictions

Certificates cannot be deleted if they are referenced by any Protected Resource. Attempting to delete a certificate in use returns a `CertificateWithProtectedResourceException` (HTTP 400) with the following message:

```
You can't delete a certificate with existing protected resources.
```

