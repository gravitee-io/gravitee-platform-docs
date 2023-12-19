---
description: >-
  This page discusses how to deploy APIM and Cockpit together in multi-tenant
  mode
---

# Multi-tenancy

## Overview

{% hint style="warning" %}
Multi-tenancy requires an [enterprise-enabled Gravitee Cockpit account](https://documentation.gravitee.io/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee#enterprise-version-of-gravitee-cockpit).&#x20;

To learn more about Gravitee Enterprise and what's included in various enterprise packages, [book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/) or [check out the pricing page](https://www.gravitee.io/pricing).
{% endhint %}

Gravitee uses the term multi-tenancy to describe a configuration in which:&#x20;

* A single APIM installation supports multiple Organizations and Environments created through Cockpit. Each tenant can be either an Organization or an Environment.
* Features and data are isolated between tenants.
* Dedicated URLs to access APIM components and APIs deployed on Gravitee Gatways. These URLs are labeled as Access Points.

{% hint style="info" %}
The way in which data and features are isolated between the logical hierarchical structures of APIM enables the existence of a multi-tenant Developer Portal.
{% endhint %}

APIM 4.2 implements changes to how Organizations and Environments are managed, in addition to the configuration that is propagated from Gravitee Cockpit. The following sections cover:

* How to configure a multi-tenant installation with Gravitee 4.2, including Access Points
* How to run a standalone (not multi-tenant) installation after APIM and/or Cockpit have been upgraded to support multi-tenancy

## How to set up multi-tenancy

{% hint style="info" %}
The following instructions are guidelines that apply to both Gravitee Cloud and self-hosted customers who want to run a multi-tenant APIM installation.
{% endhint %}

Multi-tenancy is an enterprise feature. In order to use it, you need to:&#x20;

* Enable APIM's multi-tenancy mode
* Connect the APIM installation to an enterprise-enabled Gravitee Cockpit account
* Enable the Access Points feature

Follow the steps below to implement best practices for APIM multi-tenancy.

{% hint style="warning" %}
Once a multi-tenant APIM is connected to Cockpit, it is not possible to disable multi-tenancy mode in APIM.
{% endhint %}

1. [Install APIM](./) on your preferred infrastructure and deployment type
2. Explicitly set APIM to multi-tenant mode by commenting out the multi-tenant section in the configuration. Optionally, you can specify the configuration of Access Points, which comprises the URLs that APIM components will be addressed on.&#x20;

{% hint style="info" %}
Cockpit is able to interpret a variabilized Access Point structure. Cockpit will interpret non-variabilized instructions literally, which may result in multiple Environment components receiving the same Access Point configuration.
{% endhint %}

```yaml
installation:
  type: multi-tenant
  multi-tenant:
    # Specify the Access Points of your installation, mandatory if you want to connect it to Cockpit with a multi-tenant installation
    # You can use template variable such as {account}, {organization} or {environment}
    accessPoints:
      organization:
        console:
          host: '{organization}.{account}.example.com'
          secured: true
        console-api:
          host: '{organization}.{account}.example.com'
          secured: true
      environment:
        portal:
          host: '{environment}.{organization}.{account}.example.com'
          secured: true
        portal-api:
          host: '{environment}.{organization}.{account}.example.com'
          secured: true
        gateway:
          host: '{environment}.{organization}.{account}.example.com'
          secured: true
```

3. Sign in to your enterprise version of Gravitee Cockpit and
   * Create one Organization
   * Create one Environment
4. Link your APIM installation to the Environment you created by following [these instructions](https://documentation.gravitee.io/gravitee-cloud/guides/register-installations). Your APIM installation will be recognized by Cockpit as multi-tenant and send templated Access Points to the connected Environment.
5. Add a new Environment within the same Organization and connect it to the multi-tenant APIM installation

{% hint style="success" %}
Congratulations, you can now enjoy the benefits of multi-tenancy!
{% endhint %}

## Access Points

The Access Points feature allows different tenants to use dedicated URLs to access resources. The following tips and caveats apply to the configuration and use of Access Points:

* As Access Points rely on proper mapping, e.g., through a load balancer, you may need to edit your `etc/hosts` file prior to local testing.
* Once a multi-tenant APIM installation is connected to Cockpit, custom Access Points can be defined at both the Organization and Environment levels using Cockpit.
* When enabled, Access Point URLs will be used declaratively whenever possible.&#x20;
  * For example, when an API is created, its entrypoint will be set to virtual host mode and the host option will be limited to what the Access Points define. This allows users sharing an installation to have APIs with the same path deployed on the same set of logical Gateways.
* If you're running a completely self-hosted APIM, you may want to set up [custom Access Points](multi-tenancy.md#wip-using-custom-access-points) so you can define your own domain and certificate.

### Using custom Access Points

1. Update Access Points using either the Cockpit UI or Management API
2. To configure your own reverse proxy to point to APIM components:
   1. It must be exposed and include the customer certificate
   2. It must be configured to proxy any custom Access Points mapped to your default Access Points. For example, if the Access Point for the console has been customized, the custom Access Point must be proxied to the default console Access Point.

## Constraints of multi-tenancy mode

As of APIM 4.2, multi-tenancy is subject to the following limitations:

* Although you can connect more than one standalone APIM installation to the same Cockpit Organization, you cannot connect more than one multi-tenant APIM installation. Trying to do so will generate errors.&#x20;
* You cannot connect a multi-tenant-enabled APIM installation to Cockpit if you do not have an enterprise-enabled Cockpit account. Trying to do so will generate errors.

## Example: A typical multi-tenant setup

By leveraging the same APIM installation, multi-tenancy mode allows you to reduce the footprint of your infrastructure, and typically its cost and complexity. However, it can be beneficial to use separate installations for production and non-production environments.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/mNhfcqTUgEOXngJNcAcdIf1o.png" alt=""><figcaption><p>Typical multi-tenant setup</p></figcaption></figure>

A typical multi-tenant setup would connect one multi-tenant APIM installation to non-production environments and a standalone APIM installation to the production environment.

## How to manage standalone mode

Multi-tenancy support in Gravitee 4.2 necessitated changes to both APIM and Cockpit. However, customer deployments may continue to function as standalone APIM installations, and the following sections describe the user requirements for each of the possible scenarios in which APIM and/or Cockpit has been upgraded to support multi-tenancy:

* [APIM <4.2 connected to Cockpit](multi-tenancy.md#apim-less-than-4.2-connected-to-cockpit)
* [APIM 4.2 without Cockpit connected](multi-tenancy.md#apim-4.2-without-cockpit-connected)
* [APIM 4.2 with Cockpit connected](multi-tenancy.md#apim-4.2-with-cockpit-connected)
* [APIM 4.2 and multiple Consoles/Portals in a connected Cockpit](multi-tenancy.md#apim-4.2-and-multiple-consoles-portals-in-a-connected-cockpit)

### APIM <4.2 connected to Cockpit

{% hint style="success" %}
No changes are required of the user.
{% endhint %}

If, following the release of multi-tenancy support, Cockpit is connected to either an APIM version below 4.2 or any version of AM, Cockpit will recognize the APIM/AM installation as type `legacy` and behave as it did prior to the introduction of the multi-tenancy capability.

### APIM 4.2 without Cockpit connected

{% hint style="success" %}
No changes are required of the user.
{% endhint %}

If an APIM installation not connected to Cockpit is upgraded to 4.2, the APIM installation is standalone and behaves as it did prior to the introduction of the multi-tenancy capability.

### APIM 4.2 with Cockpit connected

{% hint style="warning" %}
The user must edit the Management API's `gravitee.yaml`.
{% endhint %}

If an APIM installation connected to Cockpit is upgraded to 4.2, the user must make the following changes to the Management API's `gravitee.yaml` file for the installation to function as `standalone`:

```yaml
installation:
  type: standalone # Could be either standalone, multi-tenant; Default is standalone.
  # Specify the URL of Management API of this instance, mandatory if you want to connect it to Cockpit
  api:
    proxyPath:
      management: ${http.api.management.entrypoint} # By default /management
      portal: ${http.api.portal.entrypoint}  # By default /portal
  standalone:
    api:
    # Specify the URLs of Management API, mandatory if you want to connect it to Cockpit with a standalone installation
      url: http://localhost:8083
    # Specify the URL of Console UI of this instance, mandatory if you want to connect it to Cockpit with a standalone installation
    console:
      url: http://localhost:3000
    portal:
      url: http://localhost:4100
```

### APIM 4.2 and multiple Consoles/Portals in a connected Cockpit

{% hint style="warning" %}
The user must edit the Management API's `gravitee.yaml`.
{% endhint %}

If an APIM installation with multiple Consoles and/or Portals set up in a connected Cockpit is upgraded to 4.2, the user must make the following changes to the Management API's `gravitee.yaml` file for the installation to function as `standalone`:

```yaml
installation:
  type: standalone # Could be either standalone, multi-tenant; Default is standalone.
  # Specify the URL of Management API of this instance, mandatory if you want to connect it to Cockpit
  api:
    proxyPath:
      management: ${http.api.management.entrypoint} # By default /management
      portal: ${http.api.portal.entrypoint}  # By default /portal
  standalone:
    api:
    # Specify the URLs of Management API, mandatory if you want to connect it to Cockpit with a standalone installation
      url: http://localhost:8083
    # Specify the URL of Console UI of this instance, mandatory if you want to connect it to Cockpit with a standalone installation
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
