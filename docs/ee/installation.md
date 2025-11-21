---
title: EE Installation
tags:
  - Enterprise Edition
  - EE
  - Installation
---

# EE Installation

## API Management (APIM) and Access Management (AM)

Version 3.18.x of the Gravitee Platform (APIM and AM 3.18.0 were released at the beginning of July 2022) has introduced a unified, single distribution bundles for all features available in the Community Edition (CE) and the Enterprise Edition (EE) of Gravitee for the APIM and AM products respectively.

Previously, the two editions used to be distributed as separate bundles (CE and EE) per product, and any migration to EE required full re-installation. This change allows for a smooth transition from CE to EE functionality, and enables you to trial EE features in APIM and AM without the need for a standalone EE installation when migrating from CE.

If you are a Gravitee CE user and you want to try out EE features, just install the unified bundle, request an EE license, add it to the installation, and restart. You no longer need to download and install a new, standalone EE version of APIM or AM!

NOTE: You can now sign up for a free, time-limited, full EE-grade API Management trial with included Alert Engine, as part of the [free Gravitee Cockpit trial registration](https://cockpit.gravitee.io/register). The Gravitee Cockpit trial also allows you to try Gravitee API Designer.

## Alert Engine (AE)

AE is not part of the Community Edition - it is an Enterprise feature and requires an EE license. It is [distributed separately](https://www.gravitee.io/downloads) and can be installed via Docker, Kubernetes, or manually using a Zip File.

## Installation steps for APIM, AM, AE, and other EE modules

=== "Installing as a new instance"

    To perform a new EE installation:

    1. Download the full bundles of the desired products (APIM, AM, AE) from [the Gravitee platform downloads page](https://www.gravitee.io/downloads).
    2. Install the relevant product bundles by following the respective installation guides.
    3. Download/install the [desired EE modules](/ee/ee_overview.html#ee_components).
    3.1. To install AE, consult the Alert Engine section on the [Gravitee downloads web page](https://www.gravitee.io/downloads) and/or follow the installation guide.
    3.2. EE plugins are installed from their respective repositories in GitHub. Gravitee's EE plugin repositories are private and their names are prefixed as `gravitee-io/gravitee-policy-<plugin-name>`. For example, the Data Logging Masking Policy repository is at `https://github.com/gravitee-io/gravitee-policy-data-logging-masking`. To request access to private EE plugin repositories, email [contact@graviteesource.com](contact@graviteesource.com) in case you have not been granted such access already as part of your EE license request process.
    4. [Request](/ee/ee_licensing.html#ask-license) an EE license.
    5. [Apply the EE license](/ee/ee_licensing.html#apply_the_license) to the relevant existing product instances.
    6. Restart.

    !!! info "Docker installation option for EE removed"
        We have removed the option to install EE bundles and EE licenses using Docker as we have simplified the installation process for EE through the use of unified platform distribution bundles for each product, as described below. The process for EE license requests, installation, and support is described in [the EE Licensing section](/ee/ee_licensing.html).

=== "Migrating from an existing CE installation"

    !!! info "Ensure you are running a LTS version"
    Before you proceed, please ensure that you are running a [long-term support (LTS) version](/ee/ee_versioning.html) of the respective product(s).

    To migrate from an existing Community Edition (CE) installation to EE:

    1. Download/install the [desired EE modules](/ee/ee_overview.html#ee_components).
    2. [Request](/ee/ee_licensing.html#ask-license) an EE license.
    3. [Apply the EE license](/ee/ee_licensing.html#apply_the_license) to the relevant existing product instances.
    4. Restart.

## Cockpit

Gravitee [Cockpit](https://www.gravitee.io/platform/cockpit) is a centralized, multi-environment tool for managing all your Gravitee API Management and Access Management installations in a single place.

After version 3.15.0, Gravitee Cockpit became a SaaS product, meaning that you do not need to install it as a self-hosted solution anymore. You can [register](https://cockpit.gravitee.io/register) and use Gravitee Cockpit for free as part of the Community Edition, enabling you to also access a full, time-limited, EE-grade API Management trial (with Alert Engine included), manage Gravitee environments and installations, and design APIs with the Gravitee API Designer also included in the trial.

When used for free, Gravitee Cockpit has a limitation of up to two environments per user. However, you can [upgrade](https://www.gravitee.io/contact-us) to a [paid Enterprise Edition plan](https://www.gravitee.io/pricing) to unlock more environments and use Gravitee Cockpit as an Enterprise-grade tool for production.

!!! info "Older, self-hosted Gravitee Cockpit versions"
    While this is not recommended, you can still install an older version of Gravitee Cockpit (3.15.0 and below) as a self-hosted instance - see the legacy Gravitee Cockpit installation guide for details.

## API Designer

Gravitee [API Designer](https://www.gravitee.io/platform/api-designer) is free to use with the Community Edition, with a limitation of one active design at any given time. [Contact us](https://www.gravitee.io/contact-us) if you need to remove this limitation by upgrading to a [paid Enterprise Edition plan](https://www.gravitee.io/pricing).

To try Gravitee API Designer, sign up for a Gravitee Cockpit trial [here](https://cockpit.gravitee.io/register) - API Designer is part of the trial.
