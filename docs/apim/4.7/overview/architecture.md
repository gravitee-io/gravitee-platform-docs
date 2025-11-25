---
description: An overview about architecture.
---

# Architecture

## Overview

Gravitee offers three different API Management architecture schemes: [self-hosted](architecture.md#self-hosted-architecture), [hybrid](architecture.md#hybrid-architecture), and [Gravitee-managed](architecture.md#gravitee-managed-architecture).

Each architecture relies on a specific set of Gravitee components. Some components are common to all architectures while others are architecture-specific. The following table compares the component types and management of self-hosted and hybrid architectures.

<table><thead><tr><th width="326">Component</th><th data-type="checkbox">Self-hosted</th><th data-type="checkbox">Hybrid</th></tr></thead><tbody><tr><td>API Management Console</td><td>true</td><td>true</td></tr><tr><td>Management API</td><td>true</td><td>true</td></tr><tr><td>Developer Portal</td><td>true</td><td>true</td></tr><tr><td>APIM Gateway</td><td>true</td><td>true</td></tr><tr><td>Bridge Gateway</td><td>false</td><td>true</td></tr><tr><td>Config Database</td><td>true</td><td>true</td></tr><tr><td>Analytics Database</td><td>true</td><td>true</td></tr><tr><td>Logstash</td><td>false</td><td>true</td></tr><tr><td>Redis</td><td>false</td><td>true</td></tr><tr><td>Rate Limits Database</td><td>true</td><td>false</td></tr><tr><td>[Enterprise] Gravitee Cockpit</td><td>true</td><td>true</td></tr><tr><td>[Enterprise] API Designer</td><td>true</td><td>true</td></tr><tr><td>[Enterprise] Alert Engine</td><td>true</td><td>true</td></tr></tbody></table>

## Component Descriptions

Component descriptions for the full catalog of Gravitee architecture components are summarized in the following table:

<table><thead><tr><th width="199">Component</th><th>Description</th></tr></thead><tbody><tr><td>APIM Console<br>(for API producers)</td><td>This web UI gives easy access to some key APIM Management API services. API publishers can use it to publish APIs.<br>Administrators can also configure global platform settings and specific portal settings.</td></tr><tr><td>APIM Management API</td><td>This RESTful API exposes services to manage and configure the APIM Console and APIM Developer Portal web UIs.<br>All exposed services are restricted by authentication and authorization rules. For more information, see the<a href="../management-api/management-api-reference.md"> Management API Reference</a> section.</td></tr><tr><td>APIM Developer Portal<br>(for API consumers)</td><td>This web UI gives easy access to some key APIM API services. Allows API consumers to manage their applications and search for, view, try out, and subscribe to a published API.</td></tr><tr><td>APIM Gateway</td><td>APIM Gateway is the core component of the APIM platform. You can think of it like a smart reverse proxy.<br><br>Unlike a traditional HTTP proxy, APIM Gateway has the capability to apply <a href="broken-reference/">policies</a> (i.e., rules or logic) to both the request and response phases of an API transaction. With these policies, you can transform, secure, monitor, etc., your APIs.</td></tr><tr><td>Bridge Gateway</td><td>In a hybrid architecture, a <em>bridge</em> API Gateway exposes extra HTTP services for bridging HTTP calls to the underlying repository (which can be any of our supported repositories: MongoDB, JDBC, etc.)</td></tr><tr><td>Config Database</td><td>Database that stores API Management data such as API definitions, users, applications, and plans.</td></tr><tr><td>Analytics Database</td><td>Database that stores Gateway events and logs. In a hybrid architecture, the Analytics Database is supplemented by an "S3 Bucket."</td></tr><tr><td>Logstash</td><td>Collects and sends local Gateway logs/metrics to the Gravitee APIM SaaS Control Plane. Exclusive to hybrid architecture and hosted by user on-prem or in a private cloud.</td></tr><tr><td>Redis</td><td>Local database for rate limit synchronized counters (Rate Limit, Quota, Spike Arrest). (Optional) Acts as an external cache in accordance with the Cache policy. Exclusive to hybrid architecture and hosted by user on-prem or in a private cloud.</td></tr><tr><td>[Enterprise]<br>Gravitee Cloud</td><td>Tool for centralized, multi-environment/organization management of APIM and AM installations.</td></tr><tr><td>[Enterprise]<br>API Designer</td><td>Drag-and-drop graphical (MindMap-based) tool to quickly and intuitively design APIs (Swagger/OAS) and deploy mocked APIs for testing.</td></tr><tr><td>[Enterprise]<br>Alert Engine</td><td>Provides APIM and AM users with efficient and flexible API platform monitoring. Enables advanced alerting configuration and notifications sent via webhooks or over email, Slack, etc.<br>Does not require external components or a database; receives events and sends notifications according to conditions pre-configured upstream via triggers.</td></tr></tbody></table>

## Self-hosted architecture

Self-hosted architecture refers a scheme where all Gravitee API Management components are hosted by the user on-prem and/or in a private cloud. Gravitee Cloud and API Designer are optional Gravitee-managed components that can be connected to a self-hosted API Management installation.

The following diagrams illustrate the component management, design, and virtual machine internal/external access deployment of a self-hosted architecture.

## Self-hosted component management

![](../../4.0/.gitbook/assets/file.excalidraw%20\(7\)%20\(1\).svg)

### Self-hosted architecture diagram

![Self-hosted architecture](../../4.0/.gitbook/assets/file.excalidraw%20\(6\)%20\(1\).svg)

### Self-hosted VM installation: LAN + DMZ deployment

![Self-hosted architecture LAN + DMZ](../../4.0/.gitbook/assets/file.excalidraw%20\(5\)%20\(1\).svg)

## Hybrid architecture

Hybrid architecture refers to a scheme where certain Gravitee API Management components are Gravitee-managed SaaS components while others remain self-hosted by the user on-prem and/or in a private cloud. Gravitee Cloud and API Designer are optional Gravitee-managed components that can be connected to a hybrid API Management installation.

The following diagrams illustrate the component management, design, and self-hosted-to-SaaS connections of a hybrid architecture.

### Hybrid component management

<img src="../../4.0/.gitbook/assets/file.excalidraw (7) (1).svg" alt="" class="gitbook-drawing">

### Hybrid architecture diagram

![](../../4.0/.gitbook/assets/file.excalidraw%20\(4\)%20\(1\).svg)

### Self-hosted-to-SaaS connections

<img src="../../4.0/.gitbook/assets/file.excalidraw (6) (1).svg" alt="Hybrid: SaaS to self-hosted connections" class="gitbook-drawing">

## Gravitee-managed architecture

Gravitee-managed architecture refers to a scheme where all Gravitee API Management components are Gravitee-managed SaaS components. Gravitee Cloud and API Designer are optional and can be connected to a Gravitee-managed API Management installation.
