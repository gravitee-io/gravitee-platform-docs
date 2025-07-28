# Deployments

## Console and Portal APIs

Gravitee APIM Management API lets you simultaneously expose the APIM Console and Developer Portal REST APIs. This speeds up configuration for new users discovering the platform.

If the Console and Developer Portal are not intended for the same category of users, we recommend that you deploy them on separate APIM instances, where the Console API is only enabled for instances dedicated to the Console and the Developer Portal API is only enabled for instances dedicated to the Developer Portal.&#x20;

In the `gravitee.yaml` file of instances dedicated to the Management Console:

* Enable the `console` parameter by setting `enabled = true`.
* Disable the `portal` parameter by setting `enabled = false`.

```yaml
http:
  api:
    console:
      enabled: true
    portal:
      enabled: false
```

In the `gravitee.yaml` file of instances dedicated to the Developer Portal:

* Enable the `console` parameter by setting `enabled = false`.
* Disable the `portal` parameter by setting `enabled = true`.

```yaml
http:
  api:
    console:
      enabled: false
    portal:
      enabled: true
```

With this configuration, the Console REST API remains publicly inaccessible even if you decide to expose your Developer Portal.

{% hint style="info" %}
For security, do not publicly expose either your Console or Developer Portal unless there is a compelling business requirement.&#x20;
{% endhint %}

## Enable HTTPS

To protect against man-in-the-middle attacks, ensure that your REST APIs are only reachable over HTTPS.

Methods to configure TLS depend on installation type. To let Gravitee manage the TLS connection directly, use the following configuration for the `jetty` section of `your gravitee.yaml` file:

```yaml
jetty:
  secured: true
  ssl:
    keystore:
      type: jks # Supports jks, pkcs12
      path: <keystore_path>
      password: <keystore_secret>
```

## Analytics

We recommend that you disable logging for APIs in a production environment. Logging impacts API performance. Also, to store the data in the Gateway memory, the heap pressure on the Gateway must increase, which can lead to a Gateway crash.&#x20;

If you need to enable logging in your production environment, complete the following step:

* In your `gravitee.yml` file, navigate to the `reporters` section, and then set the `max_size` to `256KB`. The default value is `-1`, which indicates no limit.&#x20;

Here is an example configuration:

```yaml
reporters:
# logging configuration
  logging:
    max_size: 256KB # max size per API log content respectively : client-request, client-response, proxy-request and proxy-response in MB (-1 means no limit)
```

{% hint style="info" %}
For hybrid Gateways that are connected to Gravitee Cloud, `max_size` is automatically set to 256KB unless the customer specifies a lower value.
{% endhint %}
