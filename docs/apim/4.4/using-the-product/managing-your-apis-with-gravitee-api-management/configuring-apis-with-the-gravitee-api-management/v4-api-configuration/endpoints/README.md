---
description: >-
  This article introduces endpoint behavior and the processes for configuring
  and managing v4 API endpoints
---

# Endpoints

## Introduction

In Gravitee, Gateway endpoints define the protocol and configuration settings by which the Gateway API will fetch data from, or post data to, the backend API. After you've created your Gateway API and selected your endpoint(s), you can configure them in the API Management Console. The following sections:

* [Link to endpoint configuration and implementation](README.md#configuration-and-implementation)
* [Describe endpoint management](README.md#endpoint-management)
* [Describe endpoint default behavior](README.md#default-behavior)

## Configuration and implementation

Click on the tiles below to learn how to configure and implement v4 proxy API endpoints and v4 message API endpoints.

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>v4 Proxy API Endpoints</td><td></td><td><a href="v4-proxy-api-endpoints.md">v4-proxy-api-endpoints.md</a></td></tr><tr><td></td><td>v4 Message API Endpoints</td><td></td><td><a href="v4-message-api-endpoints/">v4-message-api-endpoints</a></td></tr><tr><td></td><td>Health-check</td><td></td><td><a href="health-check.md">health-check.md</a></td></tr></tbody></table>

## Endpoint management

### Single endpoints

After you've configured your endpoints, you can modify or delete existing endpoints, or add new ones:

<figure><img src="../../../../../.gitbook/assets/Screen Shot 2023-07-18 at 10.41.53 AM.png" alt=""><figcaption><p>Edit single endpoints</p></figcaption></figure>

* **Modify:** To alter an existing endpoint, select the <img src="../../../../../.gitbook/assets/Screen Shot 2023-07-18 at 10.43.13 AM.png" alt="" data-size="line"> icon, and then edit your endpoint configuration.&#x20;
* **Delete:** To delete an existing endpoint, select the <img src="../../../../../.gitbook/assets/Screen Shot 2023-07-18 at 10.46.30 AM.png" alt="" data-size="line">icon underneath **ACTIONS** in the **Endpoints** menu.
* **Add:** To add a new endpoint, click **Add endpoint**. Configure the endpoint per the instructions in the [API creation documentation](../../../create-apis/the-api-creation-wizard/v4-api-creation-wizard.md).

When you are done, make sure to redeploy the API for your changes to take effect.

### Endpoint groups

After you've configured your endpoints, you can modify or delete existing endpoint groups, or add new ones:

<figure><img src="../../../../../.gitbook/assets/endpoint groups v4 message api backend.png" alt=""><figcaption><p>Edit endpoint groups</p></figcaption></figure>

* **Modify:** To modify an endpoint group, click **Edit** to the right of the group name.
* **Delete:** To delete an endpoint group, click **Delete** to the right of the group name**.** You will be prompted to confirm deletion of the endpoint group. If only one endpoint group exists, you will not have the option to delete it.
* **Add:** To add a new endpoint group, click **Add endpoint group** at the bottom of the page and configure the group's default values. Only one type of endpoint group can be created at a time. By default, the new endpoint group will contain an endpoint that automatically inherits the group's default configuration.

When you are done, make sure to redeploy the API for your changes to take effect.

## Default behavior

### Single endpoint

Within an endpoint group, clicking `Add Endpoint` toggles `Inherit configuration from the endpoint group` to ON by default:

<figure><img src="../../../../../.gitbook/assets/default behavior toggle to inherit.png" alt=""><figcaption><p>Toggle to inherit endpoint configuration</p></figcaption></figure>

If an endpoint is added to the endpoint group, it will inherit the group's configuration by default. This allows an API publisher to quickly add new endpoints with the same settings and behavior as other endpoints in the group.

If `Inherit configuration from the endpoint group` is toggled OFF, changes can be made to the new endpoint's configuration. When these changes are saved, the configuration is updated.&#x20;

If `Inherit configuration from the endpoint group` remains OFF, the updated values will persist. Subsequent updates to the group’s default configuration will not override this endpoint's configuration once it has been modified to no longer inherit from the group.

### Endpoint group

* During the API creation workflow, the endpoint configuration determines the endpoint group’s default configuration. The endpoint then inherits this configuration from the group by default.
* If the configuration of an endpoint group is updated, all the endpoints with `Inherit configuration from the endpoint group` enabled will be similarly updated and remain static.
* By default, the API will use the first endpoint group listed. This is indicated by the **Default** badge next to the group name. You can click the up/down arrow keys to reorder the endpoint groups and assign a different default:

<figure><img src="../../../../../.gitbook/assets/default endpoint group (1).png" alt=""><figcaption><p>Default endpoint group</p></figcaption></figure>
