---
description: >-
  This page describes you upgrade your API Management if you installed your API
  Management with RPM packages
---

# Upgrading with RPM packages

For versions 4.1.4 of Gravitee and above, you can upgrade and restart Gravitee API Management (APIM) to perform an RPM upgrade of the APIM components.

{% hint style="info" %}
Ensure that you are aware of any breaking changes and deprecated functionality. For more information about breaking changes and deprecated functionality, see [breaking-changes-and-deprecated-functionality-for-api-management.md](breaking-changes-and-deprecated-functionality-for-api-management.md "mention").
{% endhint %}

To upgrade your RPM installation, choose the upgrade process depending on your installation:

* [Upgrade the full APIM stack](upgrading-gravitee-api-management-installed-with-rpm-packages.md#upgrading-the-full-apim-stack). With this method, you upgrade all the Gravitee APIM components.
* [Upgrading Gravitee's API Management components individually](upgrading-gravitee-api-management-installed-with-rpm-packages.md#upgrading-gravitees-api-management-components-individually). With this method, you can upgrade only certain components.

## Upgrading the full APIM stack

* To upgrade your APIM installation, perform the package upgrade, and then restart APIM using the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-4x
sudo systemctl daemon-reload
sudo systemctl restart graviteeio-apim-gateway graviteeio-apim-rest-api nginx
```

## Upgrading Gravitee's API Management components individually

To upgrade an APIM component, you can perform a yum upgrade, and then restart the APIM component. You can upgrade the following components:

<details>

<summary>Upgrading the APIM Gateway package</summary>

* To upgrade the APIM Gateway package, use the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-gateway-4x
sudo systemctl restart graviteeio-apim-gateway
```

</details>

<details>

<summary>Upgrading the Management API package</summary>

* To upgrade the Management API package, use the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-rest-api-4x
sudo systemctl restart graviteeio-apim-rest-api
```

</details>

<details>

<summary>Upgrading the Management Console package</summary>

* To upgrade the Management Console package, use the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-management-ui-4x
sudo systemctl restart nginx
```

</details>

<details>

<summary>Upgrading the Developer Portal package</summary>

* To upgrade the Developer Portal package, use the following commands:&#x20;

```bash
sudo yum upgrade -y graviteeio-apim-portal-ui-4x
sudo systemctl restart nginx
```

</details>
