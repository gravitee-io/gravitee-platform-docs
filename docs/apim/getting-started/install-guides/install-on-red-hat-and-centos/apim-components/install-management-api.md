# Install Management API

## Prerequisites

The following steps assume you have configured your package management system as described in [Configure the package management system (yum).](../#configure-the-package-management-system-yum)

## Install the management API package

To install the last stable version of the management API, run the following command:

```sh
sudo yum install -y graviteeio-apim-rest-api-3x
```

## Run the management API

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

## View the logs

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

\
