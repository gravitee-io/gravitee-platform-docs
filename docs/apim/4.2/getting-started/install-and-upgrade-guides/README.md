---
description: Get up and running with Gravitee API Management
---

# Install & Upgrade Guides

{% hint style="warning" %}
**Changes to Gravitee distribution bundle**

Version 3.18.0 of the Gravitee Platform (released on 7th July 2022) has introduced a unified, single distribution bundle for all features available in the Community Edition (CE) and the Enterprise Edition (EE) of Gravitee APIM. Previously, the two editions used to be distributed as separate bundles per product (APIM and AM).

This change allows for a smooth transition from CE to EE functionality, and enables you to trial EE features without the need for a migration or a standalone EE installation.

If you are a Gravitee CE user and you want to try out EE features, just install the unified bundle, request an EE license, apply it to the installation, and restart. You no longer need to download a new EE version of APIM!

In addition, you can now [register for a free time-limited Gravitee Cockpit trial directly on the web](https://cockpit.gravitee.io/register), enabling you to also access a full, time-limited, EE-grade API Management trial (with Alert Engine included), manage Gravitee environments and installations, and design APIs with the Gravitee API Designer also included in the trial.

For more information about Enterprise Edition licenses, installation, and versioning, see the Enterprise Edition section.
{% endhint %}

As described in the [Introduction to Gravitee API Management (APIM)](../../README.md), APIM is split into four main components:

* APIM Gateway
* APIM Management API
* APIM Management Console
* APIM Developer Portal

The links below provide detailed guides on how you can setup, configure, and upgrade your APIM environment. You can get started with APIM in a variety of ways, including:

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td><strong>Enterprise Trial</strong></td><td></td><td><a href="free-trial.md">free-trial.md</a></td></tr><tr><td></td><td><strong>Install on Docker</strong></td><td></td><td><a href="install-on-docker/">install-on-docker</a></td></tr><tr><td></td><td><strong>Install on Kubernetes</strong></td><td></td><td><a href="install-on-kubernetes/">install-on-kubernetes</a></td></tr><tr><td></td><td><strong>Install on Amazon</strong></td><td></td><td><a href="install-on-amazon/">install-on-amazon</a></td></tr><tr><td></td><td><strong>Install on Red Hat and CentOS</strong></td><td></td><td><a href="install-on-red-hat-and-centos/">install-on-red-hat-and-centos</a></td></tr><tr><td></td><td><strong>Install with <code>.ZIP</code></strong></td><td></td><td><a href="install-with-.zip.md">install-with-.zip.md</a></td></tr><tr><td></td><td><strong>Hybrid Deployment</strong></td><td></td><td><a href="../hybrid-deployment/">hybrid-deployment</a></td></tr><tr><td></td><td><strong>Upgrade Guide</strong></td><td></td><td><a href="4.2-upgrade-guide.md">4.2-upgrade-guide.md</a></td></tr></tbody></table>

{% hint style="info" %}
**Gravitee dependencies**

Gravitee's installation & upgrade guides provide information on how to install Gravitee components. For prerequisite documentation on third-party products such as [MongoDB](https://docs.mongodb.com/) or [Elasticsearch](https://www.elastic.co/guide/index.html), please visit their respective websites.
{% endhint %}
