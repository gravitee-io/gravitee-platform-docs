---
description: >-
  This page discusses how to deploy APIM and Cockpit together in multi-tenant
  mode
---

# Multi-tenancy

## Overview

{% hint style="warning" %}
Multi-tenancy requires running APIM 4.2 and an [enterprise-enabled Gravitee Cockpit account](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee#enterprise-version-of-gravitee-cockpit).

To learn more about Gravitee Enterprise and what's included in various enterprise packages, [book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/) or [check out the pricing page](https://www.gravitee.io/pricing).
{% endhint %}

Gravitee uses the term multi-tenancy to describe a configuration in which:

* A single APIM installation supports multiple Organizations and Environments created through Cockpit. Each tenant can be either an Organization or an Environment.
* Features and data are isolated between tenants.
* Dedicated URLs, or Access Points, are used to access APIM components and APIs deployed on Gravitee Gateways. APIs may only be published on these defined entrypoints.

{% hint style="info" %}
The way in which data and features are isolated between the logical hierarchical structures of APIM enables the existence of a multi-tenant Developer Portal.
{% endhint %}

APIM 4.2 implements changes to how Organizations and Environments are managed, in addition to the configuration that is propagated from Gravitee Cockpit. The following sections cover:

* How to configure a `multi-tenant` installation with Gravitee 4.2, including Access Points.
* For information on how to run a `standalone` (not multi-tenant) installation with APIM 4.2 and newer, refer to the [4.2 Upgrade Guide](4.2-upgrade-guide.md#updating-cockpit-connection).

## How to set up multi-tenancy

{% hint style="info" %}
The following instructions are guidelines that apply to both Gravitee Cloud and self-hosted customers who want to run a multi-tenant APIM installation.
{% endhint %}

Multi-tenancy is an enterprise feature. In order to use it, you need to:

* Enable APIM's multi-tenancy mode
* Connect the APIM installation to an enterprise-enabled Gravitee Cockpit account

Follow the steps below to implement best practices for APIM multi-tenancy.

{% hint style="warning" %}
Once a multi-tenant APIM is connected to Cockpit, it is not possible to disable multi-tenancy mode in APIM. We recommend first trying multi-tenancy in a Sandbox or similar installation.
{% endhint %}

1. [Install APIM](./) on your preferred infrastructure and deployment type
2. Explicitly set APIM to multi-tenant mode by commenting out the multi-tenant section in the configuration. Optionally, you can specify the configuration of Access Points, which comprises the URLs that APIM components will be addressed on.

{% hint style="info" %}
Cockpit is able to interpret a variabilized Access Point structure based on Account, Organization, and Environment Human Readable IDs. Cockpit will interpret non-variabilized instructions literally, which may result in multiple Environment components receiving the same Access Point configuration.
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
4.  Link your APIM installation to the Environment you created by following [these instructions](https://documentation.gravitee.io/gravitee-cloud/guides/register-installations). Your APIM installation will be identified as `MULTI-TENANT`, recognized by Cockpit as multi-tenant, and send templated Access Points to the connected Environment.

    <figure><img src="../../.gitbook/assets/image%20(58).png" alt=""><figcaption><p>Installation details in Cockpit showing the installation as multi-tenant</p></figcaption></figure>
5. Add a new Environment within the same Organization and connect it to the multi-tenant APIM installation

{% hint style="success" %}
Congratulations, you can now enjoy the benefits of multi-tenancy!
{% endhint %}

## Access Points

The Access Points feature allows different tenants to use dedicated URLs to access resources. The following tips and caveats apply to the configuration and use of Access Points:

* As Access Points rely on proper mapping, e.g., through a load balancer, you may need to edit your `etc/hosts` file prior to testing locally.
* When enabled, Access Point URLs will be used declaratively whenever possible.
  * For example, when an API is created, its entrypoint will be set to virtual host mode and the host option will be limited to what the Access Points define. This allows users sharing an installation to have APIs with the same path deployed on the same set of logical Gateways.
* Once a multi-tenant APIM installation is connected to Cockpit, custom Access Points can be defined at both the Organization and Environment levels using Cockpit. These values will override the values originally sent from the APIM installation, as shown below.

<figure><img src="../../.gitbook/assets/image (57).png" alt=""><figcaption><p>Access Points configuration for Organization-related APIM nodes, found in Organization settings in Cockpit</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (55).png" alt=""><figcaption><p>Access Points configuration for Environment-related APIM nodes, found in Environment settings in Cockpit</p></figcaption></figure>

### Using custom Access Points

1. Update Access Points using either the Cockpit UI or Management API
2. To configure your own reverse proxy to point to APIM components:
   1. It must be exposed and include the customer certificate
   2. It must be configured to proxy any custom Access Points mapped to your default Access Points. For example, if the Access Point for the console has been customized, the custom Access Point must be proxied to the default console Access Point.

## Constraints of multi-tenancy mode

As of APIM 4.2, multi-tenancy is subject to the following limitations:

* Although you can connect more than one standalone APIM installation to the same Cockpit Organization, you cannot connect more than one multi-tenant APIM installation. Trying to do so will generate errors.
* You cannot connect a multi-tenant-enabled APIM installation to Cockpit if you do not have an enterprise-enabled Cockpit account. Trying to do so will generate errors.

{% hint style="info" %}
If you are an existing Gravitee Enterprise customer and encounter issues setting up multi-tenancy mode, reach out to your Customer Success Manager to make sure your Cockpit Account has all enterprise features enabled.
{% endhint %}

## Example: A typical multi-tenant setup

By leveraging the same APIM installation, multi-tenancy mode allows you to reduce the footprint of your infrastructure, and typically its cost and complexity. However, it can be beneficial to use separate installations for production and non-production environments.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/mNhfcqTUgEOXngJNcAcdIf1o.png" alt=""><figcaption><p>Typical multi-tenant setup</p></figcaption></figure>

A typical multi-tenant setup would connect one multi-tenant APIM installation to non-production environments and a standalone APIM installation to the production environment.
