# Deployments

## Console and Portal APIs

Gravitee APIM Management API allows the simultaneous exposure of both Console and Developer Portal REST APIs. This enables quick setup when discovering the platform.

If the Console and Developer Portal are not intended to be used by the same category of users, it is **recommended to deploy them on distinct instances**.

You can deploy instances dedicated to the Management Console with the Portal API disabled on one side:

```yaml
http:
  api:
    console:
      enabled: true
    portal:
      enabled: false
```

On the other side, you can deploy another dedicated couple of instances for the Developer Portal by disabling the Console API:

```yaml
http:
  api:
    console:
      enabled: false
    portal:
      enabled: true
```

The Console REST API will remain inaccessible to the outside world if you decide to make your Developer Portal reachable from outside of your company. However, Gravitee recommends that you do not expose your Console or Developer Portal publicly if there is no particular business requirement.&#x20;

Refer to the [Gravitee documentation](/apim/getting-started/configuration/configure-apim-management-api/internal-api#configure-the-management-and-portal-apis) for more information about Console and Portal APIs.

## Enable HTTPS

Whatever solution you rely on, **make sure your REST APIs are only reachable over HTTPS** to protect against man-in-the-middle attacks.

There are several ways to configure TLS depending on your type of installation. One way is to let Gravitee manage the TLS connection directly by configuring it:

```yaml
jetty:
  secured: true
  ssl:
    keystore:
      type: jks # Supports jks, pkcs12
      path: <keystore_path>
      password: <keystore_secret>
```

You can find additional details regarding HTTPS support for REST APIs in the[ Gravitee documentation](/apim/getting-started/configuration/configure-apim-management-api/internal-api#enable-https-support).
