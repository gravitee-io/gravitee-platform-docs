---
description: >-
  You install all the prerequisites that you need to run Gravitee’s API
  Management (APIM) and the full APIM stack.
---

# Installing Gravitee API Management on an Amazon instance with Quick install

## Before you begin

{% hint style="warning" %}
Gravitee supports only the Amazon Linux 2 image.
{% endhint %}

* Provision an Amazon instance, and then start the Amazon instance. Your Amazon instance must meet the following minimum requirements:
  * The instance type must be at least t2.medium.
  * The root volume size must be at least 40GB.
  * The security group must allow SSH connection to connect and install the Gravitee components.
  * The security group must be open to the following ports:
    * Port 8082
    * Port 8083
    * Port 8084
    * Port 8085

## Installating Gravitee API Management

* To install all the prerequisites that you need to run Gravitee APIM and Gravitee full APIM stack, use the following command:

```sh
curl -L https://bit.ly/install-apim-4x | sudo bash
```

### Verification

To verify that you installed Gravitee APIM correctly, complete the following steps:

1. Ensure that there are processes listening on the relevant ports using the following commands:

```sh
$ sudo ss -lntp '( sport = 9200 )'
$ sudo ss -lntp '( sport = 27017 )'
$ sudo ss -lntp '( sport = 8082 )'
$ sudo ss -lntp '( sport = 8083 )'
$ sudo ss -lntp '( sport = 8084 )'
$ sudo ss -lntp '( sport = 8085 )'
```

1. Send three API calls to ensure that you installed the APIM stack using the following sub-steps:

&#x20;       a.  Send a GET request using the following command:

```sh
$ curl -X GET http://localhost:8082/
```

{% hint style="info" %}
If you installed the APIM stack correctly, the API call returns the following message: No context-path matches the request URI’
{% endhint %}

&#x20;       b. Send two GET requests using the following commands:

```sh
$ curl -X GET http://localhost:8083/management/organizations/DEFAULT/console
$ curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
```

{% hint style="info" %}
If you installed the APIM stack correctly, both API calls return a JSON payload response.
{% endhint %}
