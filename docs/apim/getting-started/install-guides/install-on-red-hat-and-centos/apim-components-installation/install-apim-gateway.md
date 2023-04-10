# Install APIM Gateway

## Prerequisites

The following steps assume you have configured your package management system as described in [Configure the package management system (yum).](../#configure-the-package-management-system-yum)

## Install the APIM Gateway package

To install the last stable version of the Gravitee API Management (APIM) Gateway, run the following command:

```sh
sudo yum install -y graviteeio-apim-gateway-3x
```

## Run APIM Gateway

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

## View the logs

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

\
