# Solace

{% hint style="warning" %}
**Tech Preview**

Federated APIs are a Tech Preview feature and are not recommended for usage in production environments. If you are interested in trying our Gravitee Federated API Management, we highly recommend:

* Customers to reach out to their CSM or CSA
* Non-customers to [book some time](https://www.gravitee.io/demo) with a Gravitee Engineer for a demo and/or free POC



Gravitee does not provide formal support for tech preview features. Service-level agreements do not apply for tech preview features, and the use of tech preview features in production is at the sole risk and discretion of the customer.
{% endhint %}

## Overview

Gravitee's Solace integration supports exposing event protocols using Solace's Event Portal management API. The details of the Solace integration are described below.

{% hint style="info" %}
To access Solace's Event Portal, see [Getting Started with Event Portal's APIM/DevPortal API](https://ep-apim-devportal-integ-ea.readme.io/reference/getting-started-1#api-authentication).
{% endhint %}

## Import Rules for APIs

<figure><img src="../../../.gitbook/assets/event api product_single plan.png" alt=""><figcaption><p>Simplified import example</p></figcaption></figure>

Solace Event APIs are imported into Gravitee according to the following rules:

1. One Gravitee federated API is created per Event API that is part of an Event API Product. Gravitee metadata first confirms that the federated API does not already exist. A federated API inherits the attributes of the Solace Event API.
2. Gravitee extracts the AsyncAPI definition of each Event API from Solace to create an AsyncAPI documentation page for the federated API. By default, the page is published with private visibility.
3.  For each Solace plan associated with the Event API Product a Gravitee federated API belongs to, the federated API is allotted one Gravitee plan (default OAuth)&#x20;

    {% hint style="info" %}
    API Products do not have defined authentication schemes. Using OAuth for federated API plans ensures that applications are synced and subscription requests are handled properly. It does not restrict the use of other authentication mechanisms at runtime.
    {% endhint %}
4. Gravitee API plans inherit certain Event API Product information
5.  Gravitee only imports Event API Products whose [availability is set to “publicly available”](https://docs.solace.com/Cloud/Event-Portal/event-portal-designer-event-api-products.htm#Changing\_the\_State) to ensure that every Event API Product is fully deployed and ready to be consumed

    {% hint style="info" %}
    Gravitee only imports released Event API Products that are exposed with SMF protocol and have `PUBLISH_DESTINATIONS` set to `gravitee`. This custom attribute is used to filter out unwanted EAP.
    {% endhint %}
6. Gravitee only imports the latest version of an Event API Product

## Import rules for plans

### **Mapping Solace Event APIs to Gravitee federated APIs:**

| Event API    | Gravitee federated API |
| ------------ | ---------------------- |
| description  | description            |
| version      | version                |
| displayName  | -                      |
| name         | name                   |
| asyncAPI def | asyncAPI doc page      |

### **Mapping Solace Event API Products to Gravitee federated API plans:**

| Event API Product & plan | Gravitee federated API | Comment                                           |
| ------------------------ | ---------------------- | ------------------------------------------------- |
| name                     | plan.name              | Concatenated Event API Product name and plan name |
| description              | plan.description       |                                                   |
| plan.name                | plan.name              | Concatenated Event API Product name and plan name |
| -                        | plan.type = OAuth 2.0  | Default value                                     |

## OAuth subscriptions with a 3rd-party IdP

Solace requires a 3rd-party to act as the authorization server for OAuth. The client credentials flow is described below.&#x20;

1. An API consumer creates an application in the Gravitee Developer Portal
2. Because Dynamic Client Registration (DCR) is enabled, this request is forwarded to the 3rd-party IdP (e.g., Gravitee Access Management)
3. The 3rd-party IdP creates an application with a client ID and client secret and returns it to Gravitee
4. The API consumer can view the client ID and client secret
5. The API consumer subscribes the application to a Solace federated API
6. Gravitee [creates an equivalent application](https://ep-apim-devportal-integ-ea.readme.io/reference/createappregistration) in Solace (if it doesn’t exist already) using the client ID and (optionally) client secret
7. Gravitee [creates an access request](https://ep-apim-devportal-integ-ea.readme.io/reference/createappregistrationaccessrequest) (equivalent to a subscription) for this application to access the API Product
8. The application requests and receives an OAuth access token from the 3rd-party IdP using its client ID and secret
9. The application uses the access token to connect to the Solace gateway (a dedicated Solace broker)
10. Solace validates the access token with the 3rd-party IdP that has been registered as an OAuth provider on the broker:
    1. Solace gets the client ID from the access token (either from the token itself or from the 3rd-party IdP)
    2. Solace matches the client ID against its authorization groups (i.e., subscriptions) to verify whether the request should be accepted

{% hint style="info" %}
See Solace's [OAuth Authentication](https://docs.solace.com/Security/Configuring-Client-Authentication.htm#OAuth) documentation for more information.
{% endhint %}
