# Proxy

## Overview

Gravitee lets you define specific proxies for specific uses cases. Proxy configurations can be defined at the Gateway level or for individual APIs.&#x20;

You can define proxy settings for Gravitee using the `values.yaml` file or Gravitee-specific environment variables.&#x20;

{% hint style="info" %}
Proxy settings cannot be defined using the JAVA\_OPTS environment variable.
{% endhint %}

### Configure a proxy for the Gateway to connect with the Control Plane

The Gateway may be required to use a proxy service for external communication, such as connecting over the Internet to the Gravitee Cloud Control Plane.&#x20;

The following example configures the `values.yaml` file so that the Gateway can access the Management API using a proxy service.

Both the `management` and `gateway:management:http:proxy` sections must be configured.

```yaml
management:   
  type: http 

gateway:   
  management:     
    http:       
      proxy:
        enabled: true
        type: HTTP
        host: proxy.example.com
        port: 8080
        # username: proxy
        # password: secret
        # useSystemProxy: true # Reuses Gateway proxy config for other services too.
```

### Configure a proxy for sending Gateway metrics & logs to the Control Plane

If your Hybrid Gateway requires a proxy to connect to the Gravitee Cloud Control Plane, you must also define the following proxy configuration for the Cloud Reporter plugin. This plugin sends Gateway metrics and logs up to the control plane.

```yaml
gateway:
  reporters:
    cloud:
      client:
        proxy:
          enabled: true
          type: HTTP 
          host: proxy.example.com
          port: 8080
          # username: proxy
          # password: secret
```
