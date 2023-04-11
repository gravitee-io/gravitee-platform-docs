# APIM Components Installation

This section describes how to install the individual components from the Gravitee API Management (APIM) stack.

* Install APIM gateway
* Install management API
* Install management UI
* Install developer portal

Alternatively, you can install the full APIM stack and dependencies as detailed on the [APIM Full Stack Installation page.](gravitee-components/)

## Install APIM Gateway

### Prerequisites

* Amazon instance running
* Gravitee `yum` repository added
* Java 11 JRE installed
* MongoDB installed and running
* Elasticsearch installed and running

### Security group

* open port 8082

### Instructions

1. Install gateway:

```sh
sudo yum install graviteeio-apim-gateway-3x -y
```

2. Enable gateway on startup:

```sh
sudo systemctl daemon-reload

sudo systemctl enable graviteeio-apim-gateway
```

3. Start gateway:

```sh
sudo systemctl start graviteeio-apim-gateway
```

4. Verify, if any of the prerequisites are missing, you will receive errors during this step:

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



\
