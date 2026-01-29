# Install on Amazon

## Overview

This section explains how to install AM on Amazon Linux using the `yum` package manager.

## Prerequisites

First, you must configure the package management system (yum).

1.  Create a file called `graviteeio.repo` in location `/etc/yum.repos.d/` so that you can install AM directly using `yum`:

    ```
    [graviteeio]
    name=graviteeio
    baseurl=https://packagecloud.io/graviteeio/rpms/el/7/$basearch
    gpgcheck=0
    enabled=1
    gpgkey=https://packagecloud.io/graviteeio/rpms/gpgkey
    sslverify=1
    sslcacert=/etc/pki/tls/certs/ca-bundle.crt
    metadata_expire=300
    ```
2.  Enable GPG signature handling, which is required by some of our RPM packages:

    ```sh
    sudo yum install pygpgme yum-utils
    ```

    Before continuing, you may to refresh your local cache:

    ```sh
    sudo yum -q makecache -y --disablerepo='*' --enablerepo='graviteeio'
    ```

    Your repository is now ready to use.

## Installation Options

You can choose to install the full AM stack or install components individually:

* Install the full AM stack
* Components
  * Install AM Gateway
  * Install AM API
  * Install AM Console

## Install full AM stack

This section describes how to install the full AM stack, including all the components and, optionally, dependencies (MongoDB).

### Additional Prerequisites

Before you install the AM stack, you must complete the following configuration.

#### Install Nginx

To install Nginx, run the following commands:

```sh
$ sudo amazon-linux-extras install nginx1.12
$ sudo systemctl start nginx
```

### Install the AM package (no dependencies)

To install the AM package only, run the following command:

```sh
sudo yum install graviteeio-am-4x
```

### Install the AM package with dependencies

#### Configure dependency repositories

Before you install the AM package, you may need to add third-party repositories.

{% hint style="info" %}
For guidance on installing and configuring MongoDB, see the [MongoDB installation documentation](https://www.mongodb.com/docs/v4.4/tutorial/install-mongodb-on-red-hat/).
{% endhint %}

```
echo "[mongodb-org-4.4]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.4/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.4.asc" | sudo tee /etc/yum.repos.d/mongodb-org-4.4.repo > /dev/null

sudo yum install -y mongodb-org
sudo systemctl start mongod
```

#### Install AM

```sh
curl -L https://bit.ly/install-am-4x | bash
```

### Run AM with `systemd`

To start up the AM components, run the following commands:

```
$ sudo systemctl daemon-reload
$ sudo systemctl start graviteeio-am-4x-gateway graviteeio-am-4x-management-api
$ sudo systemctl restart nginx
```

### Check the AM components are running

When all components are started, you can do a quick test to see if everything is ok by checking these URLs:

| Component  | URL                   |
| ---------- | --------------------- |
| AM Gateway | http://localhost:8092 |
| AM API     | http://localhost:8093 |
| AM Console | http://localhost:8094 |

## Install AM Gateway

To install the latest stable version of AM Gateway, run the following command:

```sh
sudo yum install -y graviteeio-am-gateway-4x
```

### Run AM Gateway

These steps assume that you are using the default settings.

To configure AM Gateway to start automatically when the system boots up, run the following commands:

<pre class="language-sh"><code class="lang-sh"><strong>$ sudo systemctl daemon-reload
</strong>$ sudo systemctl enable graviteeio-am-gateway
</code></pre>

To start and stop AM Gateway, run the following commands:

```sh
$ sudo systemctl start graviteeio-am-gateway
$ sudo systemctl stop graviteeio-am-gateway
```

{% hint style="info" %}
These commands provide no feedback as to whether AM Gateway started successfully. This information is written to the log files located in `/opt/graviteeio/am/gateway/logs/`.
{% endhint %}

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the AM Gateway service, run the following command:

```sh
sudo journalctl --unit graviteeio-am-gateway
```

To list journal entries for the AM Gateway service starting from a given time, run the following command:

```sh
sudo journalctl --unit graviteeio-am-gateway --since  "2020-01-30 12:13:14"
```

## Install AM API

AM API is required to run AM Console. You must install AM API first before you can use AM Console.

### Install the AM API package

To install the latest stable version of AM API, run the following command:

```sh
sudo yum install -y graviteeio-am-management-api-4x
```

### Run AM API

These steps assume that you are using the default settings.

To configure AM API to start automatically when the system boots up, run the following commands:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable graviteeio-am-management-api
```

To start and stop AM API, run the following commands:

```sh
$ sudo systemctl start graviteeio-am-management-api
$ sudo systemctl stop graviteeio-am-management-api
```

{% hint style="info" %}
These commands provide no feedback as to whether AM API started successfully. this information will be written in the log files located in `/opt/graviteeio/am/management-api/logs/`.
{% endhint %}

### View the logs

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands.

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the AM API service, run the following command:

```sh
sudo journalctl --unit graviteeio-am-management-api
```

To list journal entries for the AM API service starting from a given time, run the following command:

```sh
sudo journalctl --unit graviteeio-am-management-api --since  "2020-01-30 12:13:14"
```

## Install AM Console

Before you install AM Console, you must ensure AM API is installed and running.

### Additional Prerequisites

Before you install the AM stack, you must complete the following configuration.

#### Install Nginx

To install Nginx, run the following commands:

<pre class="language-sh"><code class="lang-sh">$ sudo amazon-linux-extras install nginx1.12
<strong>$ sudo systemctl start nginx
</strong></code></pre>

### Install the AM Console package

To install the latest stable version of AM Console, run the following command:

```sh
sudo yum install -y graviteeio-am-management-ui
```

### Run AM Console

To configure AM Console to start automatically when the system boots up, run the following commands:

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

When `systemd` logging is enabled, the logging information is available using the `journalctl` commands:

To tail the journal, run the following command:

```sh
sudo journalctl -f
```

To list journal entries for the Nginx service, run the following command:

```sh
sudo journalctl --unit nginx
```

To list journal entries for the Nginx service starting from a given time:

```sh
sudo journalctl --unit nginx --since  "2020-01-30 12:13:14"
```
