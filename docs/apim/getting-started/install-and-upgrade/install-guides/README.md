---
description: Get up and running with Gravitee API Management
---

# Install & Upgrade Guides

{% hint style="warning" %}
**Changes to Gravitee distribution bundle**

Version 3.18.0 of the Gravitee Platform (released on 7th July 2022) has introduced a unified, single distribution bundle for all features available in the Community Edition (CE) and the [Enterprise Edition (EE)](https://docs.gravitee.io/ee/ee\_overview.html) of Gravitee.io APIM. Previously, the two editions used to be distributed as separate bundles per product (APIM and AM).

This change allows for a smooth transition from CE to EE functionality, and enables you to trial EE features without the need for a migration or a standalone EE installation.

If you are a Gravitee CE user and you want to try out EE features, just install the unified bundle, [request an EE license](https://docs.gravitee.io/ee/ee\_license.html), [apply it](https://docs.gravitee.io/ee/ee\_license.html) to the installation, and restart. You no longer need to download a new EE version of APIM!

In addition, you can now [register for a free time-limited Cockpit trial directly on the web](https://cockpit.gravitee.io/register), enabling you to also access a full, time-limited, EE-grade API Management trial (with Alert Engine included), manage Gravitee environments and installations, and design APIs with the Gravitee API Designer also included in the trial.

For more information about Enterprise Edition licenses, installation, and versioning, see the [Enterprise Edition section](https://docs.gravitee.io/ee/ee\_overview.html).
{% endhint %}

As described in the Introduction to Gravitee API Management (APIM), APIM is split into four main components:

* APIM gateway
* APIM management API
* APIM management UI
* APIM developer portal

The links below provide information on how you can install and configure your APIM environment. You can get started with APIM in a variety of ways, including:

<table data-card-size="large" data-view="cards"><thead><tr><th></th><th></th><th></th></tr></thead><tbody><tr><td></td><td><strong>Enterprise Trial</strong></td><td></td></tr><tr><td></td><td><strong>Install on Docker</strong></td><td></td></tr><tr><td></td><td><strong>Install on Kubernetes</strong></td><td></td></tr><tr><td></td><td><strong>Install on Amazon</strong></td><td></td></tr><tr><td></td><td><strong>Install on Red Hat and CentOS</strong></td><td></td></tr><tr><td></td><td><strong>Install with <code>.ZIP</code></strong></td><td></td></tr><tr><td></td><td><strong>Hybrid Deployment</strong></td><td></td></tr><tr><td></td><td><strong>Upgrade Guide</strong></td><td></td></tr></tbody></table>

* [Install on Amazon](https://docs.gravitee.io/apim/3.x/apim\_installation\_guide\_amazon\_introduction.html)
* [Install on Docker](https://docs.gravitee.io/apim/3.x/apim\_installation\_guide\_docker\_introduction.html)
* [Install on Red Hat and CentOS (Linux)](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_introduction.html)
* [Install on Kubernetes](https://docs.gravitee.io/apim/3.x/apim\_installguide\_kubernetes.html)
* [Install with .ZIP](https://docs.gravitee.io/apim/3.x/apim\_installguide\_gateway\_install\_zip.html)
* [Install a Hybrid Deployment](https://docs.gravitee.io/apim/3.x/apim\_installguide\_hybrid\_deployment.html#architecture)

{% hint style="info" %}
**Gravitee dependencies**

The Gravitee installation guide provides information on how to install Gravitee components. For prerequisite documentation on third-party products such as [MongoDB](https://docs.mongodb.com/), [Elasticsearch](https://www.elastic.co/guide/index.html) or others, please visit their respective websites.
{% endhint %}
