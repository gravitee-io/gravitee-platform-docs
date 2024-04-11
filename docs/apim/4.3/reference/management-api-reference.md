---
description: >-
  The Management API component manages the configuration of the entire Gravitee
  APIM platform. It empowers orgs to manage APIs effectively, automate
  processes, and enhance developer experiences.
---

# Management API Reference

## API documentation

Before using the Gravitee API docs, we highly recommend reading the contextual information in the sections below. That said, if you'd like to go ahead and explore the API documentation first, please see the tabs below.

{% hint style="warning" %}
These API docs are for v2 of our management API. To learn more about the different versions, please [refer to the relevant section below](management-api-reference.md#management).
{% endhint %}

{% tabs %}
{% tab title="APIs" %}
Manage APIs, e.g., import, update, export, and delete API definitions. You can also configure plans, policies, users, groups, and analytics settings.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-apis.html` , also available online [here](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-apis/)
* **Specification** (YAML OAS): `/management/v2/openapi-apis.yaml`, also available online [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.3.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-apis.yaml)
{% endtab %}

{% tab title="Plugins" %}
Read-only. Get information on entrypoints, endpoints, and policy plugins.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-plugins.html`, also available online [here](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-plugins/)
* **Specification** (YAML OAS): `/management/v2/openapi-plugins.yaml`, also available online [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.3.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-plugins.yaml)
{% endtab %}

{% tab title="UI/Console" %}
Read-only. Get the Console UI details.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-ui.html`, also available online [here](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-ui/)
* **Specification** (YAML OAS): `/management/v2/openapi-installation.yaml`, also available online [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.3.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-ui.yaml)
{% endtab %}

{% tab title="Installation" %}
Read-only. Get environment and organization details.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-installation.html`, also available online [here](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-installation/)
* **Specification** (YAML OAS): `/management/v2/openapi-installation.yaml`, also available online [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.3.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-installation.yaml)
{% endtab %}
{% endtabs %}

## Overview

The Management API exposes a set of RESTful endpoints that allow administrators, developers, and other stakeholders to interact with the APIM platform programmatically.\
The Management API consists of two main subcomponents, [**`Management`**](management-api-reference.md#management) and [**`Portal`**](management-api-reference.md#portal), which cater to distinct needs.&#x20;

All Management API endpoints are accessible via the main Management API component, e.g., at `http://localhost:8083` in a local installation.

## Management

{% hint style="warning" %}
Gravitee.io maintains two versions of the`Management`subcomponent concurrently. V1 remains operational to accommodate backward compatibility, but while the transition to V2 will be gradual to promote smooth adoption, users are encouraged to embrace V2 to benefit from feature enhancements.&#x20;
{% endhint %}

### **V1**

V1 is the initial version of the Management API, which covers all resources: APIs (including plans, policies, documentation, etc.), applications, subscriptions, users, etc.&#x20;

The **V1 specification** (YAML OAS) is available at `/management/openapi.yaml` of the Management API component.

### **V2**

The **V2 home page** is accessible at `/management/v2/` of the Management API component. It comprises four sections, which are described below.

{% tabs %}
{% tab title="APIs" %}
Manage APIs, e.g., import, update, export, and delete API definitions. You can also configure plans, policies, users, groups, and analytics settings.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-apis.html` , also available online [here](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-apis/)
* **Specification** (YAML OAS): `/management/v2/openapi-apis.yaml`, also available online [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.3.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-apis.yaml)
{% endtab %}

{% tab title="Plugins" %}
Read-only. Get information on entrypoints, endpoints, and policy plugins.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-plugins.html`, also available online [here](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-plugins/)
* **Specification** (YAML OAS): `/management/v2/openapi-plugins.yaml`, also available online [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.3.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-plugins.yaml)
{% endtab %}

{% tab title="UI (Console)" %}
Read-only. Get the Console UI details.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-ui.html`, also available online [here](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-ui/)
* **Specification** (YAML OAS): `/management/v2/openapi-installation.yaml`, also available online [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.3.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-ui.yaml)
{% endtab %}

{% tab title="Installation" %}
Read-only. Get environment and organization details.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-installation.html`, also available online [here](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-installation/)
* **Specification** (YAML OAS): `/management/v2/openapi-installation.yaml`, also available online [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.3.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-installation.yaml)
{% endtab %}
{% endtabs %}

## Portal

The Portal API is used to power the [Developer Portal](../guides/developer-portal/), but can also integrate into a custom developer portal. Whether you’re building an external (potentially public-facing) portal or an internal developer hub, the Portal API empowers you to create a compelling and efficient platform.

The **Portal API specification** (YAML OAS) can be found at `/portal/openapi` of the Management API component, which is also available online [here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.3.x/gravitee-apim-rest-api/gravitee-apim-rest-api-portal/gravitee-apim-rest-api-portal-rest/src/main/resources/portal-openapi.yaml) or with an OAS viewer [here](https://gravitee-io-labs.github.io/mapi-v2-docs-openapi-portal/).
