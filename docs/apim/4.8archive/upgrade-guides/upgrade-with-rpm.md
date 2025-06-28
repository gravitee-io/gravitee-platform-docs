# Upgrade with RPM

## Overview

This page describes how to upgrade your API Management if you installed your API Management with RPM packages.

For versions 4.1.4 of Gravitee and above, you can upgrade and restart Gravitee API Management (APIM) to perform an rpm upgrade of the APIM components.

{% hint style="info" %}
Refer to the Breaking changes and deprecated functionality to follow potential breaking changes.
{% endhint %}

To upgrade your RPM installation, choose the upgrade process depending on your installation:

* Upgrade the full APIM stack (includes all components)
* Upgrade components one-by-one

## Upgrade the full APIM stack

To upgrade your APIM installation, perform the package upgrade, and then restart APIM using the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-4x
sudo systemctl daemon-reload
sudo systemctl restart graviteeio-apim-gateway graviteeio-apim-rest-api nginx
```

## Upgrade the individual components

To upgrade an APIM component, you can perform a yum upgrade, and then restart the APIM. You can upgrade the following components:

### Upgrade the APIM Gateway package

To upgrade the APIM Gateway package, use the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-gateway-4x
sudo systemctl restart graviteeio-apim-gateway
```

### Upgrade the Management API package

To upgrade the Management API package, use the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-rest-api-4x
sudo systemctl restart graviteeio-apim-rest-api
```

### Upgrade the Management Console package

To upgrade the Management Console package, use the following commands:

```bash
sudo yum upgrade -y graviteeio-apim-management-ui-4x
sudo systemctl restart nginx
```

### Upgrade the Developer Portal package

```bash
sudo yum upgrade -y graviteeio-apim-portal-ui-4x
sudo systemctl restart nginx
```
