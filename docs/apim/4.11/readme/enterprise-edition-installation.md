---
description: Overview of Enterprise Edition installation
---

# Enterprise Edition installation

## API Management (APIM) and Access Management (AM)

Gravitee distributes a single, unified bundle per product for all features available in the Community Edition (CE) and the Enterprise Edition (EE) of APIM and AM. You don't install a separate EE bundle. You enable EE features by applying a valid EE license to the existing installation.

This lets you transition from CE to EE functionality smoothly, and trial EE features in APIM and AM without a standalone EE installation.

If you're a Gravitee CE user and you want to try out EE features, install the unified bundle, request an EE license, add it to the installation, and restart.

{% hint style="info" %}
**Gravitee Cloud trial**

You can sign up for a free, time-limited, full EE-grade API Management trial with included Alert Engine, as part of the [Gravitee Cloud trial registration](https://cockpit.gravitee.io/register). The Gravitee Cloud trial also lets you try Gravitee API Designer.
{% endhint %}

## Alert Engine (AE)

AE isn't part of the Community Edition. It's an exclusive Enterprise feature and requires an EE license. It's [distributed separately](https://www.gravitee.io/downloads) and can be installed using Docker, Kubernetes, or manually using a Zip file.

## Installation steps for APIM, AM, AE, and other EE modules

### Install as a new instance

To perform a new EE installation:

1. Download the full bundles of the desired products (APIM, AM, AE) from [the Gravitee platform downloads page](https://www.gravitee.io/downloads).
2. Install the relevant product bundles by following the [APIM](https://documentation.gravitee.io/apim/getting-started) and [AM](https://documentation.gravitee.io/am/getting-started/install-and-upgrade-guides) installation guides.
3. Download and install the desired EE modules.
   1. To install AE, consult the Alert Engine section on the [Gravitee downloads page](https://www.gravitee.io/downloads) and follow the [AE](https://documentation.gravitee.io/ae/getting-started/install-and-upgrade-guides) installation guide.
   2. EE plugins are installed from their respective repositories in GitHub. Gravitee's EE plugin repositories are private and their names are prefixed as `gravitee-io/gravitee-policy-<plugin-name>`. For example, the Data Logging Masking policy repository is at `https://github.com/gravitee-io/gravitee-policy-data-logging-masking`. To request access to private EE plugin repositories, email [contact@graviteesource.com](mailto:contact@graviteesource.com) if you haven't been granted access already as part of your EE license request process.
4. Request an EE license by emailing [contact@graviteesource.com](mailto:contact@graviteesource.com).
5. [Apply the EE license](enterprise-edition-licensing.md#apply-an-ee-license) to the relevant existing product instances.
6. Restart.

### Migrate from an existing CE installation

{% hint style="warning" %}
Before you proceed, make sure that you're running a [long-term support (LTS) version](../release-information/release-types.md) of the respective products.
{% endhint %}

To migrate from an existing Community Edition (CE) installation to EE:

1. Download and install the desired EE modules.
2. Request an EE license by emailing [contact@graviteesource.com](mailto:contact@graviteesource.com).
3. [Apply the EE license](enterprise-edition-licensing.md#apply-an-ee-license) to the relevant existing product instances.
4. Restart.

## Gravitee Cloud

[Gravitee Cloud](https://www.gravitee.io/platform/cockpit) is a centralized, multi-environment tool for managing all your Gravitee API Management and Access Management installations in a single place.

Gravitee Cloud is a SaaS product, so you don't need to install it as a self-hosted solution. You can [register](https://cockpit.gravitee.io/register) and use Gravitee Cloud for free as part of the Community Edition, which also gives you access to a full, time-limited, EE-grade API Management trial (with Alert Engine included), lets you manage Gravitee environments and installations, and lets you design APIs with the Gravitee API Designer included in the trial.

When used for free, Gravitee Cloud has a limit of up to two environments per user. You can [upgrade](https://www.gravitee.io/contact-us) to a [paid Enterprise Edition plan](https://www.gravitee.io/pricing) to unlock more environments and use Gravitee Cloud as an Enterprise-grade tool for production.

## API Designer

Gravitee [API Designer](https://www.gravitee.io/platform/api-designer) is free to use with the Community Edition, with a limit of one active design at any given time. [Contact Gravitee](https://www.gravitee.io/contact-us) to remove this limit by upgrading to a [paid Enterprise Edition plan](https://www.gravitee.io/pricing).

To try Gravitee API Designer, sign up for a [Gravitee Cloud trial](https://cockpit.gravitee.io/register). API Designer is part of the trial.
