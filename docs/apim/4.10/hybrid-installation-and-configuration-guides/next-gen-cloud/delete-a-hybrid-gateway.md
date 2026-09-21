---
description: Delete a hybrid API Management 4.10 Gateway you no longer need to keep your environment controlled. Follow the steps to remove it.
metaLinks:
  alternates:
    - delete-a-hybrid-gateway.md
---

# Delete a Hybrid Gateway

## Overview

Deleting a hybrid Gateway is a way to maintain control and security within your environment. By removing connections that are no longer needed, you strengthen your security model, ensure that your system remains robust, and promote product maturity.

## Delete a hybrid Gateway

1.  Sign in to [Gravitee Cloud](https://cloud.gravitee.io/).

    <figure><img src="../../.gitbook/assets/hybrid-installation-and-configuration-gu-4-1-1-1-1 (1).png" alt="The Gravitee Cloud Sign in page, offering Google and Github sign-in above email and password fields and a company SSO link."><figcaption></figcaption></figure>
2.  Navigate to the **Gateways** section, and then click the Gateway that you want to delete.

    <figure><img src="../../.gitbook/assets/4F6BF985-5015-4CA0-ABA0-526FD7E1AC90_1_201_a.jpeg" alt="The Gateways table listing two hybrid Gateways, both showing a Never Connected status."><figcaption></figcaption></figure>
3.  In the **Hybrid Gateway Details** screen, navigate to the **General Details** section, and then click **Delete Hybrid Gateway**.

    <figure><img src="../../.gitbook/assets/D3015E55-B5A1-4A0F-9019-40F12F227506_1_201_a.jpeg" alt="The Hybrid Gateway Details page, with the name, type and environment above a Never Connected status and the Delete Hybrid Gateway button highlighted."><figcaption></figcaption></figure>
4.  In the **Delete Hybrid Gateway** pop-up window, type the name of the Gateway.

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>Deleting a gateway is permanent!</p></div>

    <figure><img src="../../.gitbook/assets/855489F0-7197-46F9-9878-78EDEDD0BF9D_1_201_a.jpeg" alt="The Delete Hybrid Gateway dialog warning that the operation is irreversible, with the Gateway name typed into the Confirm field."><figcaption></figcaption></figure>

    5\. Click \*\*Delete Hybrid Gateway\*\*.

## Verification

When you delete a hybrid Gateway, you receive the following message: "Gateway has been deleted."

<figure><img src="../../.gitbook/assets/hybrid-installation-and-configuration-gu-35-1 (1).png" alt="A green confirmation message reading Gateway has been deleted."><figcaption></figcaption></figure>

## Next steps

* (Optional) Link your hybrid deployment to a new hybrid Gateway. For more information about linking to a hybrid Gateway, see [link-to-a-hybrid-gateway.md](link-to-a-hybrid-gateway.md "mention").
