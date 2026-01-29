---
description: An overview about update the connection to cloud.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/upgrade-guides/update-the-connection-to-cloud
---

# Update the Connection to Cloud

## Overview

APIM 4.2 brings improved management of multi-tenancy mode, where one APIM installation now tends to multiple tenants on either the Organization on Environment level.\
\
Multi-tenancy support in Gravitee 4.2 necessitated changes to both APIM and Cloud, but customer deployments may continue to function as `standalone` APIM installations. A `standalone` installation behaves the same as APIM 4.1 connected to Cloud.\
\
APIM installations connected to Cloud require changes to the Management API's `gravitee.yml` file.

## APIM 4.2 with Cloud connected

{% hint style="warning" %}
The user must edit the Management API's `gravitee.yaml`.
{% endhint %}

If an APIM installation connected to Cloud is upgraded to 4.2, the user must make the following changes to the Management API's `gravitee.yaml` file for the installation to function as `standalone`:

```yaml
installation:
  type: standalone # Could be either standalone, multi-tenant; Default is standalone.
  # Specify the URL of Management API of this instance, mandatory if you want to connect it to Cloud
  api:
    # Specify the URLs of Management API, mandatory if you want to connect it to Cloud with a standalone installation
    url: http://localhost:8083
    proxyPath:
      management: ${http.api.management.entrypoint} # By default /management
      portal: ${http.api.portal.entrypoint}  # By default /portal
  standalone:
    # Specify the URL of Console UI of this instance, mandatory if you want to connect it to Cloud with a standalone installation
    console:
      url: http://localhost:3000
    # Specify the URL of Portal UI of this instance
    portal:
      url: http://localhost:4100
```

## APIM 4.2+ and multiple Consoles/Portals in a connected Cloud

{% hint style="warning" %}
The user must edit the Management API's `gravitee.yaml`.
{% endhint %}

If an APIM installation with multiple Consoles and/or Portals set up in a connected Cloud is upgraded to 4.2, the user must make the following changes to the Management API's `gravitee.yaml` file for the installation to function as `standalone`:

```yaml
installation:
  type: standalone # Could be either standalone, multi-tenant; Default is standalone.
  # Specify the URL of Management API of this instance, mandatory if you want to connect it to Cloud
  api:
    proxyPath:
      management: ${http.api.management.entrypoint} # By default /management
      portal: ${http.api.portal.entrypoint}  # By default /portal
  standalone:
    api:
    # Specify the URLs of Management API, mandatory if you want to connect it to Cloud with a standalone installation
      url: http://localhost:8083
    # Specify the URL of Console UI of this instance, mandatory if you want to connect it to Cloud with a standalone installation
    console:
      urls:
        - orgId: DEFAULT
          url: http://localhost:3000
        - orgId: organization#2
          url: http:/localhost:3001
    portal:
      urls:
        - envId: DEFAULT
          url: http://localhost:4100
        - envId: environment#2
          url: http:/localhost:4101
```
