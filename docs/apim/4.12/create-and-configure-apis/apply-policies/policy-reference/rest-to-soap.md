---
description: An overview about rest to soap.
metaLinks:
  alternates:
    - rest-to-soap.md
---

# REST to SOAP

## Overview

You can use the Rest-to-soap policy to expose SOAP backend service as a REST API. The policy passes the SOAP envelope message to the backend service as a POST request. SOAP envelopes support Expression Language to provide dynamic SOAP actions.

### Automatic Application During WSDL Import

The REST-to-SOAP policy can be automatically applied when importing WSDL 1.1 documents to create v4 HTTP Proxy APIs. When enabled during WSDL import, the policy automatically converts incoming RESTful JSON requests to SOAP XML messages and transforms SOAP XML responses back to JSON. This transformation requires the `xml-json` policy as a dependency, which is automatically added when REST-to-SOAP is enabled.

#### Flow Generation Rules

When importing WSDL documents, flow generation behavior depends on the `withPolicies` parameter:

- When `withPolicies` is `null`, standard OpenAPI-derived flows are generated
- When `withPolicies` is an empty list (`[]`), no flows are generated (the API will have an empty flows array)
- When `withPolicies` contains `["rest-to-soap"]`, standard OpenAPI-derived flows are generated with REST-to-SOAP transformation policies applied

## Usage

For example, a SOAP API `http(s)://GATEWAY_HOST:GATEWAY_PORT/soap?countryName=France` with the following `rest-to-soap`policy SOAP envelope content:

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

Gives you the ISO country code for `France`.

## ⚠️ Security Warning: XML Injection Prevention

**Important**: When you use the REST-to-SOAP policy, you must be aware of potential XML injection vulnerabilities. User input embedded directly into SOAP envelopes without proper escaping might expose your API to security risks.

### Risk Example

For the following SOAP envelope property:

```xml
<soap:Envelope>
  <soap:Body>
    <web:getUserInfo>
      <web:id>{#request.params['userId']}</web:id>
    </web:getUserInfo>
  </soap:Body>
</soap:Envelope>
```

If user input contains XML-like content with the following url: `http(s)://GATEWAY_HOST:GATEWAY_PORT/soap?userId=1</web:id><web:id>2`

Without escaping, this might break your SOAP structure:

```xml
<soap:Envelope>
  <soap:Body>
    <web:getUserInfo>
      <web:id>1</web:id><web:id>2</web:id>  <!-- BROKEN XML! -->
    </web:getUserInfo>
  </soap:Body>
</soap:Envelope>
```

### Recommended Solution

Use the `#xmlEscape()` function in your EL expressions to safely escape user input:

```xml
<soap:Envelope>
  <soap:Body>
    <web:getUserInfo>
      <web:id>{#xmlEscape(#request.params['userId'])}</web:id>
    </web:getUserInfo>
  </soap:Body>
</soap:Envelope>
```

**Result:**

<pre><code><strong>&#x3C;web:id>1&#x26;lt;/web:id&#x26;gt;&#x26;lt;/web:id&#x26;gt;2&#x3C;/web:id>
</strong></code></pre>

## Best Practices

✅ Always use `{#xmlEscape()}` for user input in SOAP templates\
✅ Apply escaping to request parameters, headers, and body content\
✅ Consider using the `xml-threat-protection` policy for additional security\
❌ Never embed unescaped user input directly in XML/SOAP structures

## Phases

The `rest-to-soap` policy can be applied to the following API types and flow phases.

#### Compatible API types

* `PROXY`

#### Supported flow phases:

* Request

## Compatibility matrix

Strikethrough text indicates that a version is deprecated.

| Plugin version | APIM                   |
| -------------- | ---------------------- |
| 1.x            | All supported versions |

## Configuration options

| <p>Name<br><code>json name</code></p>                                | <p>Type<br><code>constraint</code></p> | Mandatory | Default | Description                                                                |
| -------------------------------------------------------------------- | -------------------------------------- | :-------: | ------- | -------------------------------------------------------------------------- |
| <p>Charset<br><code>charset</code></p>                               | string                                 |           |         | This charset will be appended to the Content-Type header value.            |
| <p>SOAP Envelope<br><code>envelope</code></p>                        | string                                 |     ✅     |         | SOAP envelope used to invoke WS. (support EL)                              |
| <p>Preserve Query Parameters<br><code>preserveQueryParams</code></p> | boolean                                |           |         | Define if the query parameters are propagated to the backend SOAP service. |
| <p>SOAP Action<br><code>soapAction</code></p>                        | string                                 |           |         | 'SOAPAction' HTTP header send when invoking WS.                            |
| <p>Strip path<br><code>stripPath</code></p>                          | boolean                                |           |         | Strip the path before propagating it to the backend SOAP service.          |

## Examples

_Proxy API With Defaults_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Rest to SOAP Transformer example API",
    "flows": [
      {
        "name": "Common Flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "STARTS_WITH"
          }
        ],
        "request": [
          {
            "name": "Rest to SOAP Transformer",
            "enabled": true,
            "policy": "rest-to-soap",
            "configuration":
              {
                "envelope": "<?xml version=\"1.0\"?>\n<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:web=\"http://www.oorsprong.org/websamples.countryinfo\"><soap:Header/><soap:Body><web:ListOfCountryNamesByName/></soap:Body></soap:Envelope>",
                "preserveQueryParams": false,
                "stripPath": false
              }
          }
        ]
      }
    ]
  }
}

```

_Proxy API on Request phase_

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "PROXY",
    "name": "Rest to SOAP Transformer example API",
    "flows": [
      {
        "name": "Common Flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "path": "/",
            "pathOperator": "STARTS_WITH"
          }
        ],
        "request": [
          {
            "name": "Rest to SOAP Transformer",
            "enabled": true,
            "policy": "rest-to-soap",
            "configuration":
              {
                "envelope": "<?xml version=\"1.0\"?>\n<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:web=\"http://www.oorsprong.org/websamples.countryinfo\"><soap:Header/><soap:Body><web:ListOfCountryNamesByName/></soap:Body></soap:Envelope>",
                "soapAction": "urn:MyAction",
                "charset": "UTF-8",
                "preserveQueryParams": true,
                "stripPath": false
              }
          }
        ]
      }
    ]
  }
}

```

## Changelog

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-rest-to-soap/blob/master/CHANGELOG.md" %}
