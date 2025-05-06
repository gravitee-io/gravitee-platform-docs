# REST to SOAP

## Overview

You can use the `rest-to-soap` policy to expose SOAP backend service as a REST API. The policy will pass the SOAP envelope message to the backend service as a POST request. SOAP envelopes support Expression Language to provide dynamic SOAP actions.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs and v4 HTTP proxy APIs. It cannot be applied to v4 message APIs or v4 TCP proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
A SOAP API `http(s)://GATEWAY_HOST:GATEWAY_PORT/soap?countryName=France` with the following `rest-to-soap` policy SOAP envelope content:

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope\\\" xmlns:web=\\\"http://www.oorsprong.org/websamples.countryinfo">
   <soap:Header/>
   <soap:Body>
      <web:CountryISOCode>
         <web:sCountryName>{#request.params['countryName']}</web:sCountryName>
      </web:CountryISOCode>
   </soap:Body>
</soap:Envelope>
```

Will give you the ISO country code for `France`.
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration is shown below:

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

### Phases

The phases checked below are supported by the `rest-to-soap` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

The `rest-to-soap` policy can be configured with the following options:

<table><thead><tr><th width="152">Property</th><th width="115" data-type="checkbox">Required</th><th width="126">Description</th><th width="278">Type</th><th>Default</th></tr></thead><tbody><tr><td>SOAP Envelope</td><td>true</td><td></td><td>SOAP envelope used to invoke WS (supports Expression Language)</td><td></td></tr><tr><td>SOAP Action</td><td>false</td><td></td><td>'SOAPAction' HTTP header sent when invoking WS</td><td></td></tr><tr><td>Charset</td><td>false</td><td></td><td>This charset will be appended to the <code>Content-Type</code> header value</td><td></td></tr><tr><td>Preserve Query Parameters</td><td>false</td><td></td><td>Whether the query parameters are propagated to the backend SOAP service</td><td></td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `rest-to-soap` policy:

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.x            | All                     |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-rest-to-soap/blob/master/CHANGELOG.md" %}
