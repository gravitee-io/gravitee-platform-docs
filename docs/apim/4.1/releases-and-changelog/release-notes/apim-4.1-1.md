---
description: This article covers the new features released in Gravitee API Management 4.1
---

# APIM 4.1

{% hint style="danger" %}
**Make sure you upgrade your license file**

If you are an existing Gravitee Enterprise customer upgrading to 4.x, please make sure that you upgrade your Gravitee license file. Reach out to your Customer Success Manager or Support team in order to receive a new 4.x license.
{% endhint %}

## Introduction

Gravitee 4.1 was released on September 28th, 2023, and introduced broadened support for asynchronous APIs, event brokers, and protocol mediation, especially as it pertains to what is surfaced in the API Management Console. For a paired-down version of what was released, please see the [changelog for Gravitee APIM 4.x](../changelogs/apim-4.0.x-changelog.md).

## v4 API configuration

### Webhook entrypoint

You can enable Dead Letter Queue to define an external storage where each unsuccessfully pushed message will be stored and configure a replay strategy. A pre-existing and supported endpoint or endpoint group can be selected. This is an advanced configuration that requires having the endpoint already configured. Refer to the [configuration details](../../guides/api-configuration/v4-api-configuration/entrypoint-configuration.md#webhook) for more information.

### Endpoint management and defaults

Endpoints and endpoint groups that have already been configured can be modified or deleted. Single endpoints and endpoint groups can also be added following initial endpoint configuration. By default, the API will use the first endpoint group listed, but the user is able to change the order of the list.

The configuration of an endpoint during the creation workflow determines the endpoint group’s default configuration. The endpoint then inherits this configuration from the group by default. Unless inheritance is disabled, changes to the endpoint group configuration will proliferate to all endpoints in the group.

By default, an endpoint added to an endpoint group will inherit the group's configuration. This allows an API publisher to quickly add new endpoints with the same settings and behavior as other endpoints in the group. Changes can be made to the new endpoint's configuration if inheritance is disabled, and will persist if inheritance remains disabled.

For more information on endpoint enhancements, refer to [this guide](../../guides/api-configuration/v4-api-configuration/endpoint-configuration.md#endpoint-management).

### User and group access&#x20;

You can manage user and group access to individual APIs via the Management Console. You can add members to your API and alter member roles, which come with specific permissions. You can also add groups to your API to give all members of those groups access. In addition, the owner of an API can transfer ownership to another member, user, or group by selecting a stakeholder and assigning that stakeholder a role. For more information, refer to [this guide](../../guides/api-configuration/v2-api-configuration/configure-user-and-group-access.md).

### Quality of Service

4.1 introduces enhanced QoS support for various entrypoint, protocol, and endpoint selections. The QoS compatibility matrix can be found [here](../../guides/api-configuration/v4-api-configuration/quality-of-service.md).

## Importing and duplicating v4 APIs

You can now create a v4 API by uploading a JSON file containing an existing Gravitee v4 API definition. For the details of this feature, refer to the [documentation](../../guides/create-apis/import-apis.md).

A v4 API can now also be duplicated. Refer to [this page](../../guides/api-configuration/v4-api-configuration/api-general-settings.md) for more details.

## Logging

The Management Console now allows you to view comprehensive connection logs to analyze the usage of your v4 message APIs. The record will be paginated with no limit to the number of pages, and if logging is disabled, existing logs will still be displayed. Runtime log settings can be modified to customize and extend the data capture. You can also drill into a log entry to view detailed message content. For more information on logging, refer to [this section](../../getting-started/configuration/configure-apim-management-api/logging.md#management-console-logging).
