---
description: Disconnect a Gravitee Cloud gateway from your private network from either details page. Follow the steps to disconnect it safely.
---

# Disconnect a Gateway from your private network

## Overview

You can disconnect your Gateway from your private network with Gravitee Cloud.

## Prerequisites

* Enable the private network feature. To enable the private network feature, contact your Gravitee representative. For example, your Technical Account Manager.
* Create a private network. For more information about creating a private network, see [create-a-private-network.md](create-a-private-network.md "mention").
* Deploy a Gateway with the GCP provider and in the same region as your Private Network.

## Disconnect a Gateway

You can disconnect a Gateway from your private network with either of the following methods:

* [#disconnect-a-gateway-from-the-network-details-page](disconnect-a-gateway-from-your-private-network.md#disconnect-a-gateway-from-the-network-details-page "mention")
* [#disconnect-the-gateway-from-the-private-network-details-page](disconnect-a-gateway-from-your-private-network.md#disconnect-the-gateway-from-the-private-network-details-page "mention")

### Disconnect a Gateway from the network details page

1.  From the **Dashboard**, click **Settings**.<br>

    <figure><img src="../../.gitbook/assets/guide-establish-private-networks-wi-20 (2).png" alt="The Gravitee Cloud dashboard Overview with Settings highlighted in the left navigation menu."><figcaption></figcaption></figure>
2.  From the **Settings** menu, click **Private Networks**.<br>

    <figure><img src="../../.gitbook/assets/guide-establish-private-networks-wi-27 (4).png" alt="The Account settings page with Private Networks highlighted in the Settings menu."><figcaption></figcaption></figure>
3. Navigate to the **Associated Gateways** section.
4.  Click the **X** associated with the Gateway that you want to disconnect from the private network.<br>

    <figure><img src="../../.gitbook/assets/guide-establish-private-networks-wi-16.png" alt="The Associated Gateways field highlighted, showing the Gateway chip and the X button that removes it."><figcaption></figcaption></figure>
5.  Click **Save**. Wait a few minutes for Gravitee to disconnect the Gateway.<br>

    <figure><img src="../../.gitbook/assets/77F37936-778C-44DC-BF21-D3FD86BB1C67_1_201_a.jpeg" alt="The empty Associated Gateways field with the Save button highlighted."><figcaption></figcaption></figure>

#### Verification

The Gateway does not appear in the list of the Associated Gateways.<br>

<figure><img src="../../.gitbook/assets/13116D58-A60B-4DA5-9A91-4CB6643071DC_1_201_a.jpeg" alt="The Private Network Settings page with the Associated Gateways field empty after the Gateway was disconnected."><figcaption></figcaption></figure>

### Disconnect the Gateway from the private network details page

1.  From the **Dashboard**, click the Gateway that you want to disconnect from the private Network.<br>

    <figure><img src="../../.gitbook/assets/9FD737AC-1DF2-48D7-A3B3-1439418167E2_1_201_a.jpeg" alt="The Dashboard with a Gateway name highlighted in the Gateways table."><figcaption></figcaption></figure>
2.  From the Gateway's menu, click **Network**.

    <figure><img src="../../.gitbook/assets/guide-establish-private-networks-wi-36.png" alt="The Gravitee Hosted Gateway page with Network highlighted in the Gateway menu."><figcaption></figcaption></figure>
3.  Click **Disconnect**. Wait a few minutes for the disconnection to complete.

    <figure><img src="../../.gitbook/assets/guide-establish-private-networks-wi-37.png" alt="The Network Settings page for a connected Gateway, with a Disconnect button in place of Connect."><figcaption></figcaption></figure>

#### Verification

The Gateway is removed from the **Private Network Settings** scree&#x6E;**.**

<figure><img src="../../.gitbook/assets/AE8FE10B-330E-4048-8061-87AAC7B08509_1_201_a.jpeg" alt="The Network Settings page after disconnecting, with the Private Network field empty and the Connect button disabled."><figcaption></figcaption></figure>
