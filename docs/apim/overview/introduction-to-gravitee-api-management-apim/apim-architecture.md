---
description: >-
  This article describes Gravitee API Management Architecture. Familiarity with
  the architecture is a prerequisite to installing Gravitee API Management.
---

# APIM Architecture

## Introduction

Gravitee offers three different API Management architecture schemes:

* Gravitee API Management hybrid architecture
* Gravitee API Management self-hosted architecture
* Gravitee API Management "fully Gravitee-managed" architecture

Each architecture relies on a specific set of Gravitee components. Common and architecture-specific components are identified below:&#x20;

<table><thead><tr><th width="340">Component</th><th width="121" data-type="checkbox">Self-hosted</th><th width="115" data-type="checkbox">Hybrid</th><th data-type="checkbox">SaaS</th></tr></thead><tbody><tr><td></td><td>true</td><td>false</td><td>false</td></tr><tr><td></td><td>true</td><td>false</td><td>false</td></tr><tr><td></td><td>true</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr><tr><td></td><td>false</td><td>false</td><td>false</td></tr></tbody></table>

## Self-hosted architecture

Self-hosted refers to when the customer and/or user hosts every Gravitee API Management component. Please note that we include both Gravitee Cloud and API Designer as componetns in our diagrams, as these are optional, fully-Gravitee-managed components that you can connect to your self-hosted API Management installation if you so wish.

### Components  <a href="#components" id="components"></a>

![Self-Hosted Components](https://dobl1.github.io/gravitee-se-docs/latest/assets/gio-apim-self-hosted-components.svg)

<table><thead><tr><th width="163" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">Gravitee API Management UI<br>(for API producers)</td><td>This web UI gives easy access to some key <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-rest-api">APIM API</a> services. <a href="https://docs.gravitee.io/apim/3.x/apim_overview_concepts.html#gravitee-concepts-publisher">API Publishers</a> can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</td></tr><tr><td align="center">Dev / API Portal<br>(for API consumers)</td><td>This web UI gives easy access to some key <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-rest-api">APIM API</a> services. <a href="https://docs.gravitee.io/apim/3.x/apim_overview_concepts.html#gravitee-concepts-consumer">API Consumers</a> can use it to search for, view, try out and subscribe to a published API.<br>They can also use it to manage their <a href="https://docs.gravitee.io/apim/3.x/apim_overview_concepts.html#gravitee-concepts-application">applications</a>.</td></tr><tr><td align="center">Management API</td><td>This RESTful API exposes services to manage and configure the <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-mgmt-ui">APIM Console</a> and <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-portal-ui">APIM Portal</a> web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the <a href="https://docs.gravitee.io/apim/3.x/apim_installguide_rest_apis_documentation.html">API Reference</a> section.<br>This components might be installed twice if you need a separation between Dev Portal and Administration Console<br>For example, to make the administration console accessible only internally (LAN), as opposed to the Dev Portal accessible from the outside (DMZ), in this scenario the Management API will only expose the operations that relates respectively to the Dev Portal and Administration Console.</td></tr><tr><td align="center">API Gateways</td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="https://docs.gravitee.io/apim/3.x/apim_overview_plugins.html#gravitee-plugins-policies">policies</a> (i.e., rules) to both HTTP requests and responses according to your needs. With these policies, you can enhance request and response processing by adding transformations, security, and many other exciting features.</td></tr><tr><td align="center">Config Database</td><td>Database use to store all the API Management platform management data, such as API definitions, users, applications and plans.</td></tr><tr><td align="center">Analytics Database</td><td>Database use to store the variety of events occurring in the gateway.</td></tr><tr><td align="center">Rate Limits Database</td><td>Database use locally for rate limits synchronized counters (Rate Limit, Quota, Spike Arrest) and optionnaly as an external cache for the <a href="https://docs.gravitee.io/apim/3.x/apim_resources_cache_redis.html#redis_cache_resource">Cache policy</a>.</td></tr><tr><td align="center">[Enterprise]<br>Cockpit</td><td>Cockpit is a centralized, multi-environments / organizations tool for managing all your Gravitee API Management and Access Management installations in a single place.</td></tr><tr><td align="center">[Enterprise]<br>API Designer</td><td>Drag-and-Drop graphical (MindMap based) API designer to quickly and intuitively design your APIs (Swagger / OAS) and even deploy mocked APIs for quick testing.</td></tr><tr><td align="center">[Enterprise]<br>Alert Engine</td><td>Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and using Webhooks.<br>AE does not require any external components or a database as it does not store anything. It receives events and sends notifications under the conditions which have been pre-configured upstream with triggers.</td></tr></tbody></table>

### Architecture diagram <a href="#architecture-diagram" id="architecture-diagram"></a>

![Self-Hosted Architecture](https://dobl1.github.io/gravitee-se-docs/latest/assets/gio-apim-self-hosted-architecture.svg)

#### Install on VMs : LAN + DMZ deployment <a href="#install-on-vms-lan-dmz-deployment" id="install-on-vms-lan-dmz-deployment"></a>

![Self-Hosted Architecture LAN + DMZ](https://dobl1.github.io/gravitee-se-docs/latest/assets/gio-apim-self-hosted-architecture-vms.svg)

## Hybrid architecture

Hybrid architecture refers to when certain Gravitee API Management components are managed as SaaS components by Gravitee and others remain self-hosted by the customer and/or user.&#x20;

### Overall separation of components <a href="#components" id="components"></a>

![Hybrid Architecture Components](https://dobl1.github.io/gravitee-se-docs/latest/assets/gio-apim-hybrid-components.svg)

### SaaS Components <a href="#saas-components" id="saas-components"></a>

These "SaaS Components" are the components that Gravitee manages.

<table><thead><tr><th width="186" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">Gravitee API Mamagement UI<br>(for API producers)</td><td>This web UI gives easy access to some key <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-rest-api">APIM API</a> services. <a href="https://docs.gravitee.io/apim/3.x/apim_overview_concepts.html#gravitee-concepts-publisher">API Publishers</a> can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</td></tr><tr><td align="center">Dev / API Portal<br>(for API consumers)</td><td>This web UI gives easy access to some key <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-rest-api">APIM API</a> services. <a href="https://docs.gravitee.io/apim/3.x/apim_overview_concepts.html#gravitee-concepts-consumer">API Consumers</a> can use it to search for, view, try out and subscribe to a published API.<br>They can also use it to manage their <a href="https://docs.gravitee.io/apim/3.x/apim_overview_concepts.html#gravitee-concepts-application">applications</a>.</td></tr><tr><td align="center">Management API</td><td>This RESTful API exposes services to manage and configure the <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-mgmt-ui">APIM Console</a> and <a href="https://docs.gravitee.io/apim/3.x/apim_overview_components.html#gravitee-components-portal-ui">APIM Portal</a> web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the <a href="https://docs.gravitee.io/apim/3.x/apim_installguide_rest_apis_documentation.html">API Reference</a> section.</td></tr><tr><td align="center">SaaS API Gateways</td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="https://docs.gravitee.io/apim/3.x/apim_overview_plugins.html#gravitee-plugins-policies">policies</a> (i.e., rules) to both HTTP requests and responses according to your needs. With these policies, you can enhance request and response processing by adding transformations, security, and many other exciting features.</td></tr><tr><td align="center">Bridge Gateways</td><td>A <em>bridge</em> API Gateway exposes extra HTTP services for bridging HTTP calls to the underlying repository (which can be any of our supported repositories: MongoDB, JDBC and so on)</td></tr><tr><td align="center">Config Database</td><td>All the API Management platform management data, such as API definitions, users, applications and plans.</td></tr><tr><td align="center">S3 Bucket + Analytics Database</td><td>Analytics and logs data</td></tr><tr><td align="center">[Enterprise]<br>Gravitee Cloud</td><td>Cockpit is a centralized, multi-environments / organizations tool for managing all your Gravitee API Management and Access Management installations in a single place.</td></tr><tr><td align="center">[Enterprise]<br>API Designer</td><td>Drag-and-Drop graphical (MindMap based) API designer to quickly and intuitively design your APIs (Swagger / OAS) and even deploy mocked APIs for quick testing.</td></tr><tr><td align="center">[Enterprise]<br>Alert Engine</td><td>Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and using Webhooks.<br>AE does not require any external components or a database as it does not store anything. It receives events and sends notifications under the conditions which have been pre-configured upstream with triggers.</td></tr></tbody></table>

### On-prem / Private cloud components <a href="#on-prem-private-cloud-components" id="on-prem-private-cloud-components"></a>

These "On-prem/Private cloud components" are components that the customer and/or user manages.

<table><thead><tr><th width="191" align="center">Component</th><th>Description</th></tr></thead><tbody><tr><td align="center">Gravitee.io APIm Gaetway</td><td>APIM Gateway is the core component of the APIM platform, smartly proxing trafic applying policies.</td></tr><tr><td align="center">Logstash</td><td>Collect and send local Gateways logs and metrics to the Gravitee.io APIM SaaS Control Plane.</td></tr><tr><td align="center">Redis</td><td>Database use locally for rate limits synchronized counters (RateLimit, Quota, Spike Arrest) and optionnaly as an external cache for the <a href="https://docs.gravitee.io/apim/3.x/apim_resources_cache_redis.html#redis_cache_resource">Cache policy</a>.</td></tr></tbody></table>

### Gravitee hybrid architecture diagram <a href="#architecture-diagram" id="architecture-diagram"></a>

![Hybrid Architecture](https://dobl1.github.io/gravitee-se-docs/latest/assets/hybrid-architecture.svg)

### Self-Hosted to SaaS connections <a href="#self-hosted-to-saas-connections" id="self-hosted-to-saas-connections"></a>

![Hybrid Architecture Connections](https://dobl1.github.io/gravitee-se-docs/latest/assets/hybrid-architecture-connections.svg)

