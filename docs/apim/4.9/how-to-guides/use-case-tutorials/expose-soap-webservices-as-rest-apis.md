# Expose SOAP Webservices as REST APIs

## Overview

You can use Gravitee to transform a SOAP-based endpoint, and then expose the endpoint as a REST (JSON) service.

This page explains how to transform an online SOAP service that converts the temperature from Celsius to Fahrenheit.

Here is the SOAP Endpoint and the SOAP Action:

* SOAP Endpoint (POST):  [https://www.w3schools.com/xml/tempconvert.asmx](https://www.w3schools.com/xml/tempconvert.asmx)
* SOAP Action: [https://www.w3schools.com/xml/CelsiusToFahrenheit](https://www.w3schools.com/xml/CelsiusToFahrenheit)

Here is an example using the `curl` command to call the SOAP service:

```
curl -L 'http://{Gravitee-APIM-Gateway-URL}/tempconvert-v4' \
     -H 'Content-Type: text/xml' \
     -H 'SOAPAction: https://www.w3schools.com/xml/CelsiusToFahrenheit' \
     -d '<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CelsiusToFahrenheit xmlns="https://www.w3schools.com/xml/">
      <Celsius>31</Celsius>
    </CelsiusToFahrenheit>
  </soap:Body>
</soap:Envelope>'
```

The command returns the following response:

```
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <CelsiusToFahrenheitResponse xmlns="https://www.w3schools.com/xml/">
      <CelsiusToFahrenheitResult>87.8</CelsiusToFahrenheitResult>
    </CelsiusToFahrenheitResponse>
  </soap:Body>
</soap:Envelope>
```

{% hint style="info" %}
**Gravitee notifications**

When you complete this payload/message transformation task, you can use Gravitee’s Notification feature to inform existing consumers that they can now use either SOAP or JSON.
{% endhint %}

## Defining the new JSON request payload using the Gravitee Policy studio

1. Define the new JSON request payload. Here is an example definition of a JSON request payload:

`{ “celsius” : <integer> }`

2. &#x20;Define the JSON response. Here is an example of the JSON response:

`{ “result” : <integer> }`

## Creating a new Common Flow

Within your API's Policy Studio, create a new Common flow. This flow must have a condition that it is triggered if the request is of only 'JSON' type.  A Common flow is not tied to any individual plan. Under the correct conditions, the common flow is triggered regardless if you have secured your API with a keyless plan or JWT/OAuth.

To create a Common flow, complete the following steps:&#x20;

1. Within your API's Policy Studio, navigate to **Common flows**, and then click the plus button.![](<../../.gitbook/assets/image (123).png>)
2. Name the flow. For example,JSON Request?
3. &#x20;Specify the required condition. For example,  `{#request.headers['Content-Type'][0] == 'application/json'}`.

<figure><img src="../../.gitbook/assets/image (124).png" alt="" width="375"><figcaption></figcaption></figure>

## Transforming the payload

When you create the JSON-specific flow, you transform your payload. To transform your payload, you must complete the following actions:

1. [Transform the request payload](expose-soap-webservices-as-rest-apis.md#transforming-the-request-payload)
2. [Transform the payload response](expose-soap-webservices-as-rest-apis.md#transforming-the-payload-response)

### **Transforming the request payload**

The backend service is only SOAP. You must transform the incoming JSON request to a SOAP envelope. You can use the “REST to SOAP Transformer” policy to pull in any JSON attributes from the request payload into the SOAP envelope.&#x20;

To transform the incoming JSON request to a SOAP envelope, complete these steps:

1. Within the Request phase, click the “**+**” button to add a new policy.
2. Select the “REST to SOAP Transformer” policy.
3. Specify the required SOAP envelope, and then use Gravitee’s Expression Language (EL) to dynamically insert the ‘Celsius’ value from the JSON request payload. Here is an example of the specification:

```bash
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CelsiusToFahrenheit xmlns="https://www.w3schools.com/xml/">
      <Celsius>{#jsonPath(#request.content, '$.celsius')}</Celsius>
    </CelsiusToFahrenheit>
  </soap:Body>
</soap:Envelope>
```

4. Specify the required SOAP Action. Here is an example of the SOAP Action: `https://www.w3schools.com/xml/CelsiusToFahrenheit`

#### Verification

To verify that you can transform an incoming JSON request to the required SOAP envelope, complete the following steps:

1. Save the Flow.
2. Click the **Deploy API** button. The system pushes the configuration to the API Gateway.

Here is an example of using the `curl` command for this transformation:

```
curl -L 'http://localhost:8082/tempconvert-v4' \
     -H 'Content-Type: application/json' \
     -d '{"celsius": 31}'

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <CelsiusToFahrenheitResponse xmlns="https://www.w3schools.com/xml/">
      <CelsiusToFahrenheitResult>87.8</CelsiusToFahrenheitResult>
    </CelsiusToFahrenheitResponse>
  </soap:Body>
</soap:Envelope>
```

### Transforming the payload response

You must transform the SOAP response into a JSON response, and then extract just the single \<CelsiusToFahrenheitResult> value from the SOAP envelope.  In the “Response phase”, you can use the “XML to JSON” policy and the “JSON to JSON Transformation” policy to complete the transformation.&#x20;

To transform the SOAP response into a JSON response, complete the following steps:

1. Add the “XML to JSON” policy.
2. Add the “JSON to JSON Transformation” policy, and define the JOLT specification for the transformation.  Here is an example: of the JOLT specification:

```json
[
  {
    "operation": "shift",
    "spec": {
      "soap:Envelope": {
        "soap:Body": {
          "CelsiusToFahrenheitResponse": {
            "CelsiusToFahrenheitResult": "result"
          }
        }
      }
    }
  }
]
```

3. Click **Save** and **Deploy** **API**.

### Testing the API

* To test your API, specify the “Content-Type” header with a value of “`application/json`”. Here is an example of the specification and the new JSON response:

```
curl -L 'http://localhost:8082/tempconvert-v4' \
     -H 'Content-Type: application/json' \
     -d '{"celsius": 31}'

{"result":87.8}
```

### **(Optional) Validating the JSON request**

You must ensure that the incoming JSON request actually matches our defined payload. To validate the incoming JSON payload, complete the following steps:

1. In the "Request" phase and before you add the “REST to SOAP Transformer” policy, click on the “+” button to add a new policy. &#x20;
2. Select the “JSON Validation” policy.
3. (Optional) Specify a custom error message. Here is an example HTTP  error message:  `Bad message.  You must provide the celsius key/value in JSON.  Example: { "celsius" : 20 }`
4. Specify the JSON Schema that you want all incoming requests to comply to. Here is an example JSON schema:

```
{ 
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "celsius": {
      "type": "integer"
    }
  },
  "required": [
    "celsius"
  ]
}
```

5. Save and deploy your API.

#### Request examples

Here are examples of a bad request and a good request

#### Example of a bad request

* This example is a bad request because “celsius” is misspelled.

```
curl -L 'http://localhost:8082/tempconvert-v4' \
     -H 'Content-Type: application/json' \
     -d '{"celsiusssss": 31}'


Bad request - you must provide the celsius key/value in JSON.  Example:  {"celsius" : 20}

```

**Example of a good request**

* This example is good request because the incoming JSON payload matches the defined JSON schema:

```
curl -L 'http://localhost:8082/tempconvert-v4' \
     -H 'Content-Type: application/json' \
     -d '{"celsius": 31}'


{"result":87.8}
```
