---
description: An overview about add security.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/getting-started/create-and-publish-your-first-api/add-security
---

# Add Security

## Overview

This guide shows you how to add security to your API by adding an API Key plan to your API.

## Prerequisites

* Complete the steps in [create-an-api.md](create-an-api.md "mention").

## Add security to your API

To add security to your API, complete the following steps:

1. [#add-an-api-key-plan-to-your-api](add-security.md#add-an-api-key-plan-to-your-api "mention")
2. [#remove-the-keyless-plan-from-your-api](add-security.md#remove-the-keyless-plan-from-your-api "mention")

### Add an API Key plan to your API

1.  From the **Dashboard**, click **APIs**.

    <figure><img src="../../.gitbook/assets/FEF08D45-E65E-4131-8D16-4D1D767906F0.jpeg" alt=""><figcaption></figcaption></figure>
2.  Click your API.

    <figure><img src="../../.gitbook/assets/image (320).png" alt=""><figcaption></figcaption></figure>
3.  Click **Consumers**.

    <figure><img src="../../.gitbook/assets/1CEDFEB8-E635-41FE-BEFC-3B815EEB1D69.jpeg" alt=""><figcaption></figcaption></figure>
4.  Click **+ Add new plan**, and then click **API Key**.

    <figure><img src="../../.gitbook/assets/58672F6C-4830-4710-B006-0CFF36ECC865.jpeg" alt=""><figcaption></figcaption></figure>
5.  In the **Name** field, type a name for your API.

    <figure><img src="../../.gitbook/assets/CC6C89DF-138E-4A61-BAF7-D681DCC651C8.jpeg" alt=""><figcaption></figcaption></figure>
6.  In the **Subscriptions section**, turn on **Auto validate subscription**.

    <figure><img src="../../.gitbook/assets/46EB2A9A-7339-4073-BE36-7EED0ECB6F95.jpeg" alt=""><figcaption></figcaption></figure>
7.  Click **Next**.

    <figure><img src="../../.gitbook/assets/E43BBC55-59A5-4CC6-B689-57D5433E1F35.jpeg" alt=""><figcaption></figcaption></figure>
8.  In the API Key authentication configuration screen, click **Next**.

    <figure><img src="../../.gitbook/assets/image (30).png" alt=""><figcaption></figcaption></figure>
9.  Click **Create**.

    <figure><img src="../../.gitbook/assets/image (31).png" alt=""><figcaption></figcaption></figure>
10. In the **Consumers** screen, click the **Publish the plan** button.

    <figure><img src="../../.gitbook/assets/80812F89-F280-4D0C-A83B-EB9417385B96.jpeg" alt=""><figcaption></figcaption></figure>
11. In the Publish plan pop-up window, click **Publish.**

    <figure><img src="../../.gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>
12. Click **Deploy API**.

    <figure><img src="../../.gitbook/assets/8AB63E94-AAA6-4BDA-B648-077BB451A35C (1).jpeg" alt=""><figcaption></figcaption></figure>
13. In the **Deploy your API** pop-up window, click **Deploy**.

    <figure><img src="../../.gitbook/assets/image (33).png" alt=""><figcaption></figcaption></figure>

#### Verification

The new plan appears in the **PUBLISHED** tab of the **Consumers** screen.

<figure><img src="../../.gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>

### Remove the Keyless plan from your API

{% hint style="danger" %}
WARNING: Removing a plan is irreversible
{% endhint %}

1.  Navigate to the **PUBLISHED** tab of the screen.

    <figure><img src="../../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>
2.  For your **Default Keyless (UNSECURED)** plan, click **Close the plan** button.

    <figure><img src="../../.gitbook/assets/3627B0A7-AF24-4E4B-A22B-5AFEB7FB29A5.jpeg" alt=""><figcaption></figcaption></figure>
3.  In the **Close plan** pop-up window, type Default Keyless (UNSECURED), and then click **Yes, close this plan.**

    <figure><img src="../../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

#### Verification

The Default Keyless (UNSECURED) plan is removed from the **PUBLISHED** tab.

<figure><img src="../../.gitbook/assets/image (16).png" alt=""><figcaption></figcaption></figure>

## Verification

To test your API Key plan, complete the following steps:

* [#retrieve-your-api-key](add-security.md#retrieve-your-api-key "mention")

### Retrieve your API Key

1.  From the **Dashboard**, click **Applications**.

    <figure><img src="../../.gitbook/assets/22CB1B38-1964-47F6-B5B7-8B634D3D8D0B.jpeg" alt=""><figcaption></figcaption></figure>
2.  In the **Applications** screen, click the **Default application**.

    <figure><img src="../../.gitbook/assets/image (17).png" alt=""><figcaption></figcaption></figure>
3.  In the **Default application** configuration screen, click **Subscriptions**.

    <figure><img src="../../.gitbook/assets/F1AD5888-A518-42D5-8C18-33BCCB583C06.jpeg" alt=""><figcaption></figcaption></figure>
4.  Click **+ Create a subscription**.

    <figure><img src="../../.gitbook/assets/AD60FD6C-ECAB-49A1-80B3-2C0BD89F08EA (1).jpeg" alt=""><figcaption></figcaption></figure>
5. In the **Create a subscription** pop-up window, complete the following sub-steps:
   1. Type the name of the API that you created in [create-an-api.md](create-an-api.md "mention").
   2. Select your API.
   3. Click the name of the plan that you created in [#add-an-api-key-plan-to-your-api](add-security.md#add-an-api-key-plan-to-your-api "mention").
   4.  Click **Create**.

       <figure><img src="../../.gitbook/assets/image (18).png" alt=""><figcaption></figcaption></figure>
6.  Copy your API key from the **API Keys** section of the **Subscriptions** page.

    <figure><img src="../../.gitbook/assets/0E509DC6-90E7-4154-B768-920FB55DA442.jpeg" alt=""><figcaption></figcaption></figure>

### Test your API Key

*   Test your API Key with the following command:

    ```
    curl -i "http://<gateway-domain>:<gateway-port>/<api-context-path>" \
      -H "X-Gravitee-Api-Key: <your-api-key>"
    ```

    * Replace `<gateway-domain>` with the hostname or IP address of your Gravitee gateway. For example, `localhost:` .
    * Replace `<gateway-port>` with the port where the gateway is exposed. For example, `8082` .
    * Replace `<api-context-path>` with the context path for your API. For example, myfirstapi.
    * Replace `<your-api-key>` with the API for your subscription.

You receive a `200 OK` response.

## Next steps

Add a policy to your API. For more information about adding a policy, see [add-a-policy.md](add-a-policy.md "mention").
