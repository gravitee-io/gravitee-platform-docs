---
description: The restrictions that apply to custom TCP, Datadog, and OpenTelemetry reporters in Gravitee Cloud. Browse them before you configure a reporter for your gateways.
---

# Custom Reporters Reference

## Restrictions

- Three reporter types are available: TCP, Datadog, and OpenTelemetry. The type of an existing reporter is read-only. To switch types, delete the reporter and create a new one
- A Datadog reporter doesn't send the Kafka event metrics
- A Datadog reporter targets only the following Datadog sites: `datadoghq.com`, `us3.datadoghq.com`, `us5.datadoghq.com`, `datadoghq.eu`, and `ddog-gov.com`
- The Datadog log bulk size is between 1 and 1000
- Datadog custom tags start with a letter, accept only letters, digits, and the characters `_`, `-`, `:`, `.`, and `/`, and are at most 200 characters
- A Datadog proxy host contains no scheme (`http://`, `https://`, or a SOCKS4 or SOCKS5 scheme), no path, no whitespace, and no control characters
- An OpenTelemetry reporter sends traces and logs only. It doesn't send metrics and has no data selection
- The OpenTelemetry traces endpoint is an `http` or `https` URL of at most 255 characters, without credentials and without a signal path such as `/v1/traces`. It must use `https` when TLS is enabled
- The OpenTelemetry logs endpoint is an `http` or `https` URL of at most 255 characters, without credentials, and includes the signal path, for example `/v1/logs`. It's required when logs are enabled
- The OpenTelemetry timeout is between 1000 and 60000 milliseconds
- An OpenTelemetry reporter carries at most 20 headers. A header name is at most 128 characters and is unique, compared without case. A header value is at most 446 printable ASCII characters
- An OpenTelemetry extra attribute is a `key:value` pair. The key starts with a letter and accepts only letters, digits, and the characters `_`, `-`, `.`, and `/`. Neither part contains a comma, and each part is at most 200 characters
- An OpenTelemetry Kafka operation name starts with a letter, accepts only letters, digits, and `_`, and is at most 64 characters
- OpenTelemetry TLS and proxy settings apply to traces only
- A Gateway is linked to one reporter of each type at a time. Linking another reporter of the same type from the **Reporters** page of the Gateway replaces the current one
- Only JSON output format is supported
- Gateway Monitoring Metrics data type is always excluded from export
- Reporter names must match the pattern `^[a-zA-Z0-9\s\-_.]+$`
- Host field cannot contain protocol prefixes like`http://`, `https://`, `tcp://`, or paths
- Host field cannot contain whitespace or control characters
- TLS certificate files must be JKS or PFX format
- TLS certificate files must be 2 MB or smaller
- When TLS is enabled, all three fields, type, password, content, must be provided for each store (keystore and truststore)
- Password fields display a masked placeholder (`********`) for existing values; actual passwords cannot be retrieved after initial entry
- Updating a reporter re-deploys only to gateways with `DEPLOYED` status and not `PENDING` or `DELETING`.
- Configuration keys changed from seconds to milliseconds in recent versions; existing reporters must migrate values. For example, `connectionTimeoutSeconds: "30"` becomes `connectTimeout: "1000"`)

<figure><img src="../../.gitbook/assets/gravitee-cloud-custom-reporters-step-07.png" alt="Gateway selection dialog showing no eligible gateways found message with eligibility requirements"><figcaption></figcaption></figure>
