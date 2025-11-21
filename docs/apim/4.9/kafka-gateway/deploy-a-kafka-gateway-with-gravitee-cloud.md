# Deploy a Kafka Gateway with Gravitee Cloud

## Overview

This guide explains how to use Gravitee Cloud to deploy a Gravitee Gateway that supports the Kafka protocol.

## Deploy a Kafka Gateway

1.  Sign in to [Gravitee Cloud](https://cloud.gravitee.io/).

    <figure><img src="../../4.8/.gitbook/assets/image (272) (1).png" alt=""><figcaption></figcaption></figure>
2.  From the **Dashboard**, navigate to the **Gateways** section, and then click **Deploy Gateway**.

    <figure><img src="../../4.8/.gitbook/assets/C1B3BA37-339C-4235-9592-B7EABB4DDA45_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3.  In the **Choose Gateway Deployment Method** pop-up window, select **Gravitee Hosted Gateway**, and then click **Next**.

    <figure><img src="../../4.8/.gitbook/assets/6C8CD77A-4C9A-4F45-B4BE-60573E916673_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
4.  In the **Choose Gateway Deployment Method** pop-up window, select the Gateway to deploy, and then select the service provider from the **Service Provider** drop-down menu.

    <figure><img src="../../4.8/.gitbook/assets/0A2F33F4-D84C-4808-BA20-482A2A658C77_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
5.  Click **Deploy**.

    <figure><img src="../../4.8/.gitbook/assets/DC3226E4-FF3B-43D8-93E3-28D878326053_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

## Verification

To verify that the Kafka Gateway deployed correctly, complete the following steps:

*   From the **Dashboard**, navigate to the **Gateways** section, and then confirm that the Gateway row entries are not greyed out and the Gateway name is an active link.

    <figure><img src="../../4.8/.gitbook/assets/image (303) (1).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
If the Gateway was not deployed correctly, the Gateway row entries are greyed out and the Gateway name is an inactive link.
{% endhint %}
