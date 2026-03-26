# Connect a Gateway to your private network

## Overview&#x20;

You can disconnect your Gateway from your private network with Gravitee Cloud.

## Prerequisites&#x20;

* Enable the private network feature. To enable the private network feature, contact your Gravitee representative. For example, your Technical Account Manager.&#x20;
* Create a private network. For more information about creating a private network, see [create-a-private-network.md](create-a-private-network.md "mention").
* Deploy a Gateway with the GCP provider and in the same region as your private network. For more information about deploying a Gateway see [gravitee-hosted-gateways](../gravitee-hosted-gateways/ "mention").

## Connect a Gateway&#x20;

You can connect a Gateway to your private network with either of the following methods:&#x20;

* [#connect-a-gateway-from-the-network-details-page](connect-a-gateway-to-your-private-network.md#connect-a-gateway-from-the-network-details-page "mention")
* [#connect-a-gateway-from-the-private-network-detail-page](connect-a-gateway-to-your-private-network.md#connect-a-gateway-from-the-private-network-detail-page "mention")

### Connect a Gateway from the network details page

1.  From the **Dashboard**, click **Settings**. <br>

    <figure><img src="../../.gitbook/assets/image (29).png" alt=""><figcaption></figcaption></figure>
2.  From the **Settings** menu, click **Private Networks**.<br>

    <figure><img src="../../.gitbook/assets/image (30).png" alt=""><figcaption></figcaption></figure>
3.  Click the **name of the private network** that you want to add a Gateway to.<br>

    <figure><img src="../../.gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>
4. Navigate to the **Associated Gateways** section.
5.  Type the name of the Gateway, and then click the name of the Gateway from the list. <br>

    <figure><img src="../../.gitbook/assets/A521A0CB-B8E0-4A26-8C76-FFCD344E6203_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
6.  Click **Save**. Wait a few minutes for Gravitee to establish the connection. <br>

    <figure><img src="../../.gitbook/assets/A521A0CB-B8E0-4A26-8C76-FFCD344E6203_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

#### Verification

The Gateway appears in the list of the Associated Gateways.<br>

<figure><img src="../../.gitbook/assets/632F93FD-1438-48BB-99FE-42575D373F13_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

### Connect a Gateway from the private network detail page

1.  From the **Dashboard**, click the Gateway that you want to add to the private network.<br>

    <figure><img src="../../.gitbook/assets/6D751039-69AC-44F1-8D85-AA99C13A9A35_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
2.  From the Gateway's menu, click **Network**. <br>

    <figure><img src="../../.gitbook/assets/7EB4A4F7-3FB0-4073-A24B-18EDA82C2CCE_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
3.  From the **Private Network** drop-down menu, select the private network that you want to add the Gateway to.<br>

    <figure><img src="../../.gitbook/assets/3279A1D9-8144-41BA-9FBD-991E703CB7A3_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
4.  Click **Connect**. <br>

    <figure><img src="../../.gitbook/assets/3390D31E-623A-40BA-ABDA-C9C4CAA3235D_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

#### Verification&#x20;

The **Connect** button changes to a **Disconnect** button.

<figure><img src="../../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

## Next steps&#x20;

* (Optional) [disconnect-a-gateway-from-your-private-network.md](disconnect-a-gateway-from-your-private-network.md "mention").
