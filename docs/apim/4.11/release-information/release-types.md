---
description: Gravitee's approach to software development and deployment
---

# Release Types

## Overview

Gravitee currently has two types of releases: [Beta](#beta) and [general availability](#general-availability). Feature identification and usage considerations for each release type are summarized below:

<table><thead><tr><th width="149.66666666666666">Release type</th><th width="238">Identification</th><th>Usage</th></tr></thead><tbody><tr><td>Beta</td><td>A beta feature is publicly available and tagged as <strong>Beta</strong> in-product </td><td>Features are available for usability testing but are not suitable for production environments</td></tr><tr><td>General availability</td><td>A feature is considered generally available if its documentation lacks a <strong>Beta</strong> tag</td><td>Features can be confidently deployed in production environments because they are stable and officially supported</td></tr></tbody></table>

A release does not need to go through beta to reach general availability.

## Beta <a href="#beta" id="beta"></a>

{% hint style="warning" %}
Deploying a beta feature or version in a production environment is strongly discouraged
{% endhint %}

The beta designation signifies that a feature or release version has achieved a high level of quality. However, beta features or versions should still not be deployed in a production environment.

A beta feature or version is made accessible to the general public for usability testing and to gather valuable feedback before it is released as production-ready and stable. This allows users to provide input and help shape the final release, ensuring a more robust and reliable product.

When utilizing a beta feature or version, please note:

* **Reporting Issues:** Customers are strongly encouraged to engage with Gravitee Support to report any issues encountered during beta testing.
  * Support requests should be submitted with normal priority.&#x20;
  * Contractual Service Level Agreements (SLAs) do not apply to beta features.
* **Support Limitations:** Support for tasks such as data recovery, rollback, or other related activities is not available when using a beta feature or version.
* **Documentation Caveats:** User documentation for beta features might be unavailable, incomplete, or not fully reflect the entire functionality of the feature.

## General availability <a href="#general-availability" id="general-availability"></a>

When a feature or release version reaches general availability, it signifies that the software has been publicly released and is fully supported according to [Gravitee's support and maintenance policy](https://documentation.gravitee.io/platform-management/support-model). Generally available features are officially documented and their interfaces are stable.

Interfaces associated with GA features adhere to a [semantic versioning model](https://semver.org/). This ensures that any changes made to the interfaces follow a consistent and predictable versioning scheme, maintaining compatibility with existing implementations.
