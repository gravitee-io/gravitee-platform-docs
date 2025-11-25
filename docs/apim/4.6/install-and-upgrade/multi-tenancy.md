---
description: This page discusses how to deploy APIM and Cloud together in multi-tenant mode
---

# Multi-tenancy

{% hint style="warning" %}
Multi-tenancy requires running APIM 4.2 and an [enterprise-enabled Gravitee Cloud account](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee#enterprise-version-of-gravitee-cockpit).

To learn more about Gravitee Enterprise and what's included in various enterprise packages, [book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/) or [check out the pricing page](https://www.gravitee.io/pricing).
{% endhint %}

## Overview

Changes to the management of Gravitee Organizations and Environments and to the configuration propagated from Gravitee Cloud enable multi-tenancy. Gravitee multi-tenancy describes a configuration in which:

* A single APIM installation supports multiple Organizations and Environments created through Cloud. Each tenant can be either an Organization or an Environment.
* Features and data are isolated between tenants.
* Dedicated URLs, or Access Points, are used to access APIM components and APIs deployed on Gravitee Gateways. APIs may only be published on these defined entrypoints.

{% hint style="info" %}
The isolation scheme of data and features between the logical hierarchical structures of APIM enables a multi-tenant Developer Portal.
{% endhint %}

The following sections describe:

* [How to set up multi-tenancy](multi-tenancy.md#how-to-set-up-multi-tenancy)
* [Access points](multi-tenancy.md#access-points)
* [Constraints of multi-tenancy mode](multi-tenancy.md#constraints-of-multi-tenancy-mode)
* [A typical multi-tenant setup](multi-tenancy.md#a-typical-multi-tenant-setup)

{% hint style="info" %}
For information on how to run a `standalone` (not multi-tenant) installation with APIM, refer to the [Upgrade Guide](upgrade-guide.md)
{% endhint %}

## How to set up multi-tenancy

{% hint style="info" %}
The following instructions are guidelines that apply to both Gravitee Cloud and self-hosted customers who want to run a multi-tenant APIM installation.
{% endhint %}

Multi-tenancy is an enterprise feature. In order to use it, you need to:

* Enable APIM's multi-tenancy mode
* Connect the APIM installation to an enterprise-enabled Gravitee Cloud account

Follow the steps below to implement best practices for APIM multi-tenancy.

{% hint style="warning" %}
Once a multi-tenant APIM is connected to Cloud, it is not possible to disable multi-tenancy mode in APIM. We recommend first trying multi-tenancy in a Sandbox or similar installation.
{% endhint %}

1. Install APIM on your preferred infrastructure and deployment type
2.  Explicitly set APIM to multi-tenant mode by commenting out the multi-tenant section in the configuration. Optionally, you can specify the configuration of Access Points, which comprises the URLs that APIM components will be addressed on.

    \{% hint style="info" %\} Cloud is able to interpret a variabilized Access Point structure based on Account, Organization, and Environment Human Readable IDs. Cloud will interpret non-variabilized instructions literally, which may result in multiple Environment components receiving the same Access Point configuration. \{% endhint %\}

    ```yaml
    installation:
      type: multi-tenant
      multi-tenant:
        # Specify the Access Points of your installation, mandatory if you want to connect it to Cloud with a multi-tenant installation
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
3. Sign in to your enterprise version of Gravitee Cloud and
   * Create one Organization
   * Create one Environment
4. Link your APIM installation to the Environment you created by following [these instructions](https://documentation.gravitee.io/gravitee-cloud/guides/register-installations). Your APIM installation will be identified as `MULTI-TENANT`, recognized by Cloud as multi-tenant, and send templated Access Points to the connected Environment
5. Add a new Environment within the same Organization and connect it to the multi-tenant APIM installation

{% hint style="success" %}
Congratulations, you can now enjoy the benefits of multi-tenancy!
{% endhint %}

## Access Points

The Access Points feature allows different tenants to use dedicated URLs to access resources. The following tips and caveats apply to the configuration and use of Access Points:

* As Access Points rely on proper mapping, e.g., through a load balancer, you may need to edit your `etc/hosts` file prior to testing locally.
* When enabled, Access Point URLs will be used declaratively whenever possible.
  * For example, when you create an API, the entrypoint of the gateway will be restricted to the defined gateway environment Access Point. This allows users sharing an installation to have APIs with the same path deployed on the same set of logical Gateways.

{% hint style="info" %}
Note that prior to 4.4, APIs where forced to be in virtual host mode. This is no longer needed in 4.4 as improvements to Gateway environment Access Points have been made. Path based APIs are now supported in multi-tenant mode.\
\
All APIs that have been created prior to 4.4 will still be in virtual host mode.
{% endhint %}

* Once a multi-tenant APIM installation is connected to Cloud, custom Access Points can be defined at both the Organization and Environment levels using Cloud. These values will override the values originally sent from the APIM installation, as shown below.

<figure><img src="../.gitbook/assets/image (57).png" alt=""><figcaption><p>Access Points configuration for Organization-related APIM nodes, found in Organization settings in Cloud</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (55).png" alt=""><figcaption><p>Access Points configuration for Environment-related APIM nodes, found in Environment settings in Cloud</p></figcaption></figure>

### Using custom Access Points

1. Update Access Points using either the Cloud UI or Management API
2. To configure your own reverse proxy to point to APIM components:
   1. It must be exposed and include the customer certificate
   2. It must be configured to proxy any custom Access Points mapped to your default Access Points. For example, if the Access Point for the console has been customized, the custom Access Point must be proxied to the default console Access Point.

## Constraints of multi-tenancy mode

Multi-tenancy is subject to the following limitations:

* Although you can connect more than one standalone APIM installation to the same Cloud Organization, you cannot connect more than one multi-tenant APIM installation. Trying to do so will generate errors.
* You cannot connect a multi-tenant-enabled APIM installation to Cloud if you do not have an enterprise-enabled Cloud account. Trying to do so will generate errors.

{% hint style="info" %}
If you are an existing Gravitee Enterprise customer and encounter issues setting up multi-tenancy mode, reach out to your Customer Success Manager to make sure your Cloud Account has all enterprise features enabled.
{% endhint %}

## A typical multi-tenant setup

By leveraging the same APIM installation, multi-tenancy mode allows you to reduce the footprint of your infrastructure, and typically its cost and complexity. However, it can be beneficial to use separate installations for production and non-production environments.

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/mNhfcqTUgEOXngJNcAcdIf1o.png" alt=""><figcaption><p>Typical multi-tenant setup</p></figcaption></figure>

A typical multi-tenant setup would connect one multi-tenant APIM installation to non-production environments and a standalone APIM installation to the production environment.
