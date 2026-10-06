---
description: Unless an API has a keyless plan, a consumer registers an application in the Developer Portal 4.11 and subscribes. Follow the steps.
---

# Create an Application

## Overview

Unless the API has a keyless plan, a consumer must register an application and subscribe to a published API plan to access an API. Applications act on behalf of the user to request tokens, provide user identity information, and retrieve protected resources from remote services and APIs.

## Create an application

1.  In the Developer Portal, click on **Applications** in the header

    <figure><img src="../../.gitbook/assets/applications_home.png" alt="The portal Applications page listing one application card with its description and owner."><figcaption><p>Create an app</p></figcaption></figure>
2.  On the **General** page, specify:

    * **Application name:** Give your application a name (required)
    * **Description:** Describe the purpose of your application (required)
    * **Domain used by the application:** Enter the domain to be used by the application or keep the pre-filled default
    * (Optional) **Application Image:** Select an image for your application

    <figure><img src="../../.gitbook/assets/applications_general.png" alt="The General step of the create application wizard, with the application name, description and domain fields beside an image upload area."><figcaption><p>General application configuration</p></figcaption></figure>
3. Select the appropriate tile to configure security for the type of _software application_ you're registering your application for. Each application type requires you to set certain parameters.

{% tabs %}
{% tab title="Simple" %}
A Simple application is hands-free. With this application, you have the ability to define the client ID.

Parameters:

* **Type:** Enter the type of application (mobile, web, etc.).
* **Client ID:** Enter the client ID of the application. This field is required to subscribe to certain API plans (OAuth2, JWT).

<figure><img src="../../.gitbook/assets/applications_security simple.png" alt="The Security step of the create application wizard with the Simple application type selected, above type and client ID fields."><figcaption><p>Configure a Simple application</p></figcaption></figure>
{% endtab %}

{% tab title="SPA" %}
A **SPA**, or single-page application (Angular, React, etc.), is a web application that performs the majority of the user interface logic in a web browser and uses web APIs to communicate with the web server.

Parameters:

* Toggle **Authorization Code** and **Implicit** to enable the types of rights authorized for the client. For security, define only the types you need.
* Use the **+** icon to add **Redirect URIs** where the authorization server will send OAuth responses.

<figure><img src="../../.gitbook/assets/applications_security spa check.png" alt="The Security step with the SPA application type selected, Authorization Code enabled, and a redirect URI added as a chip."><figcaption><p>Configure a SPA application</p></figcaption></figure>

{% hint style="info" %}
Until you add a **Redirect URI**, a red "x" will appear in lieu of the green checkmark above **Security**:

<img src="../../.gitbook/assets/applications_security spa x.png" alt="The Security step with the SPA type selected and a redirect URI typed but not yet added, and the step marked incomplete." data-size="original">
{% endhint %}
{% endtab %}

{% tab title="Web" %}
A traditional **Web** application (Java, .Net, etc.) performs the majority of the application logic on the server.

Parameters:

* Toggle **Authorization Code**, **Refresh Token**, and **Implicit (Hybrid)** to enable the types of rights authorized for the client. For security, define only the types you need.
* Use the **+** icon to add **Redirect URIs** where the authorization server will send OAuth responses.

<figure><img src="../../.gitbook/assets/applications_security web.png" alt="The Security step with the Web application type selected and Authorization Code, Refresh Token and Implicit hybrid options listed."><figcaption><p>Configure a Web application</p></figcaption></figure>

{% hint style="info" %}
Once you add a **Redirect URI**, a green checkmark will appear in lieu of the red "x" above **Security.**
{% endhint %}
{% endtab %}

{% tab title="Native" %}
A **Native** application (iOS, Android, etc.) can be installed directly on a mobile device.

Parameters:

* Toggle **Authorization Code**, **Refresh Token**, **Resource Owner Password**, and **Implicit (Hybrid)** to enable the types of rights authorized for the client. For security, define only the types you need.
* Use the **+** icon to add **Redirect URIs** where the authorization server will send OAuth responses.

<figure><img src="../../.gitbook/assets/applications_security native.png" alt="The Security step with the Native application type selected and Authorization Code, Refresh Token, Resource Owner Password and Implicit hybrid options listed."><figcaption><p>Configure a Native application</p></figcaption></figure>

{% hint style="info" %}
Once you add a **Redirect URI**, a green checkmark will appear in lieu of the red "x" above **Security.**
{% endhint %}
{% endtab %}

{% tab title="Backend to backend" %}
A **Backend to backend** application is machine to machine and does not require a user interface.

Parameters:

* Toggle **Client Credentials** to enable the types of rights authorized for the client. For security, define only the types you need.

<figure><img src="../../.gitbook/assets/applications_security b2b.png" alt="The Security step with the Backend to backend type selected and only Client Credentials available."><figcaption><p>Configure a Backend to backend application</p></figcaption></figure>
{% endtab %}
{% endtabs %}

4.  Use the search field to find an API for your application, then subscribe to it. Optionally, you can leave a comment for the API owner.

    <figure><img src="../../.gitbook/assets/applications_subscribe.png" alt="The Subscription step of the create application wizard, with an API searched, a plan selected, and the resulting subscription request listed."><figcaption><p>Subscribe to an API</p></figcaption></figure>
5.  Review the information you entered, then click **CREATE THE APP**:

    <figure><img src="../../.gitbook/assets/applications_validate.png" alt="The Validation step of the create application wizard, summarising the general and security choices beside the subscription request."><figcaption></figcaption></figure>

{% hint style="success" %}
You have successfully created an application!
{% endhint %}

## Application options

Once you've created an application, you can click on it and use the header options to review and edit the details of its configuration and usage:

*   **General information:** View and/or modify the application's configuration.

    <figure><img src="../../.gitbook/assets/application_edit.png" alt="The General information tab of an application, with name, description, domain and client ID fields beside an options panel and a list of subscribed APIs."><figcaption><p>General information</p></figcaption></figure>
*   **Metadata:** Enter a **Name** and **Value** and use the **Format** selector to define metadata for your application. Use the **ADD** and **UPDATE** buttons to modify your entries.

    <figure><img src="../../.gitbook/assets/application_metadata.png" alt="The Metadata tab of an application, listing two metadata entries with their format and value, above Reset and Update buttons."><figcaption><p>Metadata</p></figcaption></figure>
*   **Subscriptions:** View the APIs your application is subscribed to. Use the **API** drop-down menu to choose a particular API and the **status** drop-down menu to list all APIs with the selected status.

    <figure><img src="../../.gitbook/assets/application_subscription info.png" alt="The Subscriptions tab of an application, with API and status filters above a table showing one accepted subscription."><figcaption><p>Subscriptions</p></figcaption></figure>
* **Members:** View and edit member information. Adding a member requires the create permission on application members, and transferring ownership requires the update permission. A user whose application role lacks these permissions doesn't see or complete these actions. An application keeps exactly one primary owner at all times.
  *   **MEMBERS LIST:** View the names and roles of current application members.

      <figure><img src="../../.gitbook/assets/application_members list.png" alt="The Members list of an application, showing one member with the primary owner role."><figcaption><p>Members list</p></figcaption></figure>
  *   **ADD A MEMBER:** Use the search field to add a member to the application and assign that member a role.

      <figure><img src="../../.gitbook/assets/application_add a member.png" alt="The Add a member form, with a user search field and a role list set to USER."><figcaption><p>Add a member</p></figcaption></figure>
  *   **TRANSFER OWNERSHIP:** Transfer ownership of the application to another user and select a different role for the current primary owner.

      <figure><img src="../../.gitbook/assets/application_transfer ownership.png" alt="The Transfer ownership form, with a search field for a new primary owner and a role list for the current owner."><figcaption><p>Transfer ownership</p></figcaption></figure>
  *   **INHERITED MEMBERS:** View the names and roles of members inherited from other groups.

      <figure><img src="../../.gitbook/assets/application_inherited members.png" alt="The Inherited members section, listing one member inherited from a group with their role."><figcaption><p>Inherited members</p></figcaption></figure>
*   **Analytics:** Use the available filters to refine the application logs. Scroll down to view other metrics related to the application (top paths, top APIs, response times, etc.). The application analytics view displays traffic from v2 APIs only. Calls made through v4 APIs don't appear in these metrics. For the detailed support matrix, see [Application-level analytics](../../create-and-configure-apis/gravitee-api-definitions/v2-and-v4-api-comparison.md#application-level-analytics).

    <figure><img src="../../.gitbook/assets/application_analytics.png" alt="The Analytics tab of an application, with time-range buttons and advanced filters above the top paths and status panels."><figcaption><p>Analytics</p></figcaption></figure>
*   **Logs:** Use the available filters to view and optionally export refined application analytics. Scroll down to view the logs. The Classic Developer Portal displays application logs for v2 APIs only. To view application logs for v4 APIs, use the [New Developer Portal](../new-developer-portal/application-logs.md).

    <figure><img src="../../.gitbook/assets/application_logs.png" alt="The Logs tab of an application, with time-range buttons and advanced filters above export, analytics and search buttons."><figcaption><p>Logs</p></figcaption></figure>
*   **Notifications:** Specify which of your application's subscription events you would like to be notified of.

    <figure><img src="../../.gitbook/assets/application_alerts.png" alt="The Notifications tab of an application, listing subscription and support events each with a toggle, all switched on."><figcaption><p>Notifications</p></figcaption></figure>
*   **Alerts:** Use the fields and drop-down menus to define an alert. After you **ADD AN ALERT**, it will appear in the **ALERTS LIST**. Application members will be notified via email.

    <figure><img src="../../.gitbook/assets/application alerts.png" alt="The Alerts tab of an application, showing one configured alert above a form for adding another."><figcaption><p>Alerts</p></figcaption></figure>
