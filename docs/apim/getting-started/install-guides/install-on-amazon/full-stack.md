# Quick Install

This is the fastest way to get Gravitee API Management (APIM) up and running on an Amazon instance.

## Prerequisites

{% hint style="warning" %}
Currently, Gravitee does not support the Amazon Linux 2023 image. Please select the Amazon Linux 2 image.
{% endhint %}

Provision and start an Amazon instance with the following minimum specifications:

* Instance Type: **t2.medium**
* Storage: Increase the root volume size to **40GB**
* Security Groups: **SSH** access is sufficient

## Security group

* open port 8082
* open port 8083
* open port 8084
* open port 8085

## Installation

1. Install all the prerequisites and Gravitee APIM components:

```sh
curl -L https://bit.ly/install-apim-3x | sudo bash
```

2. Verify:

```sh
sudo ss -lntp '( sport = 9200 )'

sudo ss -lntp '( sport = 27017 )'

sudo ss -lntp '( sport = 8082 )'

sudo ss -lntp '( sport = 8083 )'

sudo ss -lntp '( sport = 8084 )'

sudo ss -lntp '( sport = 8085 )'
```

You should see that there are processes listening on those ports.

3. Additional verification:

```sh
curl -X GET http://localhost:8082/

curl -X GET http://localhost:8083/management/organizations/DEFAULT/console

curl -X GET http://localhost:8083/portal/environments/DEFAULT/apis
```

If the installation was successful, then the first API call returns: **No context-path matches the request URI.** The final two API calls should return a JSON payload in the response.

{% hint style="success" %}
Congratulations, you have a fully functional Gravitee APIM!
{% endhint %}
