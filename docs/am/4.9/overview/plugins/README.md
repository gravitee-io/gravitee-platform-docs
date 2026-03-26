---
description: Overview of Plugins.
---

# Plugins

## Overview

Plugins are additional components that can enhance AM Gateway or AM Management API. They can customize the component’s behavior to exactly fit your needs and technical constraints.

## Types of plugins

The table below lists the different types of plugins you can use with AM alongside the component(s) they can be plugged into and some examples. Details of each plugin type can be found in the sections below.

| Type                                        | Components                            | Examples                   |
| ------------------------------------------- | ------------------------------------- | -------------------------- |
| [Identity Providers](README.md#identity-providers) | Management API / Gateway              | LDAP, Database, Social, …​ |
| [Policies](README.md#policies)                     | Management API / Gateway              | Callout                    |
| [Reporters](README.md#reporters)                   | Management API / Gateway              | MongoDB                    |
| [Repositories](README.md#repositories)             | Management API / Gateway              | MongoDB                    |
| [Alerts](README.md#alerts)                         | Management API / Gateway              | Vertx                      |
| [Secret Providers](README.md#secret-providers)     | <p>APIM API<br>APIM Gateway<br>AM</p> | Kubernetes, HC Vault       |

### Identity providers

An **identity provider** brokers trust with external user providers to authenticate and obtain information about your end users. Out-of-the-box identity providers are:

* MongoDB
* LDAP / Active Directory
* OpenID Connect IdP (Azure AD, Google)
* SAML 2.0 IdP

### Policies

A **policy** modifies the behavior of a request or response handled by AM Gateway. It can be chained by a request policy chain or a response policy chain using a logical order.

Extension points use policies to guarantee a given business rule is fulfilled during request processing. An example of using a policy is to call all external web services during Login Flow (HTTP Callout policy).

### Reporters

A **reporter** is used by an AM API or AM Management instance to report many types of events:

* Administrative metrics / tasks (CRUD on resources)
* Authentication / Authorization metrics  (sign-in activity, sign-up activity)

Out-of-the-box reporters are: MongoDB Reporter.

### Repositories

A **repository** is a storage component for AM platform configuration. Out-of-the-box repositories are: MongoDB Repository.

### Alerts

An **alert** allows AM to send triggers or events to the Alert Engine which can be processed to send a notification using the configured plugin notifier. Configuring the notifier is the responsibility of the trigger.

### Secret providers

A **secret provider** resolves secrets to avoid exposing plain text passwords and secrets keys in the `gravitee.yml` file. For example, users can store their MongoDB password in a secret manager like HashiCorp Vault and then resolve it when the platform starts.
