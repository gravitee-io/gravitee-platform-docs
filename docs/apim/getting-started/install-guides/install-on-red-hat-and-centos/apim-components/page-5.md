# Install Management UI

## Prerequisites

Before you install the management UI, you must complete the following configuration.

1. Ensure you have configured your package management system, as described in [Configure the package management system (yum).](../#configure-the-package-management-system-yum)
2. Install and run the [management API](page-3.md).
3. Install Nginx by running the following commands:

```sh
sudo yum install epel-release

sudo yum install nginx
```

## Install the management UI package

To install the last stable version of the management UI, run the following command:

```sh
sudo yum install -y graviteeio-apim-management-ui-3x
```

## Run the management UI

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

## View the logs

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

\
