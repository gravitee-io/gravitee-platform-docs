# Configuration

## Overview

The **Configuration** section allows you to manage and customize the following high-level settings:

* [General](configuration.md#general)
* [User Permissions](configuration.md#user-permissions)&#x20;
* [Properties](configuration.md#properties)
* [Resources](configuration.md#resources)
* [Notifications](configuration.md#notifications)
* [Audit Logs](configuration.md#audit-logs)

## General

The **General** tab displays a section for inputting general API details and a Danger Zone for executing functional and sometimes irreversible actions.

<figure><img src="../../.gitbook/assets/A 1 config general.png" alt=""><figcaption></figcaption></figure>

{% tabs %}
{% tab title="General details" %}
Configure the following API details and actions. Only **Name** and **Version** are required.

* Name
* Version
* Description
* Labels
* Categories
* API picture
* API background
* Owner, creation, and connection information
* The ability to export your API definition, import a new API definition to update your API, duplicate your API, and promote your API
{% endtab %}

{% tab title="Danger zone" %}
This section includes access to mission-critical (and potentially dangerous) actions:

* **Start the API:** Deploy the API to all Gateways, or the Gateways specified using [sharding tags](../../gravitee-gateway/sharding-tags.md)
* **Publish the API:** Publish the API to the Developer Portal
* **Make Public:** Make the API public so that everybody can see it
* **Deprecate:** Unpublish the API from the Developer Portal
* **Delete:** Delete the API
{% endtab %}
{% endtabs %}

Any time you make a change to your API, click the **Save** icon at the bottom of the screen.

## User Permissions

From the **User Permissions** tab, you can manage user and group access to individual APIs via the following actions:

* [Add members to an API](configuration.md#add-members-to-an-api)
* [Add groups to an API](configuration.md#add-groups-to-an-api)
* [Transfer API ownership](configuration.md#transfer-api-ownership)

{% hint style="info" %}
See [User Management](../../administration/user-management.md) to learn more about user and group creation and administration.
{% endhint %}

### Add members to an API

Click **+ Add members** to add members to your API or alter member roles, which grant specific permissions. For more information on roles, please refer to the [roles documentation.](../../administration/user-management.md#roles)

<figure><img src="../../.gitbook/assets/user permissions_add members alter roles.png" alt=""><figcaption><p>Add members and alter roles</p></figcaption></figure>

### Add groups to an API

To give groups access to your API, click **Manage groups** and select the desired group(s) from the drop-down menu. This will give all members of that group access to your API.

<figure><img src="../../.gitbook/assets/user permissions_manage groups.png" alt=""><figcaption><p>Give groups access to your API</p></figcaption></figure>

### Transfer API ownership

If you are the owner of the API, you can transfer ownership to another member, user, or group. Click **Transfer ownership**, then select **API member**, **Other user**, or **Primary owner group.** Next, define the stakeholder to which you want to transfer API ownership and assign that stakeholder a role.

<figure><img src="../../.gitbook/assets/user permissions_transfer ownership.png" alt=""><figcaption><p>Transfer API ownership</p></figcaption></figure>

## Properties

From the **Properties** tab you can configure your API properties, including dynamic properties and encryption.

Properties are read-only during the Gateway's execution of an API transaction. They can be accessed from within flows using Gravitee's Expression Language (EL) and the `#api.properties` statement. To configure properties:

To configure API properties:

1.  Select **Properties** from the inner left nav&#x20;

    <figure><img src="../../.gitbook/assets/v2 proxy_properties.png" alt=""><figcaption><p>Add API properties</p></figcaption></figure>
2. To add hardcoded properties, either:
   * Click **Add property** and enter property definitions one at a time as a key-value pair
   * Click **Import** and enter property definitions as a list in `<key>=<value>` format&#x20;

### Encryption

{% hint style="warning" %}
Encrypted values can be used by API policies, but encrypted data should be used with care. APIM Gateway will automatically decrypt these values.
{% endhint %}

To encrypt a hardcoded API property value:

1.  Reset the default secret key in `gravitee.yml`. The secret must be 32 bytes in length.&#x20;

    ```yaml
    # Encrypt API properties using this secret:
    api:
      properties:
        encryption:
             secret: vvLJ4Q8Khvv9tm2tIPdkGEdmgKUruAL6
     to provide the best security available.
    ```
2.  Enable the **Encrypt** toggle when adding a property via **Add property**. Once you click **Save**, you can no longer edit, modify, or view the value.&#x20;

    <div align="left"><figure><img src="../../.gitbook/assets/api properties_add (1).png" alt="" width="375"><figcaption></figcaption></figure></div>

### **Dynamic properties**

To configure dynamic properties:

1.  Click the **Manage dynamically** button and define the configuration&#x20;

    <figure><img src="../../.gitbook/assets/v2 proxy_properties dynamic.png" alt=""><figcaption><p>Configure dynamic properties</p></figcaption></figure>

    * Toggle **Enabled** to ON
    * **Schedule:** A cron expression to schedule the health check
    * **HTTP Method:** The HTTP method that invokes the endpoint
    * **URL:** The target from which to fetch dynamic properties
    * **Request Headers:** The HTTP headers to add to the request fetching properties
    * **Request body:** The HTTP body content to add to the request fetching properties
    * (Optional) **Transformation (JOLT specification):** If the HTTP service doesn’t return the expected output, edit the JOLT transformation accordingly
    * Toggle **Use system proxy** ON to use the system proxy configured in APIM installation
2. Click **Save**

After the first call, the resultant property is added to the list of global properties, where its value is continuously updated according to the `cron` schedule specified.

{% hint style="info" %}
Key-value pairs can also be maintained using a dictionary, e.g., if this information is stored independently of the API creation process or applies to multiple APIs.&#x20;
{% endhint %}

## Resources

The **Resources** tab allows you to configure resources for your API, which some policies support for actions such as authentication and schema registry validation. After you create resources, you will be able to reference them when designing policies.

{% hint style="info" %}
Though you can technically configure all resource types for Kafka APIs, only a subset of them are used in Kafka APIs.
{% endhint %}

The following resources are designed to be used with Kafka APIs:

| Resource                                | Description                                                                                                                                                                                                                             |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cache                                   | This resource maintains a cache linked to the API lifecycle, i.e., the cache is initialized when the API starts and released when the API stops. It is responsible for storing HTTP responses to avoid subsequent calls to the backend. |
| Cache Redis                             | This resource is the same as Cache, but the current implementation is based on Redis. It can be configured standalone or as part of the Redis Sentinel monitoring solution.                                                             |
| OAuth2 Gravitee AM Authorization Server | This resource introspects an access token generated by a Gravitee AM instance.                                                                                                                                                          |
| OAuth2 Generic Authorization Server     | This resource introspects an access token generated by a generic OAuth2 authorization server. It provides a configuration for how token introspection is applied to accommodate common authorization servers.                           |
| Confluent Schema Registry               | This resource fetches serialization/deserialization data from a Confluent schema registry.                                                                                                                                              |

To learn more about these resources and how to add them, refer to the [Resources](../../policies/resources.md) documentation.

## Notifications

The **Notifications** tab allows you to subscribe to notifications related to a specific API:

1. Log in to your **APIM Console**.
2. Select **APIs**, from the left nav.
3. Select your API.
4. Select **Configuration** from the inner left nav.
5.  Select the **Notifications** header.\


    <figure><img src="../../.gitbook/assets/A 1 config notifications.png" alt=""><figcaption></figcaption></figure>
6. Click **+ Add notification** to create a new one.
7. Give your notification a name and select either:
   * **Default Email Notifier:**
     * Enter a list of emails, using "," or ";" as the separator
   * **Default Webhook Notifier:**&#x20;
     * Enter the Webhook URL
     * Choose whether to use system proxy

<figure><img src="../../.gitbook/assets/A 1 notifications 2.png" alt=""><figcaption></figcaption></figure>

The following notifications are available to each notifier:

| Type         | Notification             | Description                                      |
| ------------ | ------------------------ | ------------------------------------------------ |
| API KEY      | API-Key Expired          | Triggered when an API Key is expired.            |
| API KEY      | API-Key Renewed          | Triggered when an API Key is renewed.            |
| API KEY      | API-Key Revoked          | Triggered when an API Key is revoked.            |
| SUBSCRIPTION | New Subscription         | Triggered when a Subscription is created.        |
| SUBSCRIPTION | Subscription Accepted    | Triggered when a Subscription is accepted.       |
| SUBSCRIPTION | Subscription Closed      | Triggered when a Subscription is closed.         |
| SUBSCRIPTION | Subscription Paused      | Triggered when a Subscription is paused.         |
| SUBSCRIPTION | Subscription Resumed     | Triggered when a Subscription is resumed.        |
| SUBSCRIPTION | Subscription Rejected    | Triggered when a Subscription is rejected.       |
| SUBSCRIPTION | Subscription Transferred | Triggered when a Subscription is transferred.    |
| SUBSCRIPTION | Subscription Failed      | Triggered when a Subscription fails.             |
| SUPPORT      | New Support Ticket       | Triggered when a new support ticket is created   |
| LIFECYCLE    | API Started              | Triggered when an API is started                 |
| LIFECYCLE    | API Stopped              | Triggered when an API is stopped                 |
| LIFECYCLE    | API Updated              | Triggered when an API is updated                 |
| LIFECYCLE    | API Deployed             | Triggered when an API is deployed                |
| LIFECYCLE    | API Deprecated           | Triggered when an API is deprecated              |
| RATING       | New Rating               | Triggered when a new rating is submitted         |
| RATING       | New Rating Answer        | Triggered when a new answer is submitted         |
| REVIEW       | Ask for API review       | Triggered when an API can be reviewed            |
| REVIEW       | Accept API review        | Triggered when an API's review has been accepted |
| REVIEW       | Reject API review        | Triggered when an API's review has been rejected |

## Audit Logs

The **Audit Logs** tab displays API-level events and audit entries, which are summarized in table format. These can be filtered by event type and date range.

<figure><img src="../../.gitbook/assets/A 1 config audit logs.png" alt=""><figcaption></figcaption></figure>
