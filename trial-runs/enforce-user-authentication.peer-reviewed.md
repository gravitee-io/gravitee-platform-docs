# Enforce User Authentication

## Overview

You can enforce user authentication to access your New Developer Portal. This limits access to your New Developer Portal to authenticated users only.

## Prerequisites

* Install a self-hosted or hybrid installation of Gravitee APIM. For more information about installing Gravitee APIM, see [Broken link](/broken/pages/l3VTaBMjUvFd4jXfkLQh "mention") or [Broken link](/broken/pages/KmYIfcneJBExnYks77zr "mention").
* Ensure that your installation of Gravitee APIM is version 4.10 or later. For more information about upgrading Gravitee APIM, see [Broken link](/broken/pages/7anra8jO4R0or1MnFTlp "mention").
* Complete the steps in [Broken link](/broken/pages/5RELNfUmXNFFWCOkXm6g "mention").
* Complete the steps in [Broken link](/broken/pages/QIVgjPDwDCknL3JThS0H "mention") or [Broken link](/broken/pages/KOiAYXXzc0qOegMbiyLg "mention").

## Configure enforcing user authentication

To enforce user authentication, complete the following steps:

* [#configure-enforcing-user-authentication-in-your-configuration-file](enforce-user-authentication.md#configure-enforcing-user-authentication-in-your-configuration-file "mention")
* [#configure-enforcing-user-authentication-in-the-apim-console](enforce-user-authentication.md#configure-enforcing-user-authentication-in-the-apim-console "mention")

### Configure enforcing user authentication in your configuration file

{% tabs %}
{% tab title="Docker" %}
1.  In your `gravitee.yaml` file, navigate to the `portal` section, and then add the following configuration:<br>

    ```yaml
    portal:
      authentication:
        forceLogin:
          enabled: true
    ```
2.  Deploy your installation with your new configuration using the following command:<br>

    ```bash
    docker compose up -d 
    ```
{% endtab %}

{% tab title="Helm" %}
1.  In your `values.yaml` file, navigate to the `api` section, and then add the following configuration:<br>

    ```yaml
    api:
      env:
        - name: gravitee_portal_authentication_forcelogin_enabled
          value: "true"
    ```
2.  Deploy your installation with your new configuration using the following command: <br>

    ```bash
    helm upgrade gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./values.yaml \
      --set 'portal.ingress.annotations.nginx\.ingress\.kubernetes\.io/rewrite-target=null' \
      --wait \
      --timeout 5m
    ```
{% endtab %}
{% endtabs %}

### Configure enforcing user authentication in the APIM Console

1.  From the **Dashboard**, click **Settings**.<br>

    <figure><img src=".gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>
2.  In the **Settings** menu, navigate to the **Portal** section, and then click **Authentication**. <br>

    <figure><img src=".gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>
3.  Turn on the **Force authentication to access portal**.<br>

    <figure><img src=".gitbook/assets/C59621FB-6019-478F-BEB5-65646363CD72_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

## Verification

* Log out of your New Developer Portal, and then try to access a page on your New Developer Portal. You are redirected to the login screen. <br>

    <figure><img src=".gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>