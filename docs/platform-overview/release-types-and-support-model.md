---
description: Gravitee's approach to software development, deployment, and support
---

# Release Types and Support Model

## Release types <a href="#tech-preview" id="tech-preview"></a>

Gravitee currently has three types of releases:

* Tech preview
* Beta
* General availability

{% hint style="info" %}
&#x20;A release does not need to go through a tech preview or beta to reach general availability.
{% endhint %}

### Tech preview <a href="#tech-preview" id="tech-preview"></a>

Tech Preview refers to a stage in which a particular feature is made available for testing and evaluation purposes to members of Gravitee's Early Access program.&#x20;

{% hint style="info" %}
**Join Gravitee's Early Access program**

If you'd like to get access to Gravitee's cutting-edge features and help shape the future of the product, you can apply to join Gravitee's Early Access program by [contacting us](https://www.gravitee.io/contact-us) or reaching out to your CSM.
{% endhint %}

It is important to note that tech preview features may have limited or no documentation, lack official support, and are not guaranteed to be included as part of the general availability (GA) release in the future. Tech previews are often referred to as "alpha" releases in other software products.

Tech preview features are experimental by nature, and as such, the interfaces associated with these features may undergo significant changes that are not compatible with previous versions. It is important not to rely on a tech preview feature becoming a fully developed product. If it does progress to that stage, anticipate substantial modifications to its functionality and behavior.

#### **Usage considerations**

It is crucial to understand that deploying a tech preview feature or version in a production environment is strongly discouraged. **These features are intended for experimental use only and are not suitable for production-level implementation.**

#### **Identifying tech preview features**

Tech preview features will only be available to members of the Early Access program and will be designated in-product with a **Tech Preview** tag.

### Beta <a href="#beta" id="beta"></a>

The beta designation signifies that a feature or release version has achieved a high level of quality. However, it is important to note that beta features or versions should still not be deployed in a production environment.

A beta feature or version is made accessible to the general public for the purposes of usability testing and to gather valuable feedback before it is released as a production-ready and stable feature or version. This allows users to provide input and help shape the final release, ensuring a more robust and reliable product.

#### **Usage considerations**

**Beta releases are not suitable for production-level implementation**. When utilizing a beta feature or version, please take note of the following:

1. **Reporting Issues:** Beta customers are strongly encouraged to engage with Gravitee Support for reporting any issues encountered during beta testing. Support requests should be submitted with normal priority; however, contractual Service Level Agreements (SLAs) will not apply to beta features.
2. **Support Limitations:** Support for tasks such as data recovery, rollback, or other related activities is not available when using a beta feature or version.
3. **Documentation Caveats:** Please be aware that user documentation for beta features might be unavailable, incomplete, or may not fully reflect the entire functionality of the feature.

#### **Identifying beta features**

Beta features will be publicly available and will be designated in product with a **Beta** tag.

### General availability <a href="#general-availability" id="general-availability"></a>

When a software feature or release version reaches general availability (GA), it signifies that the software has been publicly released and is fully supported according to [Gravitee's support and maintenance policy](release-types-and-support-model.md#support-model). Generally available features come with official documentation, as needed, and their interfaces are stable.

It is important to note that interfaces associated with GA features adhere to a [semantic versioning model](https://semver.org/). This ensures that any changes made to the interfaces follow a consistent and predictable versioning scheme, maintaining compatibility with existing implementations.

#### **Usage considerations**

GA features can be confidently deployed in production environments, given their stability and official support.

#### **Identifying GA features**

If a feature documentation lacks the labels "tech preview," "alpha," or "beta," it is considered generally available.

## Support model

**From version 3.18.0 and above: 12-month support model for all minor versions**

As of version 3.18.0 (released on 7th July 2022), we have changed the model of support we provide for released versions of the Gravitee Platform.

We now provide 12 months of support for each minor version. A minor version is considered a quarterly release version with a second-digit increment in the version cadence, for example 3.18 (but not 3.18.1 - this is a maintenance release version). Maintenance release versions will be supported for as long as their "parent" minor version is. So, for example, 3.18.1 would be supported until the deprecation of 3.18 support.

### Supported product versions and EOL dates

The tables below provide information about the entire Gravitee platform's product versions and their release and EOL (end of life) dates, as well as the support model used for each.

| Version | Support model | Release Date | EOL Date   |
| ------- | ------------- | ------------ | ---------- |
| 3.19    | 12 months     | 2022-10-04   | 2023-10-04 |
| 3.20    | 12 months     | 2023-01-12   | 2024-01-12 |
| 4.0     | 12 months     | 2023-7-20    | 2024-7-20  |

\
