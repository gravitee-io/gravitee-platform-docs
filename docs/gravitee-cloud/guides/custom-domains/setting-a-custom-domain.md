# Setting a custom domain

## Before you begin

* You must have a Gravitee Cloud account. To register for a Gravitee Cloud account or to sign in to your Gravitee Cloud account, go to [Gravitee Cloud](https://eu-auth.cloud.gravitee.io/cloud/register?response_type=code\&client_id=fd45d898-e621-4b12-85d8-98e621ab1237\&state=TG15Ym11b3VBfkZFOC5yaEV5Lkp4QThYLnlxTS45R3lhYWRCVmxBemxSUWFH\&redirect_uri=https%3A%2F%2Feu.cloud.gravitee.io\&scope=openid+profile+email+offline_access\&code_challenge=AFIIIryTl43nsxq8cT-FTU9Umfp42j7jhJTeU2Y6vhE\&code_challenge_method=S256\&nonce=TG15Ym11b3VBfkZFOC5yaEV5Lkp4QThYLnlxTS45R3lhYWRCVmxBemxSUWFH\&hubspotutk=169d02e0ddc1d02ed3202bcac0869f20).

{% hint style="warning" %}
You set a custom domain with only a paid Gravitee Cloud account.
{% endhint %}

* You must have access to your domain registrar settings.

## Procedure

1. In the **Dashboard**, navigate to the **Gateways** section, and then click the hosted gateway that you want to change to a custom domain.&#x20;

<figure><img src="../../.gitbook/assets/image (30).png" alt=""><figcaption></figcaption></figure>

2. Click **Custom Domain**.

<figure><img src="../../.gitbook/assets/image (31).png" alt=""><figcaption></figcaption></figure>

3. In the **Custom Domain Name** field, type your desired custom domain. For example, `dev.gateway.example.com`.

{% hint style="info" %}
Ensure that your organization owns and manages this domain.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>

5. In your domain registrar, create a CNAME record, and then point it to the current Gravitee-hosted gateway domain.
6. Click **Save**.&#x20;

<figure><img src="../../.gitbook/assets/image (33).png" alt=""><figcaption></figcaption></figure>

## Verification

* You can access your APIs and Gateway through your custom domain.

