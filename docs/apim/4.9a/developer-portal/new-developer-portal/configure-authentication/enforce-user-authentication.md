# Enforce User Authentication

## Overview&#x20;

You can enforce user authentication to access your New Developer Portal. This limits access to your New Developer Portal to authenticated users only.

## Prerequisites&#x20;

* Install a self-hosted or hybrid instance of Gravitee APIM. For more information about installing Gravitee APIM, see [self-hosted-installation-guides](../../../self-hosted-installation-guides/ "mention") or [hybrid-installation-and-configuration-guides](../../../hybrid-installation-and-configuration-guides/ "mention").&#x20;
* Ensure that your installation of Gravitee APIM is version 4.10 or later. For more information about upgrading Gravitee APIM, see [upgrade-guides](../../../upgrade-guides/ "mention").
* Complete the steps in [configure-the-new-portal.md](../configure-the-new-portal.md "mention").
* Complete the steps in [configure-authentication-with-login-and-password.md](configure-authentication-with-login-and-password.md "mention") or [configure-authentication-with-sso.md](configure-authentication-with-sso.md "mention").

## Enforce user authentication&#x20;

To enforce user authentication, complete the following steps:&#x20;

* [#enforce-user-authentication-via-your-configuration-file](enforce-user-authentication.md#enforce-user-authentication-via-your-configuration-file "mention")
* [#enforce-user-authentication-via-the-apim-console](enforce-user-authentication.md#enforce-user-authentication-via-the-apim-console "mention")

### Enforce user authentication via your configuration file&#x20;

{% tabs %}
{% tab title="Docker" %}
1.  In your `gravitee.yaml` file, navigate to the `portal` section, and then add the following configuration:

    ```yaml
    portal:
      authentication:
        forceLogin:
          enabled: true
    ```
2.  Deploy your installation with your new configuration using the following command:

    ```bash
    docker compose up -d 
    ```
{% endtab %}

{% tab title="Helm" %}
1.  In your `values.yaml` file, navigate to the `api` section, and then add the following configuration:

    ```yaml
    api:
      env:
        - name: gravitee_portal_authentication_forcelogin_enabled
          value: "true"
    ```
2.  Deploy your installation with your new configuration using the following command:&#x20;

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

### Enforce user authentication via the APIM Console&#x20;

1.  From the **Dashboard**, click **Settings**.

    <figure><img src="../../../.gitbook/assets/image (116).png" alt=""><figcaption></figcaption></figure>
2.  In the **Settings** menu, navigate to the **Portal** section, and then click **Authentication**.&#x20;

    <figure><img src="../../../.gitbook/assets/image (117).png" alt=""><figcaption></figcaption></figure>
3.  Turn on **Force authentication to access portal**.

    <figure><img src="../../../.gitbook/assets/C59621FB-6019-478F-BEB5-65646363CD72_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

## Verification&#x20;

*   Log out of your New Developer Portal, and then try to access a page on your New Developer Portal. You are redirected to the login screen. <br>

    <figure><img src="../../../.gitbook/assets/image (119).png" alt=""><figcaption></figcaption></figure>
