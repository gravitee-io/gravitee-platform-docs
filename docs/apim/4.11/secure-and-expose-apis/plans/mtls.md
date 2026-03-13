---
description: An overview about mtls.
metaLinks:
  alternates:
    - mtls.md
---

# mTLS

## Overview

The mTLS authentication type enforces the use of a client certificate when connecting to an API. The client certificate is added to an application, after which a subscription is created for that application. At runtime, the Gateway checks for a match between the incoming request's client certificate and a certificate belonging to an application with an active subscription.

You can use mTLS with or without TLS enabled between the client and the Gateway. The Gateway server can require client authentication, which uses the server-level truststore to determine trusted clients. The mTLS plan then evaluates the client certificate with Gateway-level TLS, which exists in either of the following locations:

* The TLS session between the client and the Gateway.
* A pre-specified header in plaintext, base64-encoded format.

Client authentication can occur if a load balancer is placed in front of the Gateway that terminates TLS.

## Limitations

Currently, mTLS plans have the following limitations:

* You can apply mTLS plans to only v4 APIs.
* You cannot use mTLS plans in Gravitee Cloud with SaaS-based Gateways.
* Only one client certificate can be added per application. This means that to rotate certificates for an application, you need to either pause the application's subscriptions or schedule a maintenance window to avoid traffic for that API.
* Applications do not provide a warning that certificates are going to expire.

## Restrictions

* mTLS plans cannot coexist with Keyless plans or authentication plans (OAuth2, JWT, API Key) in published state.
* Publishing an mTLS plan automatically closes all published Keyless and authentication plans.
* Publishing a Keyless or authentication plan automatically closes all published mTLS plans.
* Client certificates must be in PEM format for subscription creation.
* Gateway must be configured with `kafka.ssl.clientAuth=required` to enforce client certificate authentication for Kafka native APIs.
* Certificate validation failures result in `MtlsPolicyException` with error keys: `SSL_SESSION_REQUIRED`, `CLIENT_CERTIFICATE_INVALID`, `CLIENT_CERTIFICATE_MISSING`.

## How it works

When using an mTLS plan, you do not need to manually define a Gateway truststore. The Gateway automatically retrieves all certificates from [Applications (that have a TLS Configuration)](mtls.md#how-to-add-a-client-certificate) and loads them into an in-memory truststore.

## Initial Gateway configuration

To use an mTLS plan, you need to [enable HTTPS on your Gateway(s)](../../prepare-a-production-environment/configure-your-http-server.md#enable-https-support).

To enable HTTPS using the `values.yaml` file, use the following configuration to secure Gateway traffic and set the TLS client authentication option:

{% code title="Kubernetes values.yaml" %}
```yaml
gateway:
  # ... skipped for simplicity
  secured: true
  ssl:
    clientAuth: request # Supports none, request, required
    keystore:
      # ... skipped for simplicity
```
{% endcode %}

## Creating an mTLS plan

To create an mTLS plan for a Kafka native API:

1. Navigate to the API's **Plans** section in the Console.
2. Click **Add new plan**.
3. Select **mTLS** as the security type.
4. Configure the plan details (name, description, rate limits).
5. Click **Publish**.

If Keyless or authentication plans (OAuth2, JWT, API Key) are already published, the Console displays a confirmation dialog listing the plans that will be automatically closed. Click **Publish & Close** to proceed.

The Gateway validates that no conflicting plan types remain in published state. If conflicts are detected, the Gateway throws `NativePlanAuthenticationConflictException`.

## How to add a client certificate

To subscribe to an mTLS plan, the client has to add a certificate to their application. To add a certificate to an application, complete the following steps:

1. In the Console, navigate to **Applications**, and then click a specific application.
2. Within the application, click the **TLS Configuration** setting. The client certificate is pasted in base64-encoded format.

<!-- TODO: Screenshot of the TLS Configuration panel in the application settings, showing where to paste the client certificate in base64-encoded format -->
<figure><img src="../../.gitbook/assets/PLACEHOLDER-application-tls-configuration.png" alt="TLS Configuration panel in application settings"><figcaption><p>TLS Configuration panel in application settings</p></figcaption></figure>

{% hint style="warning" %}
Multiple applications in the same APIM instance may not share client certificates. You cannot save an application's configuration if its client certificate is already associated with another application.
{% endhint %}

When a client certificate is added to an application, the Gateway adds the application to its in-memory truststore. At runtime, the Gateway checks if a certificate in the truststore matches the certificate of an application subscribed to the API.

## Creating a subscription with mTLS

To create a subscription with mTLS:

1. Navigate to the application's **Subscriptions** page.
2. Select the mTLS plan.
3. Provide the client certificate in PEM format.

The subscription service computes the MD5 hash of the certificate and stores it as the security token. The Gateway's trust store manager loads the certificate into its internal registry.

When the client connects with the certificate, the Gateway extracts it from the TLS session, computes its MD5 hash, and matches it against registered subscriptions. On successful match, the Gateway populates the connection context with `planId`, `applicationId`, and `subscriptionId`. Metrics and analytics reflect the resolved subscription instead of ANONYMOUS.

## How to call an API

To call an API with mTLS, use the following command:

* Replace `<client.cer>` with the name of the file containing your client certificate.
* Replace `<client.key>` with the name of the file containing the client key.

```bash
$ curl –-cert  <client.cer> --key <client.key> https://my-gateway.com/mtls-api
```

Both the client certificate and the private key are required to ensure that your client trusts the certificate sent by the Gateway.

## Client configuration

Kafka clients must present the certificate during TLS handshake. Configure the client with the following SSL properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `ssl.keystore.location` | Path to client keystore containing the certificate | `/path/to/client.keystore.jks` |
| `ssl.keystore.type` | Client keystore type | `JKS` |
| `ssl.keystore.password` | Client keystore password | `gravitee` |

## How to terminate TLS

{% hint style="danger" %}
Starting with Gravitee APIM 4.5, client certificates processed by NGINX can only be extracted from headers in plaintext.
{% endhint %}

You can use an mTLS plan when you run a load balancer like NGINX in front of the Gateway. TLS is terminated at the load balancer, and the load balancer forwards traffic to the Gateway in plaintext.

The following blocks configure the Gateway to use mTLS:

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yaml" %}
```yaml
http:
  # ...
  ssl:
    clientAuthHeader:
      name: X-Gravitee-Client-Cert
    # ...
```
{% endcode %}
{% endtab %}

{% tab title="Kubernetes values.yaml" %}
{% code title="values.yaml" %}
```yaml
gateway:
  # ...
  ssl:
    clientAuthHeader:
      name: X-Gravitee-Client-Cert
    # ...
```
{% endcode %}
{% endtab %}
{% endtabs %}

When executing an mTLS plan, the Gateway checks if TLS is enabled.

* If TLS is enabled, the Gateway uses the certificate from the TLS handshake. The handshake occurs before plan selection.
* If TLS is not enabled, the Gateway checks for the certificate in the header. If the header contains a valid base64-encoded plaintext certificate matching a certificate for a subscribed application, the request succeed.

Ensure that only trusted parties can set the certificate header. If you are using a load balancer, the load balancer must be solely responsible for setting this header, and the Gateway should only be directly accessible through the load balancer.
