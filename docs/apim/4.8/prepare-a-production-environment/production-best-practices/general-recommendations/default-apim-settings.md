---
description: Configuration guide for default apim settings.
---

# Default APIM Settings

Perform the following steps in APIM Console to update the most common default settings.

1. Log in to APIM Console.
2. Select **Settings**.
3. In the **Portal** section:
   1. Select **Settings** in the inner sidebar.
   2.  Update the **Company name.**

       <figure><img src="../../../.gitbook/assets/prod_def apim1.png" alt=""><figcaption><p>Portal settings</p></figcaption></figure>
4. In the **Gateway** section:
   1. Select **API Logging**.
   2.  Update the maximum logging duration for APIM API logging to avoid flooding. In this example, we have configured a logging duration of 15 minutes:

       <figure><img src="../../../.gitbook/assets/prod_def apim2.png" alt=""><figcaption><p>API logging settings</p></figcaption></figure>
5. Select **Organization** in the main sidebar:
   1. In the **Gateway** section:
      1. Select **Sharding Tags**.
      2.  In the **Entrypoint mappings** section of the page, update the **Entrypoint** field with your APIM API endpoint.

          <figure><img src="../../../.gitbook/assets/prod_def apim3.png" alt=""><figcaption><p>Save sharding tag</p></figcaption></figure>
   2. Select **Settings** in the inner sidebar:
      * Update the **Title** of APIM Console to make it more appropriate to your own environment.
      *   Update the **Management URL** to your APIM Console URL.

          <figure><img src="../../../.gitbook/assets/prod_def apim4.png" alt=""><figcaption><p>Organization settings</p></figcaption></figure>
