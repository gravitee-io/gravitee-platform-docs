# Generate a New Cloud Token

## Overview

When you revoke a Cloud token, you terminate the link between the Cloud and your hybrid Gateway. If you suspect the link to your Gateway has been compromised, termination eliminates a potentially insecure connection. When you generate a new Cloud token, you ensure that only authorized access is permitted over a secure and managed Gateway connection.

## Generate a Cloud token

1.  Sign in to [Gravitee Cloud](https://cloud.gravitee.io/).\\

    <figure><img src="../../.gitbook/assets/image (4) (1) (1).png" alt=""><figcaption></figcaption></figure>
2.  Navigate to the **Gateways** section, and then click the Gateway for which you want to generate a new Cloud token.\\

    <figure><img src="../../.gitbook/assets/64DFB5D8-427B-4FD2-8013-2206631FEDE2_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3.  In the **Hybrid Gateway Details** screen, navigate to the **Cloud Tokens** section. \\

    <figure><img src="../../.gitbook/assets/D25FD656-4D9B-426A-8B3E-7CB63E826C47_1_201_a (2) (1).jpeg" alt=""><figcaption></figcaption></figure>
4.  Click the **bin** icon.\\

    <figure><img src="../../.gitbook/assets/C0E81F31-A36F-4047-8660-BE4B0A72C1B9_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
5.  In the **Revoke Cloud Token** pop-up window, type **revoke**, and then click **Revoke Token.** Your Cloud token is deleted.\\

    <figure><img src="../../.gitbook/assets/1C1BDDA3-6EAD-4574-9AAD-3B1886C5298C_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
6.  In the **Cloud Tokens** section, click **Generate Cloud Token.**\\

    <figure><img src="../../.gitbook/assets/093ECA13-2ABE-4A8A-998D-6F6D2E0E5DF9_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
7.  In the **Copy your Cloud Token** pop-up window, click **Copy and Close**. \\

    \{% hint style="warning" %\} Store your Cloud token somewhere secure. \{% endhint %\}

    <figure><img src="../../.gitbook/assets/18A6E6CD-1BA0-466F-B858-BAB94225DA7E_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

    \### Verification

*   In the **Hybrid Gateway Details** screen, navigate to the **Cloud Tokens** section. The table shows the date and time that you created the Cloud token.\\

    <figure><img src="../../.gitbook/assets/A9D87A59-C9CE-42BC-9FF9-4AC06738C249_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

## Next steps

* (Optional) Link your Cloud token to a hybrid Gateway. For more information about linking to a hybrid Gateway, see [link-to-a-hybrid-gateway.md](link-to-a-hybrid-gateway.md "mention").
