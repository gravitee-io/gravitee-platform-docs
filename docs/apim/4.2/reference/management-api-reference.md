---
description: >-
  The Management API component serves as the backbone for managing and
  configuring all aspects of the Gravitee.io API Management solution. It
  empowers organizations to manage APIs effectively, automate
---

# Management API Reference

The **Management API** exposes a set of RESTful endpoints that allow administrators, developers, and other stakeholders to interact with the platform programmatically.\
It is divided into two main parts, [**`Management`**](management-api-reference.md#management) and [**`Portal`**](management-api-reference.md#portal), each catering to distinct needs. All these elements are accessible via the management API itself (if you are running locally, at `http://localhost:8083`)

### Management

{% hint style="warning" %}
Gravitee.io currently maintains two versions concurrently. The reasons for this dual approach include backward compatibility, gradual migration, and feature enhancements. While V1 remains operational, the Gravitee.io team encourages users to embrace V2. The transition will be gradual over the next versions, allowing everyone to adapt smoothly and benefit from the latest advancements.
{% endhint %}

#### **V1**

The initial version of the Management API, covering all ressources : APIs (including Plans, Policies, Documentation, etc.), Applications, Subscriptions, Users, etc.

* **Specification** (YAML OAS): `/management/openapi.yaml`

#### **V2**

**Home Page**: `/management/v2/`

{% tabs %}
{% tab title="APIs" %}
Most likely what you are looking for ! This section allows you to manage APIs, including importing, updating, exporting and deleting API definitions. You can also configure Plans, Policies, Users, Groups and Analytics settings.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-apis.html` , [also available online here](https://elements-demo.stoplight.io/?spec=https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.2.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-apis.yaml#/).
* **Specification** (YAML OAS): `/management/v2/openapi-apis.yaml`, [also available online here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.2.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-apis.yaml).
{% endtab %}

{% tab title="Plugins" %}
Read-only. Get Entrypoints, Endpoints, and Policies plugins information.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-plugins.html`, [also available online here](https://elements-demo.stoplight.io/?spec=https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.2.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-plugins.yaml).
* **Specification** (YAML OAS): `/management/v2/openapi-plugins.yaml`, [also available online here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.2.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-plugins.yaml).
{% endtab %}

{% tab title="UI (Console)" %}
Read-only. Get the Console UI customizations details.

* **Documentation Page** (HTML page with an OAS viewer): `/management/v2/index-ui.html`, [also available online here](https://elements-demo.stoplight.io/?spec=https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.2.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-ui.yaml).
* **Specification** (YAML OAS): `/management/v2/openapi-ui.yaml`, [also available online here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.2.x/gravitee-apim-rest-api/gravitee-apim-rest-api-management-v2/gravitee-apim-rest-api-management-v2-rest/src/main/resources/openapi/openapi-ui.yaml).
{% endtab %}
{% endtabs %}

### Portal

The Portal API is used to powers the [Developer Portal](../guides/developer-portal/), but can be also used to integrate into a custom developer portal, whether you’re building an external (potentially public-facing) portal or an internal developer hub, the Portal API empowers you to create a compelling and efficient platform.

The **Portal API** specification (YAML OAS) can be found at `/portal/openapi`, [also available online here](https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.2.x/gravitee-apim-rest-api/gravitee-apim-rest-api-portal/gravitee-apim-rest-api-portal-rest/src/main/resources/portal-openapi.yaml) or [with an OAS viewer here](https://elements-demo.stoplight.io/?spec=https://raw.githubusercontent.com/gravitee-io/gravitee-api-management/4.2.x/gravitee-apim-rest-api/gravitee-apim-rest-api-portal/gravitee-apim-rest-api-portal-rest/src/main/resources/portal-openapi.yaml).
