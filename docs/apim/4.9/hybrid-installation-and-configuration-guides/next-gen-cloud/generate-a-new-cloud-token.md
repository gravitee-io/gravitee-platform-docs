---
description: An overview about generate a new cloud token.
---

# Generate a New Cloud Token

## Overview

When you revoke a Cloud token, you terminate the link between the Cloud and your hybrid Gateway. If you suspect the link to your Gateway has been compromised, termination eliminates a potentially insecure connection. When you generate a new Cloud token, you ensure that only authorized access is permitted over a secure and managed Gateway connection.

## Generate a Cloud token

1.  Sign in to [Gravitee Cloud](https://cloud.gravitee.io/).

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
2.  Navigate to the **Gateways** section, and then click the Gateway for which you want to generate a new Cloud token.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
3.  In the **Hybrid Gateway Details** screen, navigate to the **Cloud Tokens** section.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
4.  Click the **bin** icon.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
5.  In the **Revoke Cloud Token** pop-up window, type **revoke**, and then click **Revoke Token.** Your Cloud token is deleted.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
6.  In the **Cloud Tokens** section, click **Generate Cloud Token.**

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>
7.  In the **Copy your Cloud Token** pop-up window, click **Copy and Close**.

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning">
      <p>Store your Cloud token somewhere secure.</p>
    </div>

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

    \### Verification

*   In the **Hybrid Gateway Details** screen, navigate to the **Cloud Tokens** section. The table shows the date and time that you created the Cloud token.

    <figure><img src="broken-reference" alt=""><figcaption></figcaption></figure>

## Next steps

* (Optional) Link your Cloud token to a hybrid Gateway. For more information about linking to a hybrid Gateway, see [link-to-a-hybrid-gateway.md](link-to-a-hybrid-gateway.md "mention").
