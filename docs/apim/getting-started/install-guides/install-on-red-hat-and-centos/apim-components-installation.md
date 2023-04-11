# APIM Components Installation

This section describes how to install the individual components from the Gravitee API Management (APIM) stack.

* [Install APIM Gateway](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_gateway.html)
* [Install APIM API](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_management\_api.html)
* [Install APIM Console](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_management\_ui.html)
* [Install APIM Portal](https://docs.gravitee.io/apim/3.x/apim\_installguide\_redhat\_portal.html)

Alternatively, you can install the full APIM stack and dependencies as detailed on the [Install the Full APIM Stack](install-the-full-apim-stack.md) page.

## Install APIM Gateway

### Prerequisites

The following steps assume you have configured your package management system as described in [Configure the package management system (yum).](./#configure-the-package-management-system-yum)

### Install the APIM Gateway package

To install the last stable version of the Gravitee API Management (APIM) Gateway, run the following command:

```sh
sudo yum install -y graviteeio-apim-gateway-3x
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

## Install Management API

### Prerequisites

The following steps assume you have configured your package management system as described in [Configure the package management system (yum).](./#configure-the-package-management-system-yum)

### Install the management API package

To install the last stable version of the management API, run the following command:

```sh
sudo yum install -y graviteeio-apim-rest-api-3x
```

### Run the management API

These steps assume that you are using the default settings.

To configure the management API to start automatically when the system boots up, run the following commands:

```sh
sudo systemctl daemon-reload

sudo systemctl enable graviteeio-apim-rest-api
```

To start and stop the management API, run the following commands:

```sh
sudo systemctl start graviteeio-apim-rest-api

sudo systemctl stop graviteeio-apim-rest-api
```

{% hint style="info" %}
These commands provide no feedback as to whether the management API started successfully. This information is written to the log files located in `/opt/graviteeio/apim/rest-api/logs/`.
{% endhint %}

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the management API service, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-rest-api
```

To list journal entries for the management API service starting from a given time, run the following command:

```sh
sudo journalctl --unit graviteeio-apim-rest-api --since  "2020-01-30 12:13:14"
```

## Install Management UI

### Prerequisites

Before you install the management UI, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](./#configure-the-package-management-system-yum)
2. Install and run the [management API](broken-reference).
3. Install Nginx by running the following commands:

```sh
sudo yum install epel-release

sudo yum install nginx
```

### Install the management UI package

To install the last stable version of the management UI, run the following command:

```sh
sudo yum install -y graviteeio-apim-management-ui-3x
```

### Run the management UI

{% hint style="info" %}
The management UI is based on Nginx.
{% endhint %}

To configure the management UI to start automatically when the system boots up, run the following commands:

```sh
sudo systemctl daemon-reload

sudo systemctl enable nginx
```

To start and stop Nginx, run the following commands:

```sh
sudo systemctl start nginx

sudo systemctl stop nginx
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

## Install Developer Portal

### Prerequisites

Before you install the developer portal, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](./#configure-the-package-management-system-yum)
2. Install and run the [management API](broken-reference).
3. Install Nginx by running the following commands:

```sh
sudo yum install epel-release

sudo yum install nginx
```

### Install the developer portal package

To install the last stable version of The developer portal , run the following command:

```sh
sudo yum install -y graviteeio-apim-portal-ui-3x
```

### Run the developer portal

{% hint style="info" %}
The developer portal is based on Nginx.
{% endhint %}

To configure the developer portal to start automatically when the system boots up, run the following commands:

```sh
sudo systemctl daemon-reload

sudo systemctl enable nginx
```

To start and stop Nginx, run the following commands:

```sh
sudo systemctl start nginx

sudo systemctl stop nginx
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

{% hint style="success" %}
Congratulations, you have a fully functional Gravitee APIM!
{% endhint %}

