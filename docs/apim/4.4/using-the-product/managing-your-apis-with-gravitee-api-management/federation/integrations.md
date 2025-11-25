---
description: Configuration guide for Integrations.
---

# Integrations

## Introduction

Integrations are components that allow users to connect Gravitee to 3rd-party API gateways or event brokers to discover, then import, APIs and other assets. The ability to import 3rd-party components into Gravitee facilitates the creation of both federated APIs and traditional proxy and message APIs.

Integrations are managed and configured through the Gravitee APIM Console. Each integration is paired with a component called an agent, which handles the communication between the 3rd-party provider and Gravitee.

## Integration management

Gravitee offers an integration plugin for every supported 3rd-party provider of gateways and brokers (e.g., AWS API Gateway and Solace). The configuration, lifecycle, and status of integrations can be managed from within Gravitee. Management includes creation, editing, and the configuration of different attributes and pages.

* [Prerequisites](integrations.md#prerequisites)
* [Permissions](integrations.md#permissions)
* [Create an integration](integrations.md#create-an-integration)
* [View or edit an integration](integrations.md#view-or-edit-an-integration)
* [Delete an integration](integrations.md#delete-an-integration)

### Prerequisites

All integration plugins that are not offered out-of-the-box must be installed before use. The following compatibility matrix identifies which integrations are supported by which versions of Gravitee.

| Gravitee version      | AWS API Gateway | Solace Event Broker |
| --------------------- | --------------- | ------------------- |
| Versions prior to 4.4 | No              | No                  |
| 4.4.x                 | Yes             | Yes                 |

### Permissions

The environment-level INTEGRATION permission corresponds to the following CRUD permissions:

* **Create:** Create a new integration
* **Read:** View an integration’s details
* **Update:** Modify an integration’s attributes, refresh agent status.
* **Delete:** Delete an integration

By default, user roles have the following permissions:

* **ADMIN:** CRUD
* **API\_PUBLISHER:** CRUD
* **USER:** \_R\_\_

### Create an integration

To create an integration, the user selects an integration type and provides basic information, such as a name and description. Once created, the integration must be connected to an agent to be fully functional.

1. Log in to your APIM Console
2. Select **Integrations** from the left nav
3.  Click **Create Integration**

    <figure><img src="../../../.gitbook/assets/integration_create (1).png" alt=""><figcaption></figcaption></figure>
4. Choose an integration provider
5.  Enter general information for the integration

    <figure><img src="../../../.gitbook/assets/integration_general info (1).png" alt=""><figcaption></figcaption></figure>
6.  Click **Create Integration**

    <figure><img src="../../../.gitbook/assets/integration_overview (1).png" alt=""><figcaption></figcaption></figure>

### View or edit an integration

Gravitee automatically detects which integrations were installed by the customer. Depending on the integration, parts of the UI are dynamic, such as forms for entering 3rd-party provider connection parameters. These forms adapt based on the schema provided by the integration.

To view or edit an integration:

1. Log in to your APIM Console
2. Select **Integrations** from the left nav
3.  Click on the integration you're interested in

    <figure><img src="../../../.gitbook/assets/integration_edit 2 (1).png" alt=""><figcaption></figcaption></figure>
4.  From the inner left nav, select **Overview** to run discovery and edit discovered APIs, or select **Configuration** to edit the general information or delete the integration (if no federated APIs are linked to it)

    <figure><img src="../../../.gitbook/assets/integration_edit 3 (1).png" alt=""><figcaption></figcaption></figure>

    \{% hint style="info" %\} Integration status provides the user with critical information, such as if the integration is active and can reach the agent, if the agent is running and can reach the provider, and if the agent is receiving errors. \{% endhint %\}

### Delete an integration

{% hint style="info" %}
An integration can only be deleted if it has no associated federated APIs.
{% endhint %}

To delete an integration:

1. Log in to your APIM Console
2. Select **Integrations** from the left nav
3. Click on the integration you're interested in
4. Select **Configuration** from the inner left nav
5.  In the **Danger Zone** section, click **Delete Integration**

    <figure><img src="../../../.gitbook/assets/integration delete (1).png" alt=""><figcaption></figcaption></figure>

    \{% hint style="info" %\} If **Delete Integration** is grayed out, you must first click **Delete APIs** to delete the federated APIs associated with the integration. \{% endhint %\}
