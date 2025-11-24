---
description: Overview of Life Policy.
noIndex: true
---

# End of Life Policy

This page describes the End of Life policy and maintenance windows for Ambassador Edge Stack.

### Supported Versions

Ambassador Edge Stack versions are expressed as **x.y.z**, where **x** is the major version, **y** is the minor version, and **z** is the patch version, following [Semantic Versioning](https://semver.org/) terminology.

**X-series (Major Versions)**

* **3.y**: 3.0

**Y-release (Minor versions)**

* For 3.y, that is **3.10.z**

In this document, **Current** refers to the latest X-series release.

Maintenance refers to the previous X-series release, including critical security and Sev1 defect patches.

### Patch Releases

* What is included in a patch release?

1. We will fix security issues in Ambassador Edge Stack code
2. We will pick up security fixes from dependencies as they are made available
3. We will not maintain forks of our major dependencies
4. We will not attempt our own back ports of critical fixes to dependencies which are out of support from their own communities

### CNCF Ecosystem Considerations

* Envoy releases a major version every 3 months and supports its previous releases for 12 months. Envoy does not support any release longer than 12 months.
* Kubernetes 1.19 and newer receive 12 months of patch support (The [Kubernetes Yearly Support Period](https://github.com/kubernetes/enhancements/blob/master/keps/sig-release/1498-kubernetes-yearly-support-period/README.md)). We will follow the Kubernetes EOL policy. This policy helps us maintain the integrity of our systems and provides you with the latest features, bug fixes, and security updates.

Note that the cadence and versioning of Ambassador Edge Stack releases are independent from the cadences and versioning of Emissary-Ingress project it is based on.

## The Policy

We will offer a 9 month maintenance window for the latest Y-release of an X-series after a new X-series goes GA and becomes the current release. During the maintenance window, only critical security and Sev1 defect patches will be released for the maintenance X-series. Users desiring new features or bug fixes for lower severity defects will need to migrate to the current X-series.

The current X-series will receive as many Y-releases as necessary and as often as we have new features or patches to release.

We refer to the movement between major versions as a migration. For example, users migrate from the 2.x series to the 3.x series. Alternatively, movement between minor versions within the same major version is referred to as an upgrade. For example, users upgrade from 3.9.0 to 3.10.0.

Artifacts of releases outside of the maintenance window will be frozen and will remain available publicly for download for a minimal period of time. These artifacts include Docker images, application binaries, Helm charts, etc.

Explore the latest enhancements and updates in our software by checking out the [Release Notes](release-notes.md). Stay informed about new features, improvements, and bug fixes to make the most out of your experience with Edge Stack.
