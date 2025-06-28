---
hidden: true
---

# WS Security Authentication

## Phase <a href="#user-content-phase" id="user-content-phase"></a>

| onRequestContent | onResponse |
| ---------------- | ---------- |
| X                |            |

## Description <a href="#user-content-description" id="user-content-description"></a>

You can use the `wssecurity-authentication` policy to manage security part from a soap call. The policy compares the username and password sent in the soap header to an APIM user to determine if the user credentials are valid.

To use the policy in an API, you need to:

* configure an LDAP, inline or http resource for your API plan, which specifies where the APIM users are stored
* configure a WS-Security authentication policy for the API flows

### Example <a href="#user-content-example" id="user-content-example"></a>

In the example below, the policy will extract **foo** & **bar** from the payload.

```
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Header>
        <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2003/06/secext">
            <wsse:UsernameToken>
                <wsse:Username>foo</wsse:Username>
                <wsse:Password>bar</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soap:Header>
    <soap:Body>
        ...
    </soap:Body>
</soap:Envelope>
```

{% hint style="info" %}
LDAP, inline and http resources are not part of the default APIM configuration, so you must download these resource plugins from [here](https://download.gravitee.io/#graviteeio-apim/plugins/resources/)
{% endhint %}

LDAP, inline and http resources are not part of the default APIM configuration, so you must download these resource plugins from [here](https://download.gravitee.io/#graviteeio-apim/plugins/resources/)

## Compatibility with APIM <a href="#user-content-compatibility-with-apim" id="user-content-compatibility-with-apim"></a>

| Plugin version | APIM version  |
| -------------- | ------------- |
| 1.x            | 3.x           |
| 2.x            | 4.0 and later |

## Configuration <a href="#user-content-configuration" id="user-content-configuration"></a>

The policy configuration is as follows:

| Property                | Description | Type            |
| ----------------------- | ----------- | --------------- |
| authenticationProviders |             | List of strings |
