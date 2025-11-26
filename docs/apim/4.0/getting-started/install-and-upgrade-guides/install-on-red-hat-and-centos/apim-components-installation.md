---
description: Tutorial on APIM Components Installation.
---

# APIM Components Installation

{% hint style="info" %}
**Gravitee dependencies**

Gravitee's [Installation & Upgrade Guides](../README.md) provide information on how to install Gravitee components. For prerequisite documentation on third-party products such as [MongoDB](https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-on-red-hat/) or [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/8.11/rpm.html), please visit their respective websites.
{% endhint %}

This section describes how to install the individual components from the Gravitee API Management (APIM) stack.

* [Install APIM Gateway](apim-components-installation.md#install-apim-gateway)
* [Install APIM API](apim-components-installation.md#install-management-api)
* [Install APIM Console](apim-components-installation.md#install-management-console)
* [Install APIM Portal](apim-components-installation.md#install-developer-portal)

Alternatively, you can install the full APIM stack and dependencies as detailed on the [Install the Full APIM Stack](apim-full-stack-installation.md) page.

## Install APIM Gateway

### Prerequisites

The following steps assume you have configured your package management system as described in [Configure the package management system (yum).](README.md#configure-the-package-management-system-yum)

### Install the APIM Gateway package

To install the last stable version of the Gravitee API Management (APIM) Gateway, run the following command:

```sh
sudo yum install -y graviteeio-apim-gateway-4x
```

### Run APIM Gateway

These steps assume that you are using the default settings.

To configure APIM Gateway to start automatically when the system boots up, run the following commands:

```sh
sudo systemctl daemon-reload
sudo systemctl enable graviteeio-apim-gateway
```

To start and stop APIM Gateway, run the following commands:

```sh
sudo systemctl start graviteeio-apim-gateway
sudo systemctl stop graviteeio-apim-gateway
```

{% hint style="info" %}
These commands provide no feedback as to whether APIM Gateway started successfully. This information is written to the log files located in `/opt/graviteeio/apim/gateway/logs/`.
{% endhint %}

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the APIM Gateway service, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-gateway
```

To list journal entries for the APIM Gateway service starting from a given time, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-gateway --since  "2020-01-30 12:13:14"
```

### Upgrade the APIM Gateway package

For version 4.0.13 and above, to upgrade an APIM component, you can perform a `yum` upgrade and restart APIM:

```sh
sudo yum upgrade -y graviteeio-apim-gateway-4x
sudo systemctl restart graviteeio-apim-gateway
```

## Install Management API

### Prerequisites

The following steps assume you have configured your package management system as described in [Configure the package management system (yum).](README.md#configure-the-package-management-system-yum)

### Install the Management API package

To install the last stable version of the management API, run the following command:

```sh
sudo yum install -y graviteeio-apim-rest-api-4x
```

### Run the management API

These steps assume that you are using the default settings.

To configure the Management API to start automatically when the system boots up, run the following commands:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable graviteeio-apim-rest-api
```

To start and stop the management API, run the following commands:

```sh
$ sudo systemctl start graviteeio-apim-rest-api
$ sudo systemctl stop graviteeio-apim-rest-api
```

{% hint style="info" %}
These commands provide no feedback as to whether the Management API started successfully. This information is written to the log files located in `/opt/graviteeio/apim/rest-api/logs/`.
{% endhint %}

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the Management API service, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-rest-api
```

To list journal entries for the Management API service starting from a given time, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-rest-api --since  "2020-01-30 12:13:14"
```

### Upgrade the Management API package

For version 4.0.13 and above, to upgrade an APIM component, you can perform a `yum` upgrade and restart APIM:

```sh
sudo yum upgrade -y graviteeio-apim-rest-api-4x
sudo systemctl restart graviteeio-apim-rest-api
```

## Install Management Console

### Prerequisites

Before you install the Management Console, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](README.md#configure-the-package-management-system-yum)
2. [Install and run the Management API.](apim-components-installation.md#install-management-api)
3. Install Nginx by running the following commands:

```sh
$ sudo yum install epel-release
$ sudo yum install nginx
```

### Install the Management Console package

To install the last stable version of the Management Console, run the following command:

```sh
$ sudo yum install -y graviteeio-apim-management-ui-4x
```

### Run the Management Console

{% hint style="info" %}
The Management Console is based on Nginx.
{% endhint %}

To configure the Management Console to start automatically when the system boots up, run the following commands:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable nginx
```

To start and stop Nginx, run the following commands:

```sh
$ sudo systemctl start nginx
$ sudo systemctl stop nginx
```

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the Nginx service, run the following command:

```sh
sudo journalctl --unit nginx
```

To list journal entries for the Nginx service starting from a given time, run the following command:

```sh
sudo journalctl --unit nginx --since  "2020-01-30 12:13:14"
```

### Upgrade the Management Console package

For version 4.0.13 and above, to upgrade an APIM component, you can perform a `yum` upgrade and restart APIM:

```sh
sudo yum upgrade -y graviteeio-apim-management-ui-4x
sudo systemctl restart nginx
```

## Install Developer Portal

### Prerequisites

Before you install the Developer Portal, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](README.md#configure-the-package-management-system-yum)
2. [Install and run the Management API.](apim-components-installation.md#install-management-api)
3. Install Nginx by running the following commands:

```sh
$ sudo yum install epel-release
$ sudo yum install nginx
```

### Install the Developer Portal package

To install the last stable version of The Developer Portal , run the following command:

```sh
sudo yum install -y graviteeio-apim-portal-ui-4x
```

### Run the Developer Portal

{% hint style="info" %}
The Developer Portal is based on Nginx.
{% endhint %}

To configure the Developer Portal to start automatically when the system boots up, run the following commands:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable nginx
```

To start and stop Nginx, run the following commands:

```sh
$ sudo systemctl start nginx
$ sudo systemctl stop nginx
```

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the Nginx service, run the following command:

```sh
sudo journalctl --unit nginx
```

To list journal entries for the Nginx service starting from a given time, run the following command:

```sh
sudo journalctl --unit nginx --since  "2020-01-30 12:13:14"
```

### Upgrade the Developer Portal package

For version 4.0.13 and above, to upgrade an APIM component, you can perform a `yum` upgrade and restart APIM:

```sh
sudo yum upgrade -y graviteeio-apim-portal-ui-4x
sudo systemctl restart nginx
```

{% hint style="success" %}
Congratulations! Now that APIM is up and running, check out the [Quickstart Guide](../../quickstart-guide/README.md) for your next steps.
{% endhint %}
