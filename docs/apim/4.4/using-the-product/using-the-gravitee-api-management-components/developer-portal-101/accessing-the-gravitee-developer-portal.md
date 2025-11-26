---
description: Configuration guide for Accessing the Gravitee Developer Portal.
---

# Accessing the Gravitee Developer Portal

Enterprise trial users should be able to immediately access the Developer Portal from the APIM Console by selecting the **Developer Portal** link in the top left of the Console's nav bar.

<details>

<summary>Self-managed installation: Adding a Developer Portal link</summary>

The Developer Portal host of self-managed installations can easily be modified. You can manually add the **Portal URL** to see the Developer Portal link in the Console UI.

Your Developer Portal URL will depend on your deployment, so please reference the respective installation docs. For example, with the default Docker installation, you can access the Developer Portal at `http://localhost:8085` in your browser.

<img src="../../../.gitbook/assets/self-managed dev portal link.png" alt="Update Developer Portal settings in the Console" data-size="original">

* [x] Click **Settings** in the sidebar
* [x] Click **Settings** in the inner sidebar
* [x] Scroll down to **Portal** settings and provide a **Portal URL** based on your deployment configuration
* [x] Scroll to the bottom of the page and click **Save**

</details>

<figure><img src="../../../.gitbook/assets/DP_console.png" alt=""><figcaption><p>Access Developer Portal from APIM Console</p></figcaption></figure>

> * [x] Select the **Developer Portal** link in the top left of your Console's nav bar

This will bring you to the homescreen of the Developer Portal.

<figure><img src="../../../.gitbook/assets/DP_default.png" alt=""><figcaption><p>Your default Developer Portal</p></figcaption></figure>

From here, you can immediately begin searching for APIs using the Developer Portal's full-context[^1] search. However, you will not be able to subscribe to any APIs until you create an application.

[^1]: Full-context meaning it searches through the definition and metadata of all published APIs that you have access to
