# RPM

## Prerequisites

Follow the instructions to [#prepare-your-installation](./#prepare-your-installation "mention").

## Install the Gateway

Below is a sample working configuration for the RPM use case. It configures both the proxy and Redis.

```yaml
management:
  # HTTP TYPE FOR THE GRAVITEE CLOUD GATE
  type: http 
  # OPTIONAL PROXY CONFIG
  # http:
  #   proxy:
  #     useSystemProxy: false
  #     enabled: true
  #     type: HTTP
  #     host: proxy.example.com
  #     port: 8080
  #     username: proxy-username
  #     password: proxy-password

# CLOUD TOKEN TO SECURE CONNECTION TO THE CLOUD GATE
cloud:
  token: YOUR-CLOUD-TOKEN

# REDIS TO STORE AND SHARE BETWEEN GATEWAYS INSTANCES (HA)
# THE RATE LIMIT / QUOTA COUNTERS AND CACHE DATA
ratelimit:
  type: none
  # type: redis
  # redis:
  #   host: localhost
  #   port: 6379
  #   password:

# LICENCE KEY B64 ENCODED
license:
  key: YOUR-LICENCE-KEY
```

## Verification

From the Gravitee Cloud Dashboard, you can see your configured Gateway.

<figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

To verify that the Gateway is running, make a GET request to the URL on which you have published the Gateway. The output is a default message similar to:

```
No context-path matches the request URI.
```

You can now create and deploy APIs to your hybrid Gateway.
