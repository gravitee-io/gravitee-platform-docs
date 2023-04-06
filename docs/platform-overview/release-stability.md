---
description: PLACEHOLDER COPY FROM ANOTHER SITE - NEED ENG INPUT
---

# Release Stability

## Release types <a href="#tech-preview" id="tech-preview"></a>

Gravitee currently has three types of releases:

* Tech preview
* Beta
* General availablility

### Tech preview <a href="#tech-preview" id="tech-preview"></a>

A feature in tech preview might have limited to no documentation, no support, and is not guaranteed to be made available as GA in the future. Some products or projects may also call this stage _alpha_.

**A tech preview feature or version should not be deployed in a production environment**.

Tech preview features are experimental. Interfaces for features in tech preview could change in backward-incompatible ways. Do not count on the feature becoming a formal product, and expect it to change heavily if it does.

### Beta <a href="#beta" id="beta"></a>

A beta designation in Gravitee software means a feature or release version's functionality is high quality and can be deployed in a non-production environment.

**A beta feature or version should not be deployed in a production environment**.

Note the following when using a beta feature or version:

* Beta customers are encouraged to engage Gravitee Support to report issues encountered in beta testing. Support requests should be filed with normal priority, but contractual SLAs will not be applicable for beta features.
* Support is not available for data recovery, rollback, or other tasks when using a beta feature or version.
* User documentation might not be available, complete, or reflect entire functionality.

A beta feature or version is made available to the general public for usability testing and to gain feedback about the feature or version before releasing it as a production-ready, stable feature or version.

### General availability <a href="#general-availability" id="general-availability"></a>

General availability, or GA, means that the software is released publicly and is supported according to Gravitee's support and maintenance policy. Generally available features usually have official documentation (as needed) and interfaces are stable.

If feature documentation doesn’t have a tech preview, alpha, or beta label, then the feature is generally available.

You can deploy GA features to production environments.

Interfaces are guaranteed to follow a [semantic versioning](https://semver.org/) model for any changes.

## Support model

**From version 3.18.0 and above: 12-month support model for all minor versions**

As of version 3.18.0 (released on 7th July 2022), we have changed the model of support we provide for released versions of the Gravitee Platform.

We now provide 12 months of support for each minor version. A minor version is considered a quarterly release version with a second-digit increment in the version cadence, for example 3.18.x (but not 3.18.1 - this is a maintenance release version).

We no longer support STS and LTS versions (see the next section for more information).

#### Prior to version 3.18.0: STS & LTS support model

Prior to the release of version 3.18.0, when you subscribed to support services provided by Gravitee.io, you could choose between two support options:

1. Short-Term Support (STS).
2. Long-Term Support (LTS).

LTS applied to versions ending with 0 or 5 (for example: 1.25, 1.30, 1.35). STS applied to all non-LTS versions.

An LTS version was supported for around 1 year, whereas a STS version was supported for 3 months.

When moving to an enterprise version, this was not the case: **all** LTS versions were considered to be enterprise versions.

This model aimed to ensure that our customers would be running the most well-tested and production-ready versions.

### Supported product versions and EOL dates

The tables below provide information about the entire Gravitee platform's product versions and their release and EOL (end of life) dates, as well as the support model used for each.

| Version    | Support model | Release Date   | EOL Date       |
| ---------- | ------------- | -------------- | -------------- |
| **3.19.x** | **12 months** | **2022-10-04** | **2023-10-04** |

| Version    | Support model | Release Date   | EOL Date       |
| ---------- | ------------- | -------------- | -------------- |
| 3.0.x      | **LTS**       | 2020-05-20     | 2021-06-15     |
| 3.1.x      | STS           | 2020-07-17     | 2020-10-22     |
| 3.2.x      | STS           | 2020-09-22     | 2020-11-15     |
| 3.3.x      | STS           | 2020-10-15     | 2020-12-24     |
| 3.4.x      | STS           | 2020-11-24     | 2021-01-15     |
| 3.5.x      | **LTS**       | 2020-12-15     | 2021-12-15     |
| 3.6.x      | STS           | 2021-02-16     | 2021-04-16     |
| 3.7.x      | STS           | 2021-03-16     | 2021-05-13     |
| 3.8.x      | STS           | 2021-04-13     | 2021-06-18     |
| 3.9.x      | STS           | 2021-05-18     | 2021-07-15     |
| 3.10.x     | **LTS**       | 2021-06-15     | 2022-07-31     |
| 3.11.x     | STS           | 2021-08-31     | 2021-10-31     |
| 3.12.x     | STS           | 2021-09-30     | 2021-12-19     |
| 3.13.x     | STS           | 2021-11-19     | 2022-01-27     |
| 3.14.x     | STS           | 2022-01-12     | 2022-03-30     |
| 3.15.x     | **LTS**       | 2021-01-27     | 2023-01-31     |
| 3.16.x     | STS           | 2022-02-28     | 2022-04-30     |
| 3.17.x     | STS           | 2022-03-30     | 2022-07-31     |
| 3.18.x     | 12 months     | 2022-07-07     | 2023-07-07     |
| **3.19.x** | **12 months** | **2022-10-04** | **2023-10-04** |

\
