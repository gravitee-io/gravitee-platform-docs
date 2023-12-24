---
description: This page contains the technical details of the Solace endpoint plugin
---

# Solace

This is an Enterprise feature

### Description <a href="#user-content-description" id="user-content-description"></a>

This is a Solace endpoint which allow subscribing or publishing messages to a Solace broker. Note that only SMF protocol is supported.

### Compatibility matrix <a href="#user-content-compatibility-matrix" id="user-content-compatibility-matrix"></a>

| Plugin version | APIM version  |
| -------------- | ------------- |
| 1.x and upper  | 4.x or higher |

### Endpoint identifier <a href="#user-content-endpoint-identifier" id="user-content-endpoint-identifier"></a>

In order to use this plugin, you only have to declare the following identifier `solace` while configuring your API endpoints.

### Endpoint configuration <a href="#user-content-endpoint-configuration" id="user-content-endpoint-configuration"></a>

#### General configuration <a href="#user-content-general-configuration" id="user-content-general-configuration"></a>

**Endpoint level configuration**

| Attributes | Default | Mandatory | Description                                                                                    |
| ---------- | ------- | --------- | ---------------------------------------------------------------------------------------------- |
| url        | N/A     | Yes       | Define the url of Solace Broker Should start either by `tcp://` or `tcps://` for SMF protocol. |
| vpnName    | N/A     | Yes       | Virtual Event Broker to target.                                                                |

#### Shared Configuration <a href="#user-content-shared-configuration" id="user-content-shared-configuration"></a>

**Security**

Security options are available under _security_ attribute.

**Authentication**

Available under `security.auth` :

| Attributes | Default | Mandatory | Description                                 |
| ---------- | ------- | --------- | ------------------------------------------- |
| username   | N/A     | No        | The username to use for the authentication. |
| password   | N/A     | No        | The password to use for the authentication. |

**Consumer configuration**

| Attributes | Default | Mandatory | Description                                          |
| ---------- | ------- | --------- | ---------------------------------------------------- |
| enabled    | false   | No        | Allow enabling or disabling the consumer capability. |
| topics     | N/A     | Yes       | Refers to a list of UTF-8 string to subscribe to.    |

**Producer configuration**

| Attributes | Default | Mandatory | Description                                                         |
| ---------- | ------- | --------- | ------------------------------------------------------------------- |
| enabled    | false   | No        | Allow enabling or disabling the producer capability.                |
| topics     | N/A     | Yes       | Refers to a list of UTF-8 string used to publish incoming messages. |

#### Examples <a href="#user-content-examples" id="user-content-examples"></a>

Bellow you will find a full Solace endpoint configuration example:

```
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
