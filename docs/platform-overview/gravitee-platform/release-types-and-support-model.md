---
description: Gravitee's approach to software development and deployment
---

# Release Types

## Overview <a href="#tech-preview" id="tech-preview"></a>

Gravitee currently has three types of releases: [Tech Preview](release-types-and-support-model.md#tech-preview-1), [Beta](release-types-and-support-model.md#beta), and [general availability](release-types-and-support-model.md#general-availability). Feature identification and usage considerations for each release type are summarized below:

<table><thead><tr><th width="149.66666666666666">Release type</th><th width="238">Identification</th><th>Usage</th></tr></thead><tbody><tr><td>Tech preview</td><td>A tech preview feature is available only to members of the Early Access program and tagged as <strong>Tech Preview</strong> in-product</td><td>Features are intended for experimental use only and are not suitable for production environments</td></tr><tr><td>Beta</td><td>A beta feature is publicly available and tagged as <strong>Beta</strong> in-product </td><td>Features are available for usability testing but are not suitable for production environments</td></tr><tr><td>General availability</td><td>A feature is considered generally available if its documentation lacks a <strong>Tech Preview</strong> or <strong>Beta</strong> tag</td><td>Features can be confidently deployed in production environments because they are stable and officially supported</td></tr></tbody></table>

A release does not need to go through a tech preview or beta to reach general availability.

## Tech Preview <a href="#tech-preview" id="tech-preview"></a>

{% hint style="warning" %}
Deploying a tech preview feature or version in a production environment is strongly discouraged
{% endhint %}

Tech preview refers to a stage in which a particular feature is made available to members of Gravitee's Early Access program for testing and evaluation. Tech previews are often referred to as "alpha" releases in other software products.

{% hint style="info" %}
**Join Gravitee's Early Access program**

If you'd like to get access to Gravitee's cutting-edge features and help shape the future of the product, you can apply to join Gravitee's Early Access program by [contacting us](https://www.gravitee.io/contact-us) or reaching out to your CSM.
{% endhint %}

Tech preview features may have limited or no documentation, lack official support, and are not guaranteed to be included as part of the future general availability (GA) release. Do not rely on a tech preview feature becoming a fully developed product. If it does progress to that stage, anticipate substantial modifications to its functionality and behavior.

Tech preview features are experimental by nature, meaning the interfaces associated with these features may undergo significant changes that are not compatible with previous versions.&#x20;

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

When a feature or release version reaches general availability, it signifies that the software has been publicly released and is fully supported according to [Gravitee's support and maintenance policy](support-model/README.md#support-model). Generally available features are officially documented and their interfaces are stable.

Interfaces associated with GA features adhere to a [semantic versioning model](https://semver.org/). This ensures that any changes made to the interfaces follow a consistent and predictable versioning scheme, maintaining compatibility with existing implementations.
