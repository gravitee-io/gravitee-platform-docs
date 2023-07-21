---
description: This page provides the technical details of the REST to SOAP policy
---

# REST to SOAP

## Overview

Functional and implementation information for the REST to SOAP policy is organized into the following sections:

* [Examples](template-policy-rework-structure-32.md#examples)
* [Configuration](template-policy-rework-structure-32.md#configuration)
* [Compatibility](template-policy-rework-structure-32.md#compatibility-matrix)
* [Changelogs](template-policy-rework-structure-32.md#changelogs)

## Examples

You can use the `rest-to-soap` policy to expose SOAP backend service as a REST API. The policy will pass the SOAP envelope message to the backend service as a POST request. SOAP envelopes support Expression Language to provide dynamic SOAP actions.

{% tabs %}
{% tab title="Proxy API example" %}
{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

For example, a SOAP API `http(s)://GATEWAY_HOST:GATEWAY_PORT/soap?countryName=France` with the following `rest-to-soap` policy SOAP envelope content:

```
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope\\\" xmlns:web=\\\"http://www.oorsprong.org/websamples.countryinfo">
   <soap:Header/>
   <soap:Body>
      <web:CountryISOCode>
         <web:sCountryName>{#request.params['countryName']}</web:sCountryName>
      </web:CountryISOCode>
   </soap:Body>
</soap:Envelope>
```

Will give you the ISO country code for `France`
{% endtab %}
{% endtabs %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"rest-to-soap": {
  "envelope": "<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:web="http://www.oorsprong.org/websamples.countryinfo">
                 <soap:Header/>
                 <soap:Body>
                    <web:ListOfCountryNamesByName/>
                 </soap:Body>
              </soap:Envelope>",
  "soapAction": null
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>SOAP Envelope</td><td>true</td><td></td><td>SOAP envelope used to invoke WS (supports Expression Language)</td><td></td></tr><tr><td>SOAP Action</td><td>false</td><td></td><td>'SOAPAction' HTTP header sent when invoking WS</td><td></td></tr><tr><td>Charset</td><td>false</td><td></td><td>This charset will be appended to the <code>Content-Type</code> header value</td><td></td></tr><tr><td>Preserve Query Parameters</td><td>false</td><td></td><td>Whether the query parameters are propagated to the backend SOAP service</td><td></td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the JSON-to-XML policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-rest-to-soap/blob/master/CHANGELOG.md" %}
