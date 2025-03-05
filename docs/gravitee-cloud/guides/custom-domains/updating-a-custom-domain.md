# Updating a custom domain

## Before you begin&#x20;

* You must have access to your domain registrar settings.

## Procedure

1. In the **Dashboard**, navigate to the **Gateways** section, and then click the hosted gateway that you want to reset the custom domain for.

<figure><img src="../../.gitbook/assets/image (30).png" alt=""><figcaption></figcaption></figure>

2. Click **Custom Domain**.&#x20;

<figure><img src="../../.gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>

3. Click **Reset**.

<figure><img src="../../.gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>

3. In the **Are you sure that you want to proceed?** pop-up window, type the custom domain.
4. Click **Reset Custom Domain**.
5. (Optional) If you do not plan to use the custom domain again, remove the CNAME record from your domain registrar.
6. In the **Custom Domain Name** field, type the new custom domain. For example, `dev.gateway.example.com`.

{% hint style="info" %}
Ensure that your organization owns and manages this domain.
{% endhint %}

<figure><img src="../../.gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>

5. In your domain registrar, create a CNAME record, and then point it to the current Gravitee-hosted gateway domain.
6. Click **Save**.&#x20;

<figure><img src="../../.gitbook/assets/image (33).png" alt=""><figcaption></figcaption></figure>
