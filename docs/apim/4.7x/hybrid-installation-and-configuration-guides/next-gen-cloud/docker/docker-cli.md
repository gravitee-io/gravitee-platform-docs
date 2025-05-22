# Docker CLI

## Prerequisites

Follow the instructions to [#prepare-your-installation](../#prepare-your-installation "mention").

## Install the Gateway

Run the following script:

```bash
docker run -d \
  --name gio-apim-hybrid-gateway \
  -p 8082:8082 \
  -e gravitee_ratelimit_type=none \
  -e gravitee_cloud_token=<cloud_token> \
  -e gravitee_license_key=<license_key> \
  graviteeio/apim-gateway:<CONTROL_PLANE_VERSION>
```

* Replace `<cloud_token>` and `<license_key>` with the Cloud token and license key from steps 7 and 8.
* Replace `<CONTROL_PLANE_VERSION>` with the version that is in the Environments section of your Gravitee Cloud dashboard.&#x20;

## Configure Redis

To enable API rate-limiting, configure your Gateway to use a rate-limiting repository, such as Redis.. For example, modify and run the following `docker run` command:

```bash
docker run -d \
  --name gio-apim-hybrid-gateway \
  -p 8082:8082 \
  -e gravitee_ratelimit_type=redis \
  -e gravitee_ratelimit_redis_host=redis \
  -e gravitee_ratelimit_redis_port=6379 \
  -e gravitee_ratelimit_redis_password=${redis_password} \
  -e gravitee_ratelimit_redis_ssl=false \
  -e gravitee_cloud_token=<cloud_token> \
  -e gravitee_license_key=<license_key> \
  graviteeio/apim-gateway:<CONTROL_PLANE_VERSION>
```

## Verification

From the Gravitee Cloud Dashboard, you can see your configured Gateway.

<figure><img src="../../../.gitbook/assets/image (6).png" alt=""><figcaption></figcaption></figure>

To verify that the Gateway is running, make a GET request to the URL on which you have published the Gateway. The output is a default message similar to:

```
No context-path matches the request URI.
```

You can now create and deploy APIs to your hybrid Gateway.
