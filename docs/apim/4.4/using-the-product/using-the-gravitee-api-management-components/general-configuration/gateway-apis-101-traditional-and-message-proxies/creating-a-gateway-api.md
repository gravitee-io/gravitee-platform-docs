---
description: Configuration guide for Creating a Gateway API.
---

# Creating a Gateway API

### Access API creation wizard

To get started, you need to access your **APIs** homescreen. This screen displays the status of all the Gateway APIs that have been created in your current environment.

Assuming you have the proper permissions, you can access and modify the configurations of existing APIs, or, in our case, create new APIs.

<figure><img src="broken-reference" alt=""><figcaption><p>APIs homscreen</p></figcaption></figure>

> * [x] Select **APIs** in the sidebar of the Console UI
> * [x] Next, select **+ Add API** in the top right to create a new API

You will be greeted with several options to create an API. We will be creating a v4 API from scratch with the help of the creation wizard.

<figure><img src="broken-reference" alt=""><figcaption><p>Options to create a new Gateway API</p></figcaption></figure>

> * [x] Select the green **Create =>** button shown next to **Create a V4 API from scratch**

### API details

API details is the first step of the API creation wizard. Provide a name, version, and (optionally) a description for your API. This is the metadata for your API.

<figure><img src="broken-reference" alt=""><figcaption><p>Fill in API details</p></figcaption></figure>

> * [x] Provide a name, version, and (optionally) a description for your API
> * [x] Select **Validate my API details** to move on to the next step

### Proxy selection: Choose your path

This step is where you decide between the [traditional proxy and message proxy](./#traditional-and-message-proxies):

* **Traditional proxy:** Select **Proxy Upstream Protocol** to configure the Gateway API to proxy backend API servers
* **Message proxy**: Select **Introspect Messages From Event-Driven Backend** to configure the Gateway API to proxy event/message brokers

{% hint style="warning" %}
Message proxies require an enterprise license. If you don't have one, you can [schedule a demo](https://www.gravitee.io/demo).
{% endhint %}

In the Console UI, choose which type of proxy you'd like to create based on the backend resource you're most interested in exposing. If you don't have a preference, we recommend trying a traditional proxy first, as it is easier to conceptualize.

<figure><img src="broken-reference" alt=""><figcaption><p>Traditional or message proxy selection</p></figcaption></figure>

> * [x] Choose **Proxy Upstream Protocol** or **Introspect Messages from Event-Driven Backend**
