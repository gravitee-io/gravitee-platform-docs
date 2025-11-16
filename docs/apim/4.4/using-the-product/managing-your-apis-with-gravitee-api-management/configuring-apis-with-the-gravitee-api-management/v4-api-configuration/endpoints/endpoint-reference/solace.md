---
description: This page contains the technical details of the Solace endpoint plugin
---

# Solace

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../../../../../overview/gravitee-apim-enterprise-edition/README.md)**.**
{% endhint %}

## Overview

Use this endpoint to publish and/or subscribe messages to a Solace broker.&#x20;

{% hint style="info" %}
Only SMF protocol is supported.
{% endhint %}

* [Compatibility matrix](solace.md#user-content-compatibility-matrix)
* [Endpoint identifier](solace.md#user-content-endpoint-identifier)
* [Endpoint configuration](solace.md#user-content-endpoint-configuration)

## Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version  |
| -------------- | ------------- |
| 1.x and up     | 4.x or higher |

## Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

To use this plugin, declare the following `solace` identifier while configuring your API endpoints.

## Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

#### **Endpoint-level configuration**

<table><thead><tr><th width="129">Attributes</th><th width="93">Default</th><th width="121">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>url</td><td>N/A</td><td>Yes</td><td>Define the URL of the Solace broker. Should begin with either <code>tcp://</code> or <code>tcps://</code> for SMF protocol.</td></tr><tr><td>vpnName</td><td>N/A</td><td>Yes</td><td>Virtual event broker to target</td></tr></tbody></table>

### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

#### **Security**

Security options are available under _security_ attribute.

#### **Authentication**

Available under `security.auth`:

<table><thead><tr><th width="132">Attributes</th><th width="98">Default</th><th width="123">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>username</td><td>N/A</td><td>No</td><td>The username to use for the authentication</td></tr><tr><td>password</td><td>N/A</td><td>No</td><td>The password to use for the authentication</td></tr></tbody></table>

#### **Consumer configuration**

<table><thead><tr><th width="131">Attributes</th><th width="90">Default</th><th width="116">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Enable or disable the consumer capability</td></tr><tr><td>topics</td><td>N/A</td><td>Yes</td><td>Refers to a list of UTF-8 strings to subscribe to</td></tr></tbody></table>

#### **Producer configuration**

<table><thead><tr><th width="131">Attributes</th><th width="95">Default</th><th width="118">Mandatory</th><th>Description</th></tr></thead><tbody><tr><td>enabled</td><td>false</td><td>No</td><td>Enable or disable the producer capability</td></tr><tr><td>topics</td><td>N/A</td><td>Yes</td><td>Refers to a list of UTF-8 strings used to publish incoming messages</td></tr></tbody></table>

### Examples <a href="#user-content-examples" id="user-content-examples"></a>

The example below shows a full Solace endpoint configuration:

```json
{
    "name": "default",
    "type": "solace",
    "weight": 1,
    "inheritConfiguration": false,
    "configuration": {
        "url": "tcp://localhost:55554",
        "vpnName": "default"
    },
    "sharedConfigurationOverride": {
        "consumer" : {
            "enabled": true,
            "topics": ["topic/subscribe"]
        },
        "producer" : {
            "enabled": true,
            "topics": ["topic/publish"]
        },
        "security" : {
            "auth": {
                "username": "user",
                "password": "password"
            }
        }
    }
}
```
