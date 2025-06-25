# Hybrid Cloud reg and gateway deploy

### Hybrid Gateway Wizard

In this section, you can follow the steps to configure a Hybrid Gateway, and connect it to your Gravitee Cloud API Management control plane environment.

{% hint style="info" %}
You can deploy, run, and connect hybrid gateways according to your preference. To configure the hybrid gateways to your preferences, ensure that you provide your Cloud Token and License key.
{% endhint %}

1. On your Gravitee Cloud Dashboard, navigate to **Gateways**, and then click **Deploy Gateway**.

<figure><img src=".gitbook/assets/image (1) (1) (1).png" alt=""><figcaption><p>Gravitee Cloud Dashboard with no Gateways deployed.</p></figcaption></figure>

2. In the **Choose Gateway Deployment Method** pop-up window, select **Hybrid Gateway**.

<figure><img src=".gitbook/assets/image (1) (1) (1) (2).png" alt=""><figcaption><p>Gravitee Cloud Gateway deployment selection with both Gravitee Hosted Gateways (full SaaS) and Hybrid Gateways as options.</p></figcaption></figure>

3. From the **Platform** dropdown menu, select your preferred platform. This choice changes only the link reference to documentation
4. Select the Gravitee Cloud API Management Environment that you wish to connect the Hybrid gateway to.

<figure><img src=".gitbook/assets/image (270).png" alt=""><figcaption><p>Gravitee Cloud Hybrid Gateway set up guide with selection of platform and environment.</p></figcaption></figure>

5. In the **Access Point** field, type the name of your host or hosts that your Hybrid gateway will is accessible through. You configured this host in your load balancer or ingress where you run the gateway.\
   \
   In Gravitee Cloud, the full resolved URL based on your gateway host is referred to as an Access Point.\
   \
   By default, all URLs are enforcing HTTPS.
6. To retrieve your Cloud Token and License key, Click **Generate Installation Details**

<figure><img src=".gitbook/assets/image (3).png" alt=""><figcaption><p>The Deploy Hybrid Gateway screen where you should enter the gateway host that you hybrid gateway will listen to.</p></figcaption></figure>

7. Copy your Cloud Token, and then add it to your gateway deployment configuration (as described in step 9).
8. Copy your License, and then add it to your gateway deployment configuration (as described in step 9).

<figure><img src=".gitbook/assets/image (4).png" alt=""><figcaption><p>Gravitee Cloud Hybrid Gateway set up with last step where you are able to copy your generated Cloud Token and your License.</p></figcaption></figure>

10. Click **Return to Overview**. In the **Gateways** section of the **Overview** page, you can see your configured gateway.

<figure><img src=".gitbook/assets/image (6).png" alt=""><figcaption><p>Gravitee Cloud Dashboard, now with one hybrid gateway configuration added to Development environment.</p></figcaption></figure>
