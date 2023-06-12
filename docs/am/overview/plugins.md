# Plugins

## Overview

Plugins are additional components that can be _plugged into_ AM Gateway or AM API. They can customize the component’s behavior to exactly fit your needs and technical constraints.

## Types of plugins

The table below lists the different types of plugins you can use with APIM, with the component(s) they can be plugged into and some examples. For more details of what each plugin type does, see the sections below.

| Type                                                                                                         | Components               | Examples                   |
| ------------------------------------------------------------------------------------------------------------ | ------------------------ | -------------------------- |
| [Identity Providers](https://docs.gravitee.io/am/current/am\_overview\_plugins.html#gravitee-plugins-idp)    | Management API/ Gateway  | LDAP, Database, Social, …​ |
| [Policies](https://docs.gravitee.io/am/current/am\_overview\_plugins.html#gravitee-plugins-policies)         | Management API / Gateway | Callout                    |
| [Reporters](https://docs.gravitee.io/am/current/am\_overview\_plugins.html#gravitee-plugins-reporters)       | Management API / Gateway | MongoDB                    |
| [Repositories](https://docs.gravitee.io/am/current/am\_overview\_plugins.html#gravitee-plugins-repositories) | Management API / Gateway | MongoDB                    |
| [Alerts](https://docs.gravitee.io/am/current/am\_overview\_plugins.html#gravitee-plugins-alerts)             | Management API / Gateway | Vertx                      |

### Identity providers

An **identity provider** brokers trust with external user providers, to authenticate and obtain information about your end users.

Out-of-the-box identity providers are:

* MongoDB
* LDAP / Active Directory
* OpenID Connect IdP (Azure AD, Google)
* SAML 2.0 IdP

### Policies

A **policy** modifies the behavior of a request or response handled by AM Gateway. It can be chained by a request policy chain or a response policy chain using a logical order. Policies are used by extension points to guarantee a given business rule is fulfilled during request processing.

An example of a policy is:

* Call external web services during Login Flow (HTTP Callout policy)

### Reporters

A **reporter** is used by an AM API or AM Management instance to report many types of event:

* Administration metrics — administrative tasks (CRUD on resources)
* Authentication / Authorization metrics — (sign-in activity, sign-up activity)

Out-of-the-box reporters are:

* MongoDB Reporter

### Repositories

A **repository** is a storage component for AM platform configuration.

Out-of-the-box repositories are :

* MongoDB Repository

### Alerts

An **alert** allows AM to send triggers or events to the Alert Engine which can be processed to send a notification using the configured plugin notifier. Configuring the notifier is the responsibility of the trigger.

\
