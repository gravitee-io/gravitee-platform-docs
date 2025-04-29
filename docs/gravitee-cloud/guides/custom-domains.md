---
description: >-
  This page describes how to configure a custom domain for Gravitee Hosted
  Gateways.
---

# Custom Domains

## Before you begin

* You must have a subscription to Gravitee Cloud. To register for a Gravitee Cloud account or to sign in to your Gravitee Cloud account, go to [Gravitee Cloud](https://eu-auth.cloud.gravitee.io/cloud/register?response_type=code\&client_id=fd45d898-e621-4b12-85d8-98e621ab1237\&state=TG15Ym11b3VBfkZFOC5yaEV5Lkp4QThYLnlxTS45R3lhYWRCVmxBemxSUWFH\&redirect_uri=https%3A%2F%2Feu.cloud.gravitee.io\&scope=openid+profile+email+offline_access\&code_challenge=AFIIIryTl43nsxq8cT-FTU9Umfp42j7jhJTeU2Y6vhE\&code_challenge_method=S256\&nonce=TG15Ym11b3VBfkZFOC5yaEV5Lkp4QThYLnlxTS45R3lhYWRCVmxBemxSUWFH\&hubspotutk=169d02e0ddc1d02ed3202bcac0869f20).
* You must deploy a Gravitee Hosted Gateway for at least one environment.
* You must have access to your domain registrar to register a CNAME record.

## Setting a custom domain

1. In the **Dashboard**, navigate to the **Gateways** section, and then click the hosted gateway that you want to change to a custom domain.&#x20;

<figure><img src="../.gitbook/assets/image (38).png" alt=""><figcaption><p>Gravitee Cloud account Dashboard page with one Gravitee Hosted Gateway deployed.</p></figcaption></figure>

2. Click the **Custom Domain** option in the Gateway details menu.

<figure><img src="../.gitbook/assets/image (39).png" alt=""><figcaption><p>Gravitee Hosted Gateway details view.</p></figcaption></figure>

3. In the **Custom Domain Name** field, type your desired custom domain. For example, `dev.gateway.example.com`.

<figure><img src="../.gitbook/assets/image (40).png" alt=""><figcaption><p>Custom domain settings where the custom domain has been set to api.johngren.org. </p></figcaption></figure>

4. In your domain registrar, create a CNAME record, and then point the CNAME record to the current Gravitee-hosted gateway domain. Once the CNAME record is created, it is forwarded to Gravitee.&#x20;

{% hint style="info" %}
You have to only forward the DNS record to Gravitee.
{% endhint %}

<figure><img src="../.gitbook/assets/image (41).png" alt=""><figcaption><p>Instructions on what needs to be configured in your domain registrar.</p></figcaption></figure>

### SSL Certificate

Once Gravitee has verified that traffic is forwarded with the CNAME record, Gravitee conducts an HTTP-01 challenge with Google CA to issue an SSL certificate for the domain. This procedure is to ensure you have https traffic on the gateway.\
\
Also, this procedure means that Gravitee ensures that your certificate is issued and updated continuously.

Depending on Google CA load, the issue of the certificate may take some time. You can visit the custom domain settings and refresh the status to know if the certificated has been issued.

## Verification

Once both CNAME and SSL certificate has been verified, you may now make API requests using the new custom domain.&#x20;

<figure><img src="../.gitbook/assets/image (43).png" alt=""><figcaption><p>Gravitee Hosted Gateway details page. Note that the Gateway URL is the custom domain configured.</p></figcaption></figure>

{% hint style="info" %}
The Gravitee provided Gateway URL still works. This URL acts as a backup in case your custom domain has issues. The URL ensures that the service is still available on Gravitee side.
{% endhint %}

## Resetting a custom domain

{% hint style="info" %}
If you reset your custom domain, the custom domain stops working and all configuration is deleted on Gravitee side.
{% endhint %}

If you wish to delete or update your custom domain, complete the following steps:

1. Visit the Custom Domain settings of the gateway,  and then select **Reset**.

<figure><img src="../.gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>

2. In the **Are you sure that you want to proceed?** pop-up window, type the custom domain.

<figure><img src="../.gitbook/assets/image (45).png" alt=""><figcaption><p>Resetting custom domain for Gravitee Hosted Gateway.</p></figcaption></figure>

2. Click **Reset Custom Domain**.
3. (Optional) If you do not plan to use the custom domain again, remove the CNAME record from your domain registrar.&#x20;
