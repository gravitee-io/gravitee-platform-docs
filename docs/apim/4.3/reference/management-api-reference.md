---
description: >-
  The Management API empowers orgs to manage APIs effectively, automate
  processes, and enhance developer experiences
---

# Management API Reference

## Overview

The Management API component manages the configuration of the entire Gravitee APIM platform. By exposing its RESTful endpoints, administrators, developers, and other stakeholders can interact with the APIM platform programmatically.

## Documentation Viewer

Before using the Gravitee API docs, we highly recommend reading the contextual information in the sections below. To explore the API documentation, select from the following endpoints categories to open an integrated API viewer and client. The viewer includes an option to download the API specification.

* [**Console UI and v2 APIs Endpoints Documentation Viewer**](https://gravitee-io-labs.github.io/mapi-v1-docs/#tag/api-alerts)**:** Manage all aspects of the Console UI and v2 APIs, e.g., import, update, export, and delete API definitions to configure plans, policies, users, groups, and analytics settings.
* [**v4 API Endpoints Documentation Viewer**](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-apis/)**:** Manage v4 APIs, e.g., import, update, export, and delete API definitions to configure plans, policies, users, groups, and analytics settings.
* [**Portal Endpoints Documentation Viewer**](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-portal/)**:** Manage all aspects of the Developer Portal.
* [**Plugin Endpoints Documentation Viewer**](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-plugins/)**:** Read-only. Get information on entrypoints, endpoints, and policy plugins.
* [**Installation Endpoints Documentation Viewer**](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-installation/)**:** Read-only. Get environment and organization details.
* [**OEM Customization Endpoints Documentation Viewer**](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-ui/)**:** Read-only. Get details around OEM customization of the Console UI.

## Management API Deep Dive

The Management API consists of two main subcomponents, [**`Management`**](management-api-reference.md#management) and [**`Portal`**](management-api-reference.md#portal), which cater to distinct needs.&#x20;

All Management API endpoints are accessible via the main Management API component, e.g., at `http://localhost:8083` in a local installation.

### Management

There are two versions of the `Management` subcomponent: V1 and V2.

{% tabs %}
{% tab title="V1" %}
V1 is the initial version of the Management API, which covers all v2 APIs (including plans, policies, documentation, etc.) and all other resources available in the Console UI, e.g., applications, subscriptions, users, etc.&#x20;

The **V1 specification** (YAML OAS) is available at `/management/openapi.yaml` of the Management API component.
{% endtab %}

{% tab title="V2" %}
V2 is the latest version of the Management API, which currently covers v4 APIs (including plans, policies, documentation, etc.), plugins, installation, and OEM customization of the Console UI. T

The **V2 home page** is accessible at `/management/v2/` of the Management API component. It is split into four groups:

* **v4 APIs**: Accessible at `/management/v2/openapi-apis.yaml` of the Management API
* **Plugins**: Accessible at `/management/v2/openapi-plugins.yaml` of the Management API
* **Installation**: Accessible at `/management/v2/openapi-installation.yaml` of the Management API
* **OEM Customizations**: Accessible at `/management/v2/openapi-ui.yaml` of the Management API
{% endtab %}
{% endtabs %}

### Portal

The Portal API is used to power the [Developer Portal](../guides/developer-portal/README.md), and can be used as the backend API for a custom developer portal. Whether you’re building an external (potentially public-facing) portal or an internal developer hub, the Portal API empowers you to create a compelling and efficient platform.

The **Portal API specification** (YAML OAS) can be found at `/portal/openapi` of the Management API component.
