---
noIndex: true
---

# Cleartext Support

While most modern web applications choose to encrypt all traffic, there remain cases where supporting cleartext communications is important. Ambassador Edge Stack supports both forcing [automatic redirection to HTTPS](cleartext-support.md#http-https-redirection) and [serving cleartext](cleartext-support.md#cleartext-routing) traffic on a `Host`.

{% hint style="info" %}
If no `Host`s are defined, Ambassador Edge Stack enables HTTP->HTTPS redirection. You will need to explicitly create a `Host` to enable cleartext communication at all.&#x20;
{% endhint %}

{% hint style="info" %}
The `Listener` and `Host` CRDs work together to manage HTTP and HTTPS routing. This document is meant as a quick reference to the `Host` resource: for a more complete treatment of handling cleartext and HTTPS, see [Configuring Ambassador Edge Stack Communications](../../edge-stack-user-guide/service-routing-and-communication/configuring-ambassador-edge-stack-communications.md).
{% endhint %}

### Cleartext Routing

To allow cleartext to be routed, set the `requestPolicy.insecure.action` of a `Host` to `Route`:

```yaml
requestPolicy:
  insecure:
    action: Redirect
```

This allows routing for either HTTP and HTTPS, or _only_ HTTP, depending on `tlsSecret` configuration:

* If the `Host` does not specify a `tlsSecret`, it will only route HTTP, not terminating TLS at all.
* If the `Host` does specify a `tlsSecret`, it will route both HTTP and HTTPS.

{% hint style="info" %}
If no `Host`s are defined, Ambassador Edge Stack enables HTTP->HTTPS redirection. You will need to explicitly create a `Host` to enable cleartext communication at all.&#x20;
{% endhint %}

{% hint style="info" %}
The `Listener` and `Host` CRDs work together to manage HTTP and HTTPS routing. This document is meant as a quick reference to the `Host` resource: for a more complete treatment of handling cleartext and HTTPS, see [Configuring Ambassador Edge Stack Communications](../../edge-stack-user-guide/service-routing-and-communication/configuring-ambassador-edge-stack-communications.md).
{% endhint %}

### HTTP->HTTPS redirection

Most websites that force HTTPS will also automatically redirect any requests that come into it over HTTP:

```
Client              Ambassador Edge Stack
|                             |
| http://<hostname>/api       |
| --------------------------> |
|                             |
| 301: https://<hostname>/api |
| <-------------------------- |
|                             |
| https://<hostname>/api      |
| --------------------------> |
|                             |
```

In Ambassador Edge Stack, this is configured by setting the `insecure.action` in a `Host` to `Redirect`.

```yaml
requestPolicy:
  insecure:
    action: Redirect
```

Ambassador Edge Stack determines which requests are secure and which are insecure using the `securityModel` of the `Listener` that accepts the request.

{% hint style="info" %}
If no `Host`s are defined, Ambassador Edge Stack enables HTTP->HTTPS redirection. You will need to explicitly create a `Host` to enable cleartext communication at all.&#x20;
{% endhint %}

{% hint style="info" %}
The `Listener` and `Host` CRDs work together to manage HTTP and HTTPS routing. This document is meant as a quick reference to the `Host` resource: for a more complete treatment of handling cleartext and HTTPS, see [Configuring Ambassador Edge Stack Communications](../../edge-stack-user-guide/service-routing-and-communication/configuring-ambassador-edge-stack-communications.md).
{% endhint %}
