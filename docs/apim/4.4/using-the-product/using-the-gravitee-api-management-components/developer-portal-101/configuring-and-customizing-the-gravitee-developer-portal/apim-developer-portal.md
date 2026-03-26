---
description: >-
  Configuration guide for Configuring the Gravitee API Management Developer
  Portal.
---

# Configuring the Gravitee API Management Developer Portal

## Configuration file

The configuration file for APIM Portal is `assets\config.json`. The default configuration is shown below:

{% code title="config.json" %}
```json
{
  "baseURL": "/portal/environments/DEFAULT",
  "homepage": {
    "featured": {
      "size": 9
    }
  },
  "loaderURL": "assets/images/gravitee-loader.gif",
  "pagination": {
    "size": {
      "default": 10,
      "values": [5, 10, 25, 50, 100]
    }
  }
}
```
{% endcode %}

The only mandatory value in `config.json` file is `baseURL`, which describes the location of the APIM API Portal endpoint. You must set this value for APIM Portal to send requests to the endpoint.
