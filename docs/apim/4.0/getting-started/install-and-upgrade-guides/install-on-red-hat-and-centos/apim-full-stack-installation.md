# APIM Full Stack Installation

This section describes how to install the full Gravitee API Management (APIM) stack, including all the components and, optionally, dependencies (MongoDB, Elasticsearch).

Alternatively, you can install the APIM components individually as detailed on the [APIM Components page.](apim-components-installation.md)

## Prerequisites

Before you install the full APIM stack, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](README.md#configure-the-package-management-system-yum)
2. Install Nginx by running the following commands:

```sh
sudo yum install epel-release
sudo yum install nginx
```

## Install the APIM stack without dependencies

To install the APIM package only, run the following command:

```sh
sudo yum install graviteeio-apim-4x
```

## Install the APIM stack with dependencies

The following command installs both the APIM package and third-party repositories:

```sh
curl -L https://bit.ly/install-apim-4x | bash
```

## Run APIM with `systemd`

To start up the APIM components, run the following commands:

```sh
sudo systemctl daemon-reload
sudo systemctl start graviteeio-apim-gateway graviteeio-apim-rest-api
sudo systemctl restart nginx
```

## Check the APIM components are running

When all components are started, you can run a quick test by checking these URLs:

<table><thead><tr><th width="208">Component</th><th>URL</th></tr></thead><tbody><tr><td>APIM Gateway</td><td>http://localhost:8082/</td></tr><tr><td>APIM API</td><td>http://localhost:8083/management/organizations/DEFAULT/environments/DEFAULT/apis</td></tr><tr><td>APIM Management</td><td>http://localhost:8084/</td></tr><tr><td>APIM Portal</td><td>http://localhost:8085/</td></tr></tbody></table>

{% hint style="success" %}
Congratulations! Now that APIM is up and running, check out the [Quickstart Guide](../../quickstart-guide/README.md) for your next steps.
{% endhint %}

## Upgrade

To upgrade your APIM installation, perform the package upgrade and then restart APIM:

{% hint style="info" %}
For version 4.0.13 and above, upgrade and restart APIM to perform an `rpm` upgrade of APIM components.
{% endhint %}

{% hint style="warning" %}
Refer to the [changelog](../../../releases-and-changelog/changelog/apim-4.0.x.md) to follow potential breaking changes.
{% endhint %}

```sh
sudo yum upgrade -y graviteeio-apim-4x
sudo systemctl daemon-reload
sudo systemctl restart graviteeio-apim-gateway graviteeio-apim-rest-api nginx
```
