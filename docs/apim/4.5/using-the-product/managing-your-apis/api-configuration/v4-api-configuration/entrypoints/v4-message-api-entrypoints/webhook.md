---
description: This page describes the configuration options of the Webhook entrypoint
---

# Webhook

## Configuration

If you chose **Webhook** as an entrypoint, you will be brought to a page where you can configure:

### **HTTP Options**

1. **Connect timeout:** The maximum time, in milliseconds, to connect to the Webhook. Either enter a numeric value or use the arrows to the right of the text field.
2. **Read timeout:** The maximum time, in milliseconds, allotted for the Webhook to complete the request (including response). Either enter a numeric value or use the arrows to the right of the text field.
3. **Idle timeout:** The maximum time, in milliseconds, a connection will stay in the pool without being used. Once this time has elapsed, the unused connection will be closed, freeing the associated resources. Either enter a numeric value or use the arrows to the right of the text field.

### **Proxy Options**

Use the drop-down menu to select a proxy option: **No proxy**, **Use proxy configured at system level**, or **Use proxy for client connections**. If you chose **Use proxy for client connections**, define the following settings:

1. **Proxy type:** Choose between **HTTP**, **SOCKS4** and **SOCKS5**. A [**SOCKS proxy**](https://hailbytes.com/how-to-use-socks4-and-socks5-proxy-servers-for-anonymous-web-browsing/) is a type of proxy server that uses the SOCKS protocol to tunnel traffic through an intermediary server.
2. **Proxy host:** Enter your proxy host in the text field.
3. **Proxy port:** Enter your proxy port in the text field.
4. (Optional) **Proxy username:** Enter your proxy username in the text field.
5. (Optional) **Proxy password:** Enter your proxy password in the text field.

### **Quality of service**

Use the drop-down menu to choose between the available options. QoS compatibility is detailed [here](docs/apim/4.5/using-the-product/managing-your-apis/api-configuration/v4-api-configuration/quality-of-service.md).

### **Dead Letter Queue**

Toggle **Dead Letter Queue** ON to define an external storage where each unsuccessfully pushed message will be stored and configure a replay strategy. Use the drop-down menu to select a pre-existing and supported endpoint or endpoint group to use for the DLQ.

## **DLQ Configuration using the API definition**

To configure DLQs and secure callbacks for your Webhook via the API definition:

### **1. Set up DLQ**

To enable DLQ, declare another endpoint that will be used to configure the DLQ object in the Webhook entrypoint definition:

```json
{
    "type": "webhook-advanced",
    "dlq": {
        "endpoint": "dlq-endpoint"
    },
    "configuration": {}
}
```

The endpoint used for the dead letter queue:

* Must support PUBLISH mode
* Should be based on a broker that can persist messages, such as Kafka

Once configured and deployed, any message rejected with a 4xx error response by the Webhook will be automatically sent to the DLQ endpoint and the consumption of messages will continue.

### **2. Set up secure callbacks**

Callbacks can be secured using basic authentication, JWT, and OAuth2.

To secure a callback, add an `auth` object to the configuration section of your API definition. The following example shows how to configure basic authentication:

```json
{
    "configuration": {
        "entrypointId": "webhook-advanced",
        "callbackUrl": "https://example.com",
        "auth": {
            "type": "basic",
            "basic": {
                "username": "username",
                "password": "a-very-secured-password"
            }
        }
    }
}
```

To use JWT, the `auth` object should look like this:

```json
        "auth": {
            "type": "token",
            "token": {
                "value": "eyJraWQiOiJk..."
            }
        }
```

To use OAuth2, the `auth` object should look like this:

```json
        "auth": {
            "type": "oauth2",
            "oauth2": {
                "endpoint": "https://auth.gravitee.io/my-domain/oauth/token",
                "clientId": "a-client-id",
                "clientSecret": "a-client-secret",
                "scopes": ["roles"]
            }
        }
```
