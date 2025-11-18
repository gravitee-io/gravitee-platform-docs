# Introduction to Gravitee API Management

## Overview

Gravitee API Management is a lightweight and performant management tool that accelerates and streamlines the governance and security of both synchronous and asynchronous APIs. It provides a centralized platform from which to measure and control API consumption, share and discover APIs, and manage the API lifecycle, versioning, and documentation.

As a highly flexible and scalable solution, Gravitee APIM integrates with a customer's infrastructure and conforms to specific business needs. APIM is fully extensible using its own internal plugin system where customers can define their own policies and develop their own reporting systems.

Select from the options below to learn more about APIM and get it up and running.

## Gravitee Architecture

Gravitee offers three different API Management architecture schemes: [self-hosted](./#self-hosted-architecture), [hybrid](./#hybrid-architecture), and [Gravitee-managed](./#gravitee-managed-architecture).

Each architecture relies on a specific set of Gravitee components. Some components are common to all architectures while others are architecture-specific. The following table compares the component types and management of self-hosted and hybrid architectures.

### Component Descriptions

Component descriptions for the full catalog of Gravitee architecture components are summarized in the following table:

<table><thead><tr><th width="199">Component</th><th>Description</th></tr></thead><tbody><tr><td>APIM Console<br>(for API producers)</td><td>This web UI gives easy access to some key APIM Management API services. <a href="./#api-publisher">API publishers</a> can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</td></tr><tr><td>APIM Management API</td><td>This RESTful API exposes services to manage and configure the APIM Console and APIM Developer Portal web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the<a href="using-the-product/using-the-gravitee-api-management-components/general-configuration-1/management-api-reference.md"> Management API Reference</a> section.</td></tr><tr><td>APIM Developer Portal<br>(for API consumers)</td><td>This web UI gives easy access to some key APIM API services. Allows <a href="./#api-consumer">API Consumers</a> to <a href="using-the-product/managing-your-apis-with-gravitee-api-management/api-exposure-plans-applications-and-subscriptions/#applications">manage their applications</a> and search for, view, try out, and subscribe to a published API.</td></tr><tr><td>APIM Gateway</td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="using-the-product/managing-your-apis-with-gravitee-api-management/policy-studio/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</td></tr><tr><td>Bridge Gateway</td><td>In a hybrid architecture, a <em>bridge</em> API Gateway exposes extra HTTP services for bridging HTTP calls to the underlying repository (which can be any of our supported repositories: MongoDB, JDBC, etc.)</td></tr><tr><td>Config Database</td><td>Database that stores API Management data such as API definitions, users, applications, and plans.</td></tr><tr><td>Analytics Database</td><td>Database that stores Gateway events and logs. In a hybrid architecture, the Analytics Database is supplemented by an "S3 Bucket."</td></tr><tr><td>Logstash</td><td>Collects and sends local Gateway logs/metrics to the Gravitee APIM SaaS Control Plane. Exclusive to hybrid architecture and hosted by user on-prem or in a private cloud.</td></tr><tr><td>Redis</td><td>Local database for rate limit synchronized counters (Rate Limit, Quota, Spike Arrest). (Optional) Acts as an external cache in accordance with the Cache policy. Exclusive to hybrid architecture and hosted by user on-prem or in a private cloud.</td></tr><tr><td>[Enterprise]<br>Gravitee Cockpit</td><td>Tool for centralized, multi-environment/organization management of APIM and AM installations.</td></tr><tr><td>[Enterprise]<br>API Designer</td><td>Drag-and-drop graphical (MindMap-based) tool to quickly and intuitively design APIs (Swagger/OAS) and deploy mocked APIs for testing.</td></tr><tr><td>[Enterprise]<br>Alert Engine</td><td>Provides APIM and AM users with efficient and flexible API platform monitoring. Enables advanced alerting configuration and notifications sent via webhooks or over email, Slack, etc.<br>Does not require external components or a database; receives events and sends notifications according to conditions pre-configured upstream via triggers.</td></tr></tbody></table>

### Self-hosted architecture

Self-hosted architecture refers a scheme where all Gravitee API Management components are hosted by the user on-prem and/or in a private cloud. Gravitee Cockpit and API Designer are optional Gravitee-managed components that can be connected to a self-hosted API Management installation.

The following diagrams illustrate the component management, design, and virtual machine internal/external access deployment of a self-hosted architecture.

#### Self-hosted component management

<img src="../4.1/.gitbook/assets/file.excalidraw (7).svg" alt="" class="gitbook-drawing">

#### Self-hosted architecture diagram

<img src="../4.1/.gitbook/assets/file.excalidraw (6).svg" alt="Self-hosted architecture" class="gitbook-drawing">

#### Self-hosted VM installation: LAN + DMZ deployment

<img src="../4.1/.gitbook/assets/file.excalidraw (5).svg" alt="Self-hosted architecture LAN + DMZ" class="gitbook-drawing">

### Hybrid architecture

Hybrid architecture refers to a scheme where certain Gravitee API Management components are Gravitee-managed SaaS components while others remain self-hosted by the user on-prem and/or in a private cloud. Gravitee Cockpit and API Designer are optional Gravitee-managed components that can be connected to a hybrid API Management installation.

The following diagrams illustrate the component management, design, and self-hosted-to-SaaS connections of a hybrid architecture.

#### Hybrid component management

<img src="../4.0/.gitbook/assets/file.excalidraw (1).svg" alt="" class="gitbook-drawing">

#### Hybrid architecture diagram

<img src="../4.1/.gitbook/assets/file.excalidraw (4).svg" alt="" class="gitbook-drawing">

#### Self-hosted-to-SaaS connections

<img src="../../../.gitbook/assets/file.excalidraw (15) (1).svg" alt="Hybrid: SaaS to self-hosted connections" class="gitbook-drawing">

### Gravitee-managed architecture

Gravitee-managed architecture refers to a scheme where all Gravitee API Management components are Gravitee-managed SaaS components. Gravitee Cockpit and API Designer are optional and can be connected to a Gravitee-managed API Management installation.
