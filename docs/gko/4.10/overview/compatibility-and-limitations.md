# Compatibility and Limitations

## Overview

In its early iterations, the Gravitee Kubernetes Operator (GKO) focused on managing the most important aspect of any API management platform: the APIs themselves. Over time, GKO has evolved to manage API documentation pages, API access controls, API resources such as authentication servers and caches, and more. In the future, GKO will continue to expand its reach to cover new parts of the API lifecycle.

## Versioning & compatibility with APIM

Since the release of GKO 4.4, GKO follows the same release cycle and versioning scheme as APIM. This synchronization simplifies management and ensures consistency between the two systems.

### Backward compatibility

We maintain backward compatibility between APIM and GKO for up to three minor versions. This means you can safely upgrade your APIM instance while using an older GKO version, provided it is within this three-version window. For example, upgrading APIM 4.8.0 to 4.9.0 is supported if your GKO instance is running on 4.7.0 or higher.

### Forward compatibility

Forward compatibility is not supported. You cannot upgrade your GKO instance while using an older APIM version. For example, upgrading GKO from 4.8.0 to 4.9.0 with APIM 4.8.0 will result in unexpected behaviors. Always ensure your APIM minor version is equal to or newer than your GKO version.

## Deprecation policy

Gravitee is committed to providing a transparent and predictable process for feature deprecation. Our goal is to give you ample time to transition and adopt new functionality without disruption.

### Our policy

* **Timeline**: A feature marked as deprecated is available and maintained for a minimum of 12 months from the date of the deprecation announcement. This gives you a full year to adjust your systems and workflows.
* **Communication**: Deprecation announcements are made in our official product release notes and updated in the documentation. When applicable, we also provide information on recommended alternatives.
* **Removal**: Following the 12-month deprecation period, the feature may be removed in a future minor or major release.
* **Maintenance**: During the deprecation period, the feature continues to receive critical security and stability fixes. No new enhancements or functionality are added.

## Known limitations and future direction

Below are examples of resources that are not managed by GKO.&#x20;

{% hint style="info" %}
GKO management is planned for several of the following examples. Please contact us to discuss expanding GKO's scope in one of these areas.
{% endhint %}

**API-level** elements that are not managed by GKO:

* Picture & background
* Alerts
* Documentation page translations
* Documentation page attached resources, also known as API Media
* Documentation pages of type LINK
* v4 API primary owner management

GKO does not manage any **environment-level** objects, such as:

* APIM dictionaries (coming soon)
* Platform-level common policies
* Developer Portal themes

GKO does not manage other **Gravitee components**, such as:

* Gravitee Access Management
* Gravitee Alert Engine
