# Deployments

## Console and Portal APIs

Gravitee APIM Management API lets you simultaneously expose the APIM Console and Developer Portal REST APIs. This speeds up configuration for new users discovering the platform.

If the Console and Developer Portal are not intended for the same category of users, we recommend that you deploy them on separate APIM instances, where the Console API is only enabled for instances dedicated to the Console and the Developer Portal API is only enabled for instances dedicated to the Developer Portal.&#x20;

In the `gravitee.yaml` file of instances dedicated to the Management Console:

* Enable the `management` parameter by setting `enabled = true`.
* Disable the `portal` parameter by setting `enabled = false`.

```yaml
http:
  api:
    management:
      enabled: true
    portal:
      enabled: false
```

In the `gravitee.yaml` file of instances dedicated to the Developer Portal:

* Enable the `management` parameter by setting `enabled = false`.
* Disable the `portal` parameter by setting `enabled = true`.

```yaml
http:
  api:
    management:
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

## Logging

APIM lets you log the headers and payloads of requests at each stage of the processing flow. While logs provide valuable information, the logging process is resource-intensive.

{% hint style="warning" %}
Whenever possible, you should disable logging for APIs in a production environment. Logging impacts API performance, and storing data in the Gateway memory increases the heap pressure on the Gateway, which can lead to a Gateway crash.
{% endhint %}

To enable logging in your production environment, complete the following steps:

1. In your `gravitee.yml` file, navigate to the `reporters` section.
2. Set the `max_size` to `256KB`. The default value is `-1`, which indicates no limit.&#x20;

Here is an example configuration:

```yaml
reporters:
# logging configuration
  logging:
    max_size: 256KB # max size per API log content respectively : client-request, client-response, proxy-request and proxy-response in MB (-1 means no limit)
```

{% hint style="info" %}
For hybrid Gateways connected to Gravitee Cloud, `max_size` is automatically set to 256KB.
{% endhint %}

### LogGuard

Gravitee's LogGuard feature prevents the Gateway from experiencing an out-of-memory crash due to high throughput or large payloads. Once the memory pressure of the Gateway exceeds a certain threshold, LogGuard deactivates logging.

To enable LogGuard, you must complete the following steps:

* Enable the health probes in the `health` section of your `gravitee.yaml` file. LogGuard relies on the `gc-pressure` probe.
* Enable the `memory_pressure_guard` in the `reporters` section of your `gravitee.yaml` file.&#x20;

The GC pressure probe measures the percentage of CPU time used by the GC. To dynamically disable memory-consuming features, the probe output is sampled at a frequency defined by the `delay` parameter of the `health` configuration, and then compared to the pressure threshold specified by the `gcPressureThreshold` parameter.&#x20;

The following example configures the GC pressure probe:

```yaml
health:
    enabled: true
    delay: 5000
    unit: MILLISECONDS
    #The thresholds to determine if a probe is healthy or not
    threshold:
      cpu: 80 # Default is 80%
      memory: 80 # Default is 80%
      gc-pressure: 15 # Default is 15%
```

If the pressure exceeds the threshold, which is set to a default value of 15%, the `LogGuardService` activates a cooldown strategy with a fixed delay of 1 minute. The `LogGuardService` is configured in the `reporters` section of the `gravitee.yaml` file.

The following example configures `reporters` to enable LogGuard:

```yaml
reporters:
# logging configuration
  logging:
    max_size: -1 # max size per API log content respectively : client-request, client-response, proxy-request and proxy-response in MB (-1 means no limit)
    excluded_response_types: video.*|audio.*|image.*|application\/octet-stream|application\/pdf # Response content types to exclude in logging (must be a regular expression)
    memory_pressure_guard:
      enabled: true
      strategy:
        type: cooldown #type of strategy (default is cooldown)
        cooldown:
          duration: 60 #duration in seconds (default is 60 seconds)
```

{% hint style="warning" %}
If LogGuard is triggered, both the request body and response body are unavailable to the UI. They are replaced with the message `BODY NOT CAPTURED`. The request body and response body are also unavailable to external monitoring systems, such as Datadog.
{% endhint %}
