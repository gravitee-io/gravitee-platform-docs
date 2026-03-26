---
description: Tutorial on APIM Components Installation.
---

# APIM Components Installation

This page describes how to install the individual components of the Gravitee API Management (APIM) stack.

* Install APIM Gateway
* Install Management API
* Install Management Console
* Install Developer Portal

## Install APIM Gateway

### Prerequisites

* Amazon instance running
* Gravitee `yum` repository added
* Java 17 JRE installed
* MongoDB installed and running
* ElasticSearch installed and running

### Security group

* Open port 8082

### Instructions

1. Install Gateway:

```sh
sudo yum install graviteeio-apim-gateway-4x -y
```

2. Enable Gateway on startup:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable graviteeio-apim-gateway
```

3. Start Gateway:

```sh
sudo systemctl start graviteeio-apim-gateway
```

4. Verify that, if any of the prerequisites are missing, you will receive errors during this step:

```sh
sudo journalctl -f
```

{% hint style="info" %}
You can see the same logs in `/opt/graviteeio/apim/gateway/logs/gravitee.log`
{% endhint %}

5. Additional verification:

```sh
sudo ss -lntp '( sport = 8082 )'
```

You should see that there’s a process listening on that port.

6. Final verification:

```sh
curl -X GET http://localhost:8082/
```

If the installation was successful, then this API call should return: **No context-path matches the request URI.**

## Install Management API

### Prerequisites

* Amazon instance running
* Gravitee `yum` repository added
* Java 17 JRE installed
* MongoDB installed and running
* ElasticSearch installed and running

### Security group

* Open port 8083

### Instructions

1. Install Management API:

```sh
sudo yum install graviteeio-apim-rest-api-4x -y
```

2. Enable Management API on startup:

```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable graviteeio-apim-rest-api
```

3. Start REST API:

```sh
sudo systemctl start graviteeio-apim-rest-api
```

4. Verify that, if any of the prerequisites are missing, you will receive errors during this step:

```sh
sudo journalctl -f
```

{% hint style="info" %}
You can see the same logs in `/opt/graviteeio/apim/rest-api/logs/gravitee.log`
{% endhint %}

5. Additional verification:

```sh
sudo ss -lntp '( sport = 8083 )'
```

You should see that there’s a process listening on that port.

6. Final verification:

```sh
$ curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
$ curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
```

If the installation was successful, then both of these API requests will return a JSON document.

## Install Management Console

### Prerequisites

* Amazon instance running
* Gravitee `yum` repository added
* Gravitee Management API installed and running
* Nginx installed

### Security group

* Open port 8084

### Instructions

1. Install Management Console:

```sh
sudo yum install graviteeio-apim-management-ui-4x -y
```

2. Restart Nginx:

```sh
sudo systemctl restart nginx
```

3. Verify:

```sh
sudo ss -lntp '( sport = 8084 )'
```

You should see that there’s a process listening on that port.

{% hint style="info" %}
**Management Console clarification**

The Management Console package does not provide its own service. It provides:

* a javascript application that can be found at `/opt/graviteeio/apim/management-ui`
* an Nginx configuration that can be found at `/etc/nginx/conf.d/graviteeio-apim-management-ui.conf`
{% endhint %}

## Install Developer Portal

### Prerequisites

* Amazon instance running
* Gravitee `yum` repository added
* Gravitee Management API installed and running
* Nginx installed

### Security group

* Open port 8085

### Instructions

1. Install Developer Portal:

```sh
sudo yum install graviteeio-apim-portal-ui-4x -y
```

2. Restart Nginx:

```sh
sudo systemctl restart nginx
```

3. Verify:

```sh
sudo ss -lntp '( sport = 8085 )'
```

You should see that there’s a process listening on that port.

{% hint style="info" %}
**Developer portal clarification**

The Developer Portal package does not provide its own service. It provides:

* a javascript application that can be found at `/opt/graviteeio/apim/portal-ui`
* an Nginx configuration that can be found at `/etc/nginx/conf.d/graviteeio-apim-portal-ui.conf`
{% endhint %}

{% hint style="success" %}
Congratulations! Now that APIM is up and running, check out the [Tutorials](README.md) for your next steps.
{% endhint %}
