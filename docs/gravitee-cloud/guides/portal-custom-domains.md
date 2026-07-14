---
description: >-
  Configure a custom domain for the Developer Portal and the Portal API of a
  Gravitee Cloud environment, so your developers reach the portal under your own
  branded URL.
---

# Configure a Custom Domain for the Developer Portal

## Overview

With custom domains, you serve the Developer Portal of a Gravitee Cloud environment from your own domain, for example `developers.example.com` instead of the default Gravitee portal URL.

A custom domain is configured for each environment, and it has two independent targets:

* **Portal URL**: the Developer Portal that your API consumers open in a browser.
* **Portal API URL**: the Portal API that the Developer Portal calls.

Each target takes one custom domain. The default Gravitee-provided URL remains functional as a fallback.

To configure a custom domain for a Gateway instead, see [Configure a Custom Domain for a Gateway](custom-domains.md).

## Prerequisites

* A Gravitee Cloud customer account. Custom domains for the Developer Portal aren't available on trial accounts.
* Cloud Account Owner permissions. The **Custom Domain** menu doesn't appear for other roles.
* An environment with the Developer Portal enabled.
* Access to your domain registrar to manage DNS records (CNAME).

## Add a custom domain

1.  From the **Dashboard**, open the environment that you want to configure the custom domain for.

    <!-- TODO: Screenshot of the environment selected from the Dashboard -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-portal-custom-domain-environment.png" alt=""><figcaption></figcaption></figure>
2.  In the environment menu, click **Custom Domain**.

    <!-- TODO: Screenshot of the Custom Domain item in the environment menu -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-portal-custom-domain-menu.png" alt=""><figcaption></figcaption></figure>
3. Click the tab for the target that you want to configure:
   1. Click **Portal URL** to configure the domain of the Developer Portal.
   2. Click **Portal API URL** to configure the domain of the Portal API.
4. In the **Custom Domain Name** field, enter your domain. For example, `developers.example.com`. The domain follows these rules:
   1. The domain is a valid domain name that contains only lowercase letters, numbers, hyphens, and dots.
   2. The maximum length is 253 characters.
5.  Click **Save**.

    <!-- TODO: Screenshot of the Custom Domain card with a domain entered and the Save button -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-portal-custom-domain-save.png" alt=""><figcaption></figcaption></figure>

Gravitee creates the domain and triggers a DNS deployment job in the background. Until you create the CNAME record, the **CNAME Record Instructions** section shows the status `not verified`.

Repeat these steps on the other tab to configure the second target. Configure both **Portal URL** and **Portal API URL** so that the Developer Portal and the API it calls are served from your own domain.

## Configure the DNS

{% hint style="warning" %}
Forward only the DNS record to Gravitee. Don't create an A record or modify any other DNS setting for this domain.
{% endhint %}

Create a **CNAME record** at your domain registrar. To find the values for the record, complete the following steps:

1. Scroll to the **CNAME Record Instructions** section of the tab that you configured.
2.  Read the values from the table. The **Value** column contains the Gravitee host that your domain points to.

    <!-- TODO: Screenshot of the CNAME Record Instructions section -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-portal-custom-domain-cname.png" alt=""><figcaption></figcaption></figure>

Create the record with these values:

<table>
    <thead>
        <tr>
            <th width="120">Type</th>
            <th width="260">Name</th>
            <th>Value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>CNAME</td>
            <td>Your custom domain, for example <code>developers.example.com</code></td>
            <td>The Gravitee host shown in the <strong>Value</strong> column</td>
        </tr>
    </tbody>
</table>

### Ownership verification and SSL certificate issuance

Once the CNAME record resolves, Gravitee verifies that you own the domain with an HTTP-01 challenge, and then issues an SSL certificate for HTTPS traffic using Google CA. Both steps are automatic. The process takes between a few minutes and 24 hours, depending on DNS propagation.

## Verification

To verify that the custom domain is live, follow these steps:

1. Open the **Custom Domain** page for your environment, and then click the tab of the target that you configured.
2.  Check the status badges. The **CNAME Record Instructions** section shows the status of the DNS record, and the **SSL Certificate Issuance** section shows the status of the certificate.

    <table>
        <thead>
            <tr>
                <th width="200">Status</th>
                <th>Meaning</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>verified</code> and <code>issued</code></td>
                <td>The CNAME record is correct, and the SSL certificate is issued. The custom domain is live.</td>
            </tr>
            <tr>
                <td><code>verifying</code></td>
                <td>Gravitee is checking the DNS record or issuing the certificate.</td>
            </tr>
            <tr>
                <td><code>not verified</code></td>
                <td>The CNAME record isn't detected yet, so the certificate is pending.</td>
            </tr>
            <tr>
                <td><code>not configured</code></td>
                <td>No custom domain is saved for this target.</td>
            </tr>
            <tr>
                <td><code>error</code></td>
                <td>The DNS configuration is wrong, or the certificate issuance failed.</td>
            </tr>
        </tbody>
    </table>
3.  Click the **Refresh** icon in the **SSL Certificate Issuance** section to update the status.

    <!-- TODO: Screenshot of the status badges with the Refresh icon -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-portal-custom-domain-status.png" alt=""><figcaption></figcaption></figure>
4. Open your custom domain in a browser. The Developer Portal loads over HTTPS.

## Reset a custom domain

{% hint style="warning" %}
Resetting a custom domain removes it from the environment. Traffic that reaches the Developer Portal through this domain stops working immediately. The default Gravitee-provided URL keeps working.
{% endhint %}

1. Open the **Custom Domain** page for your environment, and then click the tab of the target that you want to reset.
2. Click **Reset**.
3.  In the confirmation dialog, click **Reset Custom Domain**.

    <!-- TODO: Screenshot of the Reset Custom Domain confirmation dialog -->
    <figure><img src="../.gitbook/assets/PLACEHOLDER-portal-custom-domain-reset.png" alt=""><figcaption></figcaption></figure>

Delete the CNAME record from your domain registrar as well.
