---
description: An overview about cloud certificate renewal.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/hybrid-installation-and-configuration-guides/classic-cloud/cloud-certificate-renewal
---

# Cloud Certificate Renewal

## Overview

To maintain the connection between your self-hosted Gravitee instance and Gravitee Cloud, you need a valid certificate. Certificates are valid for one year and must be renewed annually. Check your current certificate to keep track of its expiration date. You must renew your certificate prior to the expiration date for an uninterrupted connection to Gravitee Cloud.

## Renew using the Gravitee API

To renew your certificate using the Gravitee API, you need the endpoint URL and an account token.

The syntax for the endpoint URL is `https://YOUR-CLOUD-ENVIRONMENT/management/accounts/YOUR-ACCOUNT-ID/certificate/renewcert`. You can obtain the values for `YOUR-CLOUD-ENVIRONMENT` and `YOUR-ACCOUNT-ID` when you create an account token.

To create an account token and then call the API, follow the steps below.

1.  [Log in](https://eu.cloud.gravitee.io/) to your Gravitee Cloud account.

    <figure><img src="../../.gitbook/assets/00 cert cloud.png" alt=""><figcaption></figcaption></figure>
2.  Select **Settings** from the menu, go to the **Account tokens** page, and then click **Generate Account Token**.

    <figure><img src="../../.gitbook/assets/00 cert generate.png" alt=""><figcaption></figcaption></figure>
3.  Give your token a name, and then click **Generate**. Save both your account token and the URL from the **Example** section.

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>In the image below, the URL is <code>https://eu.cloud.gravitee.io/management/accounts/7b6f41d3-7118-41e9-af41-d3711801e973</code>. The environment is <code>eu.cloud.gravitee.io</code> and the account ID is <code>7b6f41d3-7118-41e9-af41-d3711801e973</code>.</p></div>

    <figure><img src="../../.gitbook/assets/00 cert token.png" alt=""><figcaption></figcaption></figure>

    4\. In Postman, select POST as the type of HTTP request, and then enter your endpoint. The endpoint is the URL from your token generation concatenated with \`/certificate/renewcert\`. \ \ For example, \`https://eu.cloud.gravitee.io/management/accounts/7b6f41d3-7118-41e9-af41-d3711801e973/certificate/renewcert\`.

    <figure><img src="../../.gitbook/assets/00 cert 01.png" alt=""><figcaption></figcaption></figure>
4.  Under the **Authorization** header, use the drop-down menu to select **Bearer Token** as the **Auth Type**, and then enter your account token.

    <figure><img src="../../.gitbook/assets/00 cert 02.png" alt=""><figcaption></figcaption></figure>
5.  Click **Send** to renew your certificate. The certificate is returned in base64.

    <figure><img src="../../.gitbook/assets/00 cert post 2.png" alt=""><figcaption></figcaption></figure>
