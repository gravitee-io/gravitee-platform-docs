---
description: >-
  Configuration guide for Creating an application with the Gravitee Developer
  Portal.
---

# Creating an application with the Gravitee Developer Portal

### Create an application

Now that we have access to the Developer Portal, we can take on the role of an API consumer. The next step is to create an application that is used to register and agree to plans.

<figure><img src="../../../../../4.0/.gitbook/assets/DP_app page (1).png" alt=""><figcaption><p>Developer Portal Applications page</p></figcaption></figure>

> * [x] Select **Applications** in the top nav bar
> * [x] Select **+ Create an App** in the subnav bar

#### General step

This will open the application creation wizard. The **General** step is focused on providing application metadata.

<figure><img src="../../../../../4.0/.gitbook/assets/DP_general (1).png" alt=""><figcaption><p>General step of application creation wizard</p></figcaption></figure>

> * [x] Provide a name and description, then click **Next**

#### Security step

The next step is focused on **Security**. This page may look different depending on your **Client Registration** settings, which are configured in the APIM console. However, everyone should have the option to create a **Simple** application.

{% hint style="info" %}
**Dynamic Client Registration**

A **Simple** application allows an API consumer to define their own `client_id`, but this is not secure and should not be used outside of testing. Therefore, Gravitee allows you to disable **Simple** applications and [use dynamic client registration (DCR) to create advanced applications](https://documentation.gravitee.io/apim/guides/api-exposure-plans-applications-and-subscriptions/plans-1#advanced-application-configuration) with the identity provider of your choosing.
{% endhint %}

<figure><img src="../../../../../4.0/.gitbook/assets/DP_security (1).png" alt=""><figcaption><p>Security step of application creation wizard</p></figcaption></figure>

> * [x] Select a **Simple** application, then click **Next**

#### Subscription step

The **Subscription** step allows you to send API subscription requests as you are creating the application. You will be able to search for published APIs you have access to and view the available plans.

Once we finish creating the app, the request will be sent for review and approval by the API publisher.

<figure><img src="../../../../../4.0/.gitbook/assets/DP_subscription (1).png" alt=""><figcaption><p>Subscription step of application creation wizard</p></figcaption></figure>

> * [x] Search for the API you published and select it
> * [x] Select **Subscribe** under the API Key Plan, then click **Next**

#### Validation step

Finally, we just need to complete the **Validation** step. Review your application details and subscription request. If everything looks good, go ahead and create your app!

<figure><img src="../../../../../4.0/.gitbook/assets/DP_validation (1).png" alt=""><figcaption><p>Validation step of application creation wizard</p></figcaption></figure>

> * [x] Click **Create the App**

You should receive confirmation that your app was successfully created. Feel free to open your app and explore the different tabs.
