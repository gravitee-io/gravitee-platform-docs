---
description: >-
  This page explains how you expose SOAP webservices for REST-based client-side
  consumption using SOAP (XML) to REST (JSON) payload (using Gravitee Policies).
---

# Exposing SOAP webservices as REST APIs

## Introduction

You can use Gravitee to transform a SOAP-based endpoint, and then expose the endpoint as a REST (JSON) service.

This page explains how to transform an online SOAP service example (that converts the temperature from celisius to fahrenheit).&#x20;

Here is the SOAP Endpoint and the SOAPAction:

* SOAP Endpoint (POST):  [https://www.w3schools.com/xml/tempconvert.asmx](https://www.w3schools.com/xml/tempconvert.asmx)
* SOAPAction: [https://www.w3schools.com/xml/CelsiusToFahrenheit](https://www.w3schools.com/xml/CelsiusToFahrenheit)

Here is an example of using 'curl' to call the SOAP service:

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

The above command would return the following response:

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

## How to define the new JSON request payload using the Gravitee Policy studio

1. &#x20;The first step is to define what we want the new JSON request payload to look like.  Here is an example definition of our JSON request payload:

`{ “celsius” : <integer> }`

2. And of course, we need to define what we want the final JSON response to look like too. Here is an example of our JSON response:

`{ “result” : <integer> }`

### Creating a new Common Flow

Within your API's Policy Studio, create a new Common Flow. This flow must have a condition that it is only triggered if the request is of 'JSON' type.  A “Common Flow” isn’t tied to any individual plan, so it will be triggered (under the correct condition) regardless if you’ve secured your API with a keyless plan or JWT/OAuth.

1. To create a common flow:  Within your API's Policy Studio, create a new Common Flow (by clicking on the “**+**” button) ![](<../.gitbook/assets/image (61).png>)
2. Name the flow (e.g: JSON Request?) and specify the required condition (e.g: `{#request.headers['Content-Type'][0] == 'application/json'}`)

<figure><img src="../.gitbook/assets/image (62).png" alt="" width="375"><figcaption></figcaption></figure>

<figure><img src="https://lh7-eu.googleusercontent.com/docsz/AD_4nXfF5UqEzo1L_zOAQsayAgAwMQ0-eelFeDdHmGqYkdOj9QNYkeImgyURTeVR1nl7CiTfJ7TPhSsydJblCg87iDycAS3HnHtN6qgb8f5Cwa_aBc0NcyLOUvGLkrLzUTEawUdJXzbT1E5jdfJeewD6MgWd0fw?key=vP9tqrgkzZBD15oIdmy0HQ" alt=""><figcaption></figcaption></figure>

Now that our JSON-specific flow has been created, we can start our payload transformation steps, which will be as follows:

1. Request phase:
   * "REST to SOAP Transformer" policy
2. Response phase:
   * "XML to JSON" policy, and
   * "JSON to JSON Transformation" policy

### **Transforming the request payload**

The backend service is only SOAP. You must transform the incoming JSON request to a SOAP envelope.  You can use the “REST to SOAP Transformer” policy and pull in any JSON attributes from the request payload into the SOAP envelope.&#x20;

To transform the incoming JSON request to a SOAP envelope, complete these steps:

1. Within the Request phase, click the “**+**” button to add a new policy.
2. Select the “**REST to SOAP Transformer**” policy.
3. Specify the required SOAP envelope, and then use Gravitee’s Expression Language (EL) to dynamically insert the ‘Celsius’ value from the JSON request payload. Here is an example of the specification (notice the use of jsonPath to pull a specific attribute/value from the JSON request playload):

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

Here is an example of using the 'curl' command for this transformation:

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

### Payload Transforming the payload Response

We now need to transform the SOAP response into a JSON response, and then extract just the single \<CelsiusToFahrenheitResult> value (from the SOAP envelope).  In the “Response phase”, you can use the “XML to JSON” policy along with the “JSON to JSON Transformation” policy to accomplish this step.&#x20;

To transform the SOAP response into a JSON response, complete the following steps:

1. Add the “XML to JSON” policy - no further configuration is required.
2. Add the “JSON to JSON Transformation” policy, and define the JOLT specification for the transformation.  Here is my example:

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

* To test our API,  you now need to specify the “Content-Type” header with a value of “`application/json`”. Here is an example of the specification (and the new JSON response):

```
curl -L 'http://localhost:8082/tempconvert-v4' \
     -H 'Content-Type: application/json' \
     -d '{"celsius": 31}'

{"result":87.8}
```

### **(Optional) Validating the JSON request**

Best practice is to ensure the incoming JSON request actually matches our defined (and expected) payload. To validate the incoming JSON payload, complete the following steps:

1. Back in the "Request" phase (and before the “REST to SOAP Transformer” policy) click on the “+” button to add a new policy.  Select the “JSON Validation” policy.
2. Optionally, you can now specify a custom error message (if the request doesn't match our needed schema).
   * Example HTTP error message:  `Bad message.  You must provide the celsius key/value in JSON.  Example: { "celsius" : 20 }`
3. You must also specify the JSON Schema (that you want all incoming requests to comply to).  Here is an example to ensure the incoming request includes a JSON attribute called "celsius" and the value type must be an integer:

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

Finally, save and deploy your API.

#### Example of a bad request:

* This example is a bad request because “celsius” is misspelled:

```
curl -L 'http://localhost:8082/tempconvert-v4' \
     -H 'Content-Type: application/json' \
     -d '{"celsiusssss": 31}'


Bad request - you must provide the celsius key/value in JSON.  Example:  {"celsius" : 20}

```

**Example of a good request:**

* This is an example of a good request because the incoming JSON payload matches our defined JSON schema:

```
curl -L 'http://localhost:8082/tempconvert-v4' \
     -H 'Content-Type: application/json' \
     -d '{"celsius": 31}'


{"result":87.8}
```
