# Configure authentication with SSO

Overview

## Prerequisites&#x20;

* Install Self-Hosted Installation of Gravitee APIM or a Hybrid Installation of Gravitee APIM. For more information about installating Gravitee APIM, see [Broken link](/broken/pages/l3VTaBMjUvFd4jXfkLQh "mention") or [Broken link](/broken/pages/KmYIfcneJBExnYks77zr "mention").&#x20;
* Ensure that your installation of Gravitee APIM  is version 4.10 or later. For more information about upgrading Gravitee APIM, see [Broken link](/broken/pages/7anra8jO4R0or1MnFTlp "mention").
* Complete the steps in [Broken link](/broken/pages/5RELNfUmXNFFWCOkXm6g "mention").
* Configure one or more of the following identity providers:
  * [Broken link](/broken/pages/R3uvwQUXDXgfvEUeS7RJ "mention")
  * [Broken link](/broken/pages/J5VAAxGsY7INiOdPvoeo "mention")
  * [Broken link](/broken/pages/nje0QyKLNK99oeIcmZLz "mention")
  * [Broken link](/broken/pages/ge2IXPgfwdedGUXUkFE3 "mention")

## Configure authentication with SSO

To configure authentication with SSO, complete the following steps:

* [#activate-an-identity-provider-in-your-configuration-file](configure-authentication-with-sso.md#activate-an-identity-provider-in-your-configuration-file "mention")
* [#activate-an-identity-provider-in-the-apim-console](configure-authentication-with-sso.md#activate-an-identity-provider-in-the-apim-console "mention")

### Activate an identity provider in your configuration file

You can activate identity providers for specific environments so that they are available in your New Developer Portal. Follow the steps relevant to your installation method:

{% tabs %}
{% tab title="Docker" %}
1. In your `gravitee.yaml` file, navigate to the `security` section, and then add the following configuration:

```yaml
security:
  providers:
    - type: google
      activations:
        - "<ORGANIZATION_ID>:<ENVIRONMENT_ID>"
```

* Replace `<ORGANIZATION_ID>` with the id for your organization. The default value is `DEFAULT`.
* Replace `<ENVIRONMENT_ID>` with the id for your environment. The default value is `DEFAULT`.

2. (Optional) Set SSO only log in. To set SSO log in only, navigate to the navigate to the `portal` section, and then add the following configuration:

```yaml
portal:
  authentication:
    localLogin:
      enabled: false
```

3. Deploy your installation your installation with the new configuration using the following command:

```
docker compose down 
docker compose up 
```
{% endtab %}

{% tab title="Helm " %}
1. In your `values.yaml` file, navigate to the `security` section, and then add the following configuration

```yaml
security:
  providers:
    - type: google
      activations:
        - "ORGANIZATION_ID:ENVIRONMENT_ID"
```

* Replace `<ORGANIZATION_ID>` with the id for your organization. The default value is `DEFAULT`.
* Replace `<ENVIRONMENT_ID>` with the id for your environment. The default value is `DEFAULT`.

2. (Optional) Set SSO only log in. To set SSO log in only, navigate to the `api` section, and then add the following configuration:

```yaml
api:
  env:
    - name: gravitee_portal_authentication_locallogin_enabled
      value: "true"
```

3. Deploy your installation with your new configuration using the following command:

```
helm upgrade gravitee-apim gravitee/apim \
  --namespace gravitee-apim \
  -f ./values.yaml \
  --set 'portal.ingress.annotations.nginx\.ingress\.kubernetes\.io/rewrite-target=null' \
  --wait \
  --timeout 5m
```
{% endtab %}
{% endtabs %}

### Activate an identity provider in the APIM Console&#x20;

1.  From the **Dashboard**, click **Settings**. <br>

    <figure><img src=".gitbook/assets/FBF81839-15D7-4CC9-8ABC-BE5C51A3260A_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
2.  From the **Settings** menu, navigate to the **Portal** section, and then click **Authentication**.<br>

    <figure><img src=".gitbook/assets/211D2526-0572-46F5-881A-0C4012D772AD_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
3.  Turn on the SSO toggle that you want to activate.<br>

    <figure><img src=".gitbook/assets/8293D9DC-F869-443A-AA92-94FF405AA4DF_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
4.  (SSO only log in only) Turn off the **Show login form on Portal** toggle. <br>

    <figure><img src=".gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

### Verification

The Login screen for your New Developer Portal shows only SSO login.

<figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

## Next steps

* [Broken link](/broken/pages/dEbr8DOikUsbYrvRS8Ec "mention")
