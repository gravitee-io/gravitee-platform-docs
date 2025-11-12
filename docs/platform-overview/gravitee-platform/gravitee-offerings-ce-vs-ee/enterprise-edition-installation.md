# Enterprise Edition Installation

## API Management (APIM) and Access Management (AM)

Version 3.18.x of the Gravitee Platform (APIM and AM 3.18.0 were released at the beginning of July 2022) has introduced a unified, single distribution bundles for all features available in the Community Edition (CE) and the Enterprise Edition (EE) of Gravitee for the APIM and AM products respectively.

Previously, the two editions used to be distributed as separate bundles (CE and EE) per product, and any migration to EE required full re-installation. This change allows for a smooth transition from CE to EE functionality, and enables you to trial EE features in APIM and AM without the need for a standalone EE installation when migrating from CE.

If you are a Gravitee CE user and you want to try out EE features, just install the unified bundle, request an EE license, add it to the installation, and restart. You no longer need to download and install a new, standalone EE version of APIM or AM.

{% hint style="info" %}
**Gravitee Cloud trial**

You can now sign up for a free, time-limited, full EE-grade API Management trial with included Alert Engine, as part of the [free Gravitee Cloud trial registration](https://cockpit.gravitee.io/register). The Gravitee Cloud trial also allows you to try Gravitee API Designer.
{% endhint %}

## Alert Engine (AE)

AE is not part of the Community Edition - it is an exclusive Enterprise feature and requires an EE license. It is [distributed separately](https://www.gravitee.io/downloads) and can be installed via Docker, Kubernetes, or manually using a Zip File.

## Installation steps for APIM, AM, AE, and other EE modules

### Installing as a new instance

To perform a new EE installation:

1. Download the full bundles of the desired products (APIM, AM, AE) from [the Gravitee platform downloads page](https://www.gravitee.io/downloads).
2. Install the relevant product bundles by following the relevant [APIM](/apim/getting-started/install-guides) and [AM](/am/getting-started/install-and-upgrade-guides) installation guides.
3. Download/install the desired EE modules.
   1. To install AE, consult the Alert Engine section on the [Gravitee downloads web page](https://www.gravitee.io/downloads) and/or follow [AE](https://documentation.gravitee.io/ae/getting-started/install-and-upgrade-guides) installation guide.
   2. EE plugins are installed from their respective repositories in GitHub. Gravitee’s EE plugin repositories are private and their names are prefixed as `gravitee-io/gravitee-policy-<plugin-name>`. For example, the Data Logging Masking Policy repository is at `https://github.com/gravitee-io/gravitee-policy-data-logging-masking`. To request access to private EE plugin repositories, email [contact@graviteesource.com](mailto:contact@graviteesource.com) in case you have not been granted such access already as part of your EE license request process.
4. Request an EE license by emailing [contact@graviteesource.com](mailto:contact@graviteesource.com).
5. [Apply the EE license](enterprise-edition-licensing.md#applying-an-ee-license) to the relevant existing product instances.
6. Restart.

{% hint style="info" %}
**EE Docker deprecation**

We have removed the option to install EE bundles and EE licenses using Docker as we have simplified the installation process for EE through the use of unified platform distribution bundles for each product, as described below. The process for EE license requests, installation, and support is described in the [EE Licensing section.](enterprise-edition-licensing.md)
{% endhint %}

### Migrating from an existing CE installation

{% hint style="warning" %}
Before you proceed, please ensure that you are running a [long-term support (LTS) version](docs/platform-overview/gravitee-platform/release-types-and-support-model.md) of the respective product(s).
{% endhint %}

To migrate from an existing Community Edition (CE) installation to EE:

1. Download/install the desired EE modules.
2. Request an EE license by emailing [contact@graviteesource.com](mailto:contact@graviteesource.com).
3. [Apply the EE license](enterprise-edition-licensing.md#applying-an-ee-license) to the relevant existing product instances.
4. Restart.

## Gravitee Cloud

[Gravitee Cloud](https://www.gravitee.io/platform/cockpit) is a centralized, multi-environment tool for managing all your Gravitee API Management and Access Management installations in a single place.

After version 3.15.0, Gravitee Cloud became a SaaS product, meaning that you do not need to install it as a self-hosted solution anymore. You can [register](https://cockpit.gravitee.io/register) and use Gravitee Cloud for free as part of the Community Edition, enabling you to also access a full, time-limited, EE-grade API Management trial (with Alert Engine included), manage Gravitee environments and installations, and design APIs with the Gravitee API Designer also included in the trial.

When used for free, Gravitee Cloud has a limitation of up to two environments per user. However, you can [upgrade](https://www.gravitee.io/contact-us) to a [paid Enterprise Edition plan](https://www.gravitee.io/pricing) to unlock more environments and use Gravitee Cloud as an Enterprise-grade tool for production.

## API Designer

Gravitee [API Designer](https://www.gravitee.io/platform/api-designer) is free to use with the Community Edition, with a limitation of one active design at any given time. [Contact us](https://www.gravitee.io/contact-us) if you need to remove this limitation by upgrading to a [paid Enterprise Edition plan](https://www.gravitee.io/pricing).

To try Gravitee API Designer, sign up for a Gravitee Cloud trial [here](https://cockpit.gravitee.io/register) - API Designer is part of the trial.
