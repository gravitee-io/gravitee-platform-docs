---
description: An overview about enable the new developer portal.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/developer-portal/new-developer-portal/configure-the-new-portal
---

# Enable the New Developer Portal

{% hint style="warning" %}
This feature is in tech preview.
{% endhint %}

## Overview

The New Developer Portal has an updated interface and improved customization options. By default, Gravitee launches the Classic Developer Portal. But you can access, test, and preview the New Developer Portal using the API Management (APIM) Console. This does not change your default settings.

For self-hosted installations and hybrid deployments of Gravitee, you can set the New Developer Portal as the default experience by setting the appropriate configurations in your `docker-compose-apim.yml` file or `values.yaml` file. If you use Gravitee Cloud, and you want to set the New Developer Portal as the default experience, contact Gravitee.

## Enable the New Developer Portal

1.  From the **Dashboard**, click **Settings**.

    <figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>
2.  In the **Portal** section of the **Settings** menu, click **Settings**.

    <figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>
3.  Navigate to the **New Developer Portal** section, and then turn on the **Enable the New Developer Portal** toggle.

    <figure><img src="../../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>
4.  In the **You have unsaved changes** pop-up window, click **Save**.

    <figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

### Verification

*   Click the **Open Website** button. The New Developer Portal opens in a new tab.

    <figure><img src="../../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

## Set the New Developer Portal as default

To configure Gravitee to use the New Developer Portal by default, complete the following steps for your installation type:

{% tabs %}
{% tab title="Docker" %}
1. In your `docker-compose-apim.yml` file, you must set the following environment variables:
   1. Navigate to `management_ui`, and then set the following environment variable: `DEFAULT_PORTAL=next`.
   2. Navigate to `portal_ui`, and then set the following environment variable: `DEFAULT_PORTAL=next`.

Here is an example of the environmental variables set in a `docker-compose-apim.yml` file:

```yaml
  management_ui:
    image: graviteeio/apim-management-ui:${APIM_VERSION:-4}
    container_name: gio_apim_management_ui
    restart: always
    ports:
      - "8084:8080"
    depends_on:
      - management_api
    environment:
      - MGMT_API_URL=http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/
      - DEFAULT_PORTAL=next
    networks:
      - frontend

  portal_ui:
    image: graviteeio/apim-portal-ui:${APIM_VERSION:-4}
    container_name: gio_apim_portal_ui
    restart: always
    ports:
      - "8085:8080"
    depends_on:
      - management_api
    environment:
      - PORTAL_API_URL=http://localhost:8083/portal/environments/DEFAULT
      - DEFAULT_PORTAL=next
    networks:
      - frontend 
```

2.  Restart APIM using the following commands:

    ```bash
    docker compose -f docker-compose-apim.yml down
    docker compose -f docker-compose-apim.yml up -d
    ```
{% endtab %}

{% tab title="Kubernetes" %}
1.  In your `values.yml` file, navigate to the `portal` section, and then set `defaultPortal` to `"next"`:

    ```yaml
    portal:
      defaultPortal: "next"
      enabled: true
      ingressClassName: nginx
      scheme: http
      pathType: Prefix
      path: /portal
      hosts:
            - apim.localhost
      annotations:
        nginx.ingress.kubernetes.io/enable-cors: "true"
        nginx.ingress.kubernetes.io/cors-allow-origin: "*"
        nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"
        nginx.ingress.kubernetes.io/cors-allow-headers: "Authorization, Content-Type, X-Requested-With, Accept, Origin"
    ```
2.  Restart APIM using the following commands:

    ```bash
    helm upgrade gravitee-apim gravitee/apim \
      --namespace gravitee-apim \
      -f ./values.yaml
    ```
{% endtab %}

{% tab title="Cloud" %}
* To enable the New Developer Portal in your Gravitee Cloud account, Contact Gravitee.
{% endtab %}
{% endtabs %}

### Verification

*   In the APIM Console, click **Developer Portal**. The New Developer Portal opens in a new tab.

    <figure><img src="../../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

## Next Steps

* Customize your New Developer Portal. For more information about customizing your New Developer Portal, see [layout-and-theme.md](layout-and-theme.md "mention") and [customize-the-homepage.md](customize-the-homepage.md "mention").
