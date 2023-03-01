---
title: APIM plugins
tags:
  - APIM
  - Components
---

# Plugins

## Overview

Plugins are additional components that can be *plugged into* [APIM Gateway](components.md#apim-gateway) or [APIM API](components.md#apim-api). They can customize the component’s behavior to exactly fit your needs and technical constraints.

For more information about plugins, including how to deploy them and details of their directory structure, see the [Plugins Developer Guide](../dev-guide/dev-guide-plugins.md).

## Types of Plugins

The table below lists the different types of plugins you can use with
APIM, with the component(s) they can be plugged into and some examples.
For more details of what each plugin type does, see the sections below.

<table>
<colgroup>
<col style="width: 22%" />
<col style="width: 22%" />
<col style="width: 55%" />
</colgroup>
<thead>
<tr class="header">
<th style="text-align: left;">Type</th>
<th style="text-align: left;">Component</th>
<th style="text-align: left;">Examples</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><p><a
href="#gravitee-plugins-idp">Identity Providers</a></p></td>
<td style="text-align: left;"><p>APIM API</p></td>
<td style="text-align: left;"><p>LDAP, Oauth2, InMemory</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p>Fetchers</p></td>
<td style="text-align: left;"><p>APIM API</p></td>
<td style="text-align: left;"><p>HTTP, GIT</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><a
href="#gravitee-plugins-policies">Policies</a></p></td>
<td style="text-align: left;"><p>APIM API<br />
APIM Gateway</p></td>
<td style="text-align: left;"><p>API Key, Rate-limiting, Cache</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><a
href="#gravitee-plugins-reporters">Reporters</a></p></td>
<td style="text-align: left;"><p>APIM Gateway</p></td>
<td style="text-align: left;"><p>Elasticsearch, Accesslog</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><a
href="#gravitee-plugins-repositories">Repositories</a></p></td>
<td style="text-align: left;"><p>APIM API<br />
APIM Gateway</p></td>
<td style="text-align: left;"><p>MongoDB, Redis, Elasticsearch</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><a
href="#gravitee-plugins-resources">Resources</a></p></td>
<td style="text-align: left;"><p>APIM API<br />
APIM Gateway</p></td>
<td style="text-align: left;"><p>Oauth2, Cache, LDAP</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p>Services</p></td>
<td style="text-align: left;"><p>APIM API<br />
APIM Gateway</p></td>
<td style="text-align: left;"><p>Sync, local-registry, health-check,
monitor</p></td>
</tr>
<tr class="even">
<td style="text-align: left;"><p><a
href="#gravitee-plugins-notifiers">Notifiers</a></p></td>
<td style="text-align: left;"><p>Alert Engine</p></td>
<td style="text-align: left;"><p>Email</p></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><p><a
href="#gravitee-plugins-alerts">Alerts</a></p></td>
<td style="text-align: left;"><p>APIM API<br />
APIM Gateway</p></td>
<td style="text-align: left;"><p>Vertx</p></td>
</tr>
</tbody>
</table>

### Identity Providers

An **identity provider** brokers trust with external user providers, to
authenticate and obtain information about your end users.

Out-of-the-box identity providers are:

-   MongoDB

-   In-memory

-   LDAP / Active Directory

-   OpenID Connect IdP (Azure AD, Google)

### Policies

A **policy** modifies the behavior of the request or response handled by
APIM Gateway. It can be chained by a request policy chain or a response
policy chain using a logical order. Policies can be considered like a
*proxy controller*, guaranteeing that a given business rule is fulfilled
during request/response processing.

Examples of a policy are:

-   Authorization using an API key (see the [api-key policy documentation](../policy-reference/policy-apikey.md))

-   Applying header or query parameter transformations

-   Applying rate limiting or quotas to avoid API flooding

Want to know how to create, use, and deploy a custom policy? Check out the [Policies Developer Guide](../dev-guide/dev-guide-policies.md).

### Reporters

A **reporter** is used by an APIM Gateway instance to report many types
of event:

-   Request/response metrics — for example, response-time,
    content-length, api-key

-   Monitoring metrics — for example, CPU, Heap usage

-   Health-check metrics — for example, status, response code

*Out-of-the-box* reporters are :

-   Elasticsearch Reporter

-   File Reporter

As with all plugins, you can create, use and deploy custom reporters as described in the [Plugins Developer Guide](../dev-guide/dev-guide-plugins.md).

### Repositories

A **repository** is a pluggable storage component for API configuration, policy configuration, analytics and so on. You can find more information in the [Repositories](../installation-guide/configuration/repositories/installation-guide-repositories.md) section of the Installation Guide.

### Resources

A **resource** can be added to an API for its whole lifecycle. APIM
comes with three default resources:

-   Cache

-   OAuth2 - Gravitee Access Management

-   OAuth2 - Generic Authorization Server

You can find more information in the [Resources](../user-guide/publisher/resources/resources-overview.md) section of the API Publisher Guide.

### Notifiers

A **notifier** is used to send notifications. Currently, the only
notifier available is the **email notifier**, but others including
**slack** and **portal** are planned soon.

### Alerts

An **alert** is used to send triggers or events to the Alert Engine
which can be processed to send a notification using the configured
plugin notifier. Configuring the notifier is the responsibility of the
trigger.
