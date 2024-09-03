---
description: >-
  Expose SOAP webservices as REST APIs This article walks through how to expose
  SOAP webservices for REST-based client-side consumption via SOAP (XML) to REST
  (JSON) payload/Message Transformation Intro
---

# Expose SOAP webservices as REST APIs

## Introduction

SOAP (XML) and REST (JSON) are dominant models when it comes to web services, and whilst developers standardized on SOAP (XML) in the past, REST (JSON) has become the modern model as it is easier to understand and has a much smaller payload size.

In this article, I’ll describe how you can use Gravitee to transform (request and response) payloads as they pass through the API Gateway, to specifically update a SOAP-based endpoint and expose it as a REST (JSON) service to existing consumers.

## What do I have today?

For demonstration purposes I’m using an online SOAP service that simply converts the temperature from celsius to fahrenheit:

SOAP Endpoint (POST):  [https://www.w3schools.com/xml/tempconvert.asmx](https://www.w3schools.com/xml/tempconvert.asmx)

SOAPAction: https://www.w3schools.com/xml/CelsiusToFahrenheit

<figure><img src="https://lh7-eu.googleusercontent.com/docsz/AD_4nXdZJyFn1ecdYMlZJMJ2sBLjuuG0BtIoHJWspBbzHI9ZiXgIlzZLPBZqIBXeoMOZpKslOWxZlMwwmkINzSTmQen5lPrA-MpnQ5CSiJDBnGeb7UQEes8tOu8JShXiA__zI52LjvCvjsHMDzDnGTk0JkK8Bj6x?key=vP9tqrgkzZBD15oIdmy0HQ" alt=""><figcaption></figcaption></figure>

I have already created this API in Gravitee, and it operates successfully as you’d expect:

<figure><img src="https://lh7-eu.googleusercontent.com/docsz/AD_4nXePwUGXu8zwlvSFrweeLxrQJOISQPU-7PE5OKlPk_AQEki6Ky2-yLaMs5gIv0Wnt6RslNRN_l0lID89U-uWbrJctdvnimgBmvhuc1z1RrnzCGUbtMOr3pKUIH-Kw58GFtlRoAMrIGzG0JWuYbHIA4VBGdpp?key=vP9tqrgkzZBD15oIdmy0HQ" alt=""><figcaption></figcaption></figure>

```
curl -L 'http://localhost:8082/tempconvert-v4' -H 'Content-Type: text/xml' -H 'SOAPAction: https://www.w3schools.com/xml/CelsiusToFahrenheit' -d '<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CelsiusToFahrenheit xmlns="https://www.w3schools.com/xml/">
      <Celsius>31</Celsius>
    </CelsiusToFahrenheit>
  </soap:Body>
</soap:Envelope>'

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <CelsiusToFahrenheitResponse xmlns="https://www.w3schools.com/xml/">
      <CelsiusToFahrenheitResult>87.8</CelsiusToFahrenheitResult>
    </CelsiusToFahrenheitResponse>
  </soap:Body>
</soap:Envelope>

```

## What do I want tomorrow?

But times have changed, and I would now like to expose this (SOAP) service as a REST API - using a JSON payload for both the request and response.

What’s also important is that existing consumers should be able to continue to use this API as a SOAP service (in parallel with it also accepting JSON requests). &#x20;

{% hint style="info" %}
**Gravitee notifications**

Once we have completed this payload/message transformation task, we can use Gravitee’s Notification feature to inform existing consumers they now have the choice of using either SOAP or JSON.
{% endhint %}

Let’s look at Gravitee’s Policy Studio where I can transform both the request and response.

## How to do it? The Gravitee Policy Studio

First of all, we need to define what the new JSON request payload should look like.  We don’t want anything as long or as complicated as the original SOAP envelope, so I’ve kept this really short and simple:

`{ “celsius” : <integer> }`

And the JSON response should be short and simple too:

`{ “result” : <integer> }`

### Create a new Flow

The first step is to create a new (Common) Flow that has a condition so that it is only triggered if the request is of JSON content.  A “Common Flow” isn’t tied to any individual plan, so it will be triggered (under the correct condition) regardless if you’ve secured your API with a keyless plan or JWT/OAuth.

I’ve named this flow “JSON Request?” and set the condition to check if the “Content-Type” request headers specify “application/json”

<figure><img src="https://lh7-eu.googleusercontent.com/docsz/AD_4nXfF5UqEzo1L_zOAQsayAgAwMQ0-eelFeDdHmGqYkdOj9QNYkeImgyURTeVR1nl7CiTfJ7TPhSsydJblCg87iDycAS3HnHtN6qgb8f5Cwa_aBc0NcyLOUvGLkrLzUTEawUdJXzbT1E5jdfJeewD6MgWd0fw?key=vP9tqrgkzZBD15oIdmy0HQ" alt=""><figcaption></figcaption></figure>

Now that our JSON-specific flow has been created, we can start our payload transformation steps:

1. Request phase:
   * REST to SOAP Transformation
2. Response phase:
   * XML to JSON

### **Payload Transformation (Request)**

Because the backend service is only SOAP, we must transform the incoming JSON request to a SOAP envelope.  We can use the “REST to SOAP Transformation” policy and pull in any JSON attributes (from the request payload) into the SOAP envelope. Follow these steps:

1. Click on the “**+**” button to add a new policy (within the “Request phase”).
2. Select the “**REST to SOAP Transformer**” policy.

<figure><img src="https://lh7-eu.googleusercontent.com/docsz/AD_4nXfpIArAtbAE4x8jpATLqYAVc4Mju4JtMw5yFkFkD6h5tAT1yKtY1H_wpkmS8kXztZfFMvEnR-kMF1WTbbz_J2cQPx06nhkyKQBn9xFxPd-j87Wz5RFIveEMgW08E03cVc2MsTaZ5IaHin1EFKBOx7II53hN?key=vP9tqrgkzZBD15oIdmy0HQ" alt=""><figcaption></figcaption></figure>

3. Specify the required SOAP envelope and use Gravitee’s Expression Language (EL) to dynamically insert the ‘Celsius’ value from the JSON request payload
   * e.g.:  \<Celsius>{#jsonPath(#request.content, '$.celsius')}\</Celsius>
4. Also specify the required SOAP Action too.
   * e.g.: https://www.w3schools.com/xml/CelsiusToFahrenheit\


<figure><img src="https://lh7-eu.googleusercontent.com/docsz/AD_4nXdYRR3nz6ftdBuio9KHbjQiQZTMUeSao2t-D27jhGmcndfSn0GwvZVyTBIhVEk_nxV1KcsYejiOHZC5NkysJYicUJWCDVlxj8EYz02VOdLXW2UPWbl8STlNEBekDctesVBzZa_XZneXvMWnU485QfSkNn8?key=vP9tqrgkzZBD15oIdmy0HQ" alt=""><figcaption></figcaption></figure>

5. Great! We’ve now transformed the incoming JSON request to the required SOAP envelope.  We can test this immediately by saving the Flow and clicking on the “**Deploy API**” button to push this new configuration to the API Gateway.  Again, both Postman and Curl examples are below:

<figure><img src="https://lh7-eu.googleusercontent.com/docsz/AD_4nXeqKimoYGYOK12gA0iDlLBrEY17fLV9EZCAEsm_n7Qdxzp3nekD8xiMfxdm0lVcsCmnLkiCf6RQwsUCxksY6OrTWA3tRAjiEpQNL1Yq43JCp35BXryIor3_UerJi_lfOJ8m7VEGn4S1QijKtDHHFNuqAjRF?key=vP9tqrgkzZBD15oIdmy0HQ" alt=""><figcaption></figcaption></figure>

```
curl -L 'http://localhost:8082/tempconvert-v4' -H 'Content-Type: application/json' -d '{
    "celsius": 31
}'

<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <soap:Body>
    <CelsiusToFahrenheitResponse xmlns="https://www.w3schools.com/xml/">
      <CelsiusToFahrenheitResult>87.8</CelsiusToFahrenheitResult>
    </CelsiusToFahrenheitResponse>
  </soap:Body>
</soap:Envelope>
```

### Payload Transformation (Response)

We now need to transform the SOAP response into JSON and extract just the single \<CelsiusToFahrenheitResult> value (to expose it in our defined JSON response).  In the “Response phase” we can use the “XML to JSON” policy along with the “JSON to JSON Transformation” policy to accomplish this step. Follow these steps:

1. Add the “XML to JSON” policy first (which doesn’t require any configuration).
2. And then add the “JSON to JSON Transformation” policy (after the “XML to JSON” policy).  You will need to define the JOLT specification for the required transformation.  In the screenshot below I’m simply extracting the value from the SOAP \<CelsiusToFahrenheitResult> attribute into our defined JSON ”result” key/value pair.
3. You should now see the flow (as shown in the screenshot below).   Finally click **Save** and **Deploy** **API**, and we can start testing the API again.

<figure><img src="https://lh7-eu.googleusercontent.com/docsz/AD_4nXdMVCNi2Xg78sMbkEBMZZuop4d-llho-JF2EuW2KDFf1qAdwN3wlZ-_ptefpEcxPHV8tl39dY4TJbQlDU8BZAu_RX6Ll_ifNdzFEJh8BIggGe50zfx1yizuHkJIJ9Vx1Ww_iTkJ-lp_F0lzotXnnLcrAaLi?key=vP9tqrgkzZBD15oIdmy0HQ" alt=""><figcaption></figcaption></figure>

### Test the API 

To test our API, we must specify the “Content-Type” header (with a value of “application/json”).\


<figure><img src="https://lh7-eu.googleusercontent.com/docsz/AD_4nXebZp3U7Q0fbD0Ueqe_JZwh85PxiDdXPU3KoM1KA_MACyoXpYuQt0IAPG6NUGRQClAqIprMnP3LgUxGJ_qaF18S0p1lb3XnQUpCA8T4VW9l0cpD3xd48h7NLvbBdFYau8KDeZVYo5ctzkuUjy4SJyk3XHQ?key=vP9tqrgkzZBD15oIdmy0HQ" alt=""><figcaption></figcaption></figure>

```
curl -L 'http://localhost:8082/tempconvert-v4' -H 'Content-Type: application/json' -d '{
    "celsius": 31
}'

{"result":87.8}
```

{% hint style="success" %}
Congrats!

We’ve now exposed a backend SOAP service as a REST API using JSON (whilst also keeping the existing SOAP capability as well).
{% endhint %}

### **JSON Validation**

However, to make this even better and easier to use, we should validate the incoming JSON request to ensure it matches our defined payload.  If it doesn’t match, then the Gateway should respond with an appropriate error message (and with an example of what a “good” JSON request should look like).

We'll continue our work in the Policy Studio. For this section, we will use the “JSON Validator” policy.  Follow these steps:

1. In the “Request phase”, and before the “REST to SOAP Transformer” policy, add in the “JSON Validation” policy.  Specify your custom error message as well as the required JSON Schema. In my case, I want to make “celsius” a required attribute/property and it must be of type “integer”.
   * E.g.: HTTP error message:  \
     `Bad message.  You must provide the celsius key/value in JSON.  Example: { "celsius" : 20 }`
   *   E.g.: JSON Schema:\
       {

       ```
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
2. Your flow should now look like this.  Don’t forget to **Save** and **Deploy your API**.

![](https://lh7-eu.googleusercontent.com/docsz/AD\_4nXcGr4PyD7S0g8vnXVz8Zs02GS5DSSW\_-h-BzyPig1a7S\_vIT85YEXvVZCn9AOmBrKLPd04fJaim15aXT7GPprIAjrlf4QZK8So9BiXz6banFuQq9xTSgYRjkNp8E4KoF56vGH1kqw1swhDoIUderQocUVXM?key=vP9tqrgkzZBD15oIdmy0HQ)

#### Test your API

Again, let’s do a couple of tests to prove this updated flow is indeed validating the incoming JSON response:

* This is bad request because “celsius” is misspelled:

```
curl -L 'http://localhost:8082/tempconvert-v4' -H 'Content-Type: application/json' -d '{
    "celsiusssss": 31
}'


Bad request - you must provide the celsius key/value in JSON.  Example:  {"celsius" : 20}

```

* This is also a bad request because the value is a string (when it should be an integer):

```
curl -L 'http://localhost:8082/tempconvert-v4' -H 'Content-Type: application/json' -d '{
    "celsius": "31"
}'


Bad request - you must provide the celsius key/value in JSON.  Example:  {"celsius" : 20}
```

* And finally, our good request (because it matches our defined JSON Schema):

```
curl -L 'http://localhost:8082/tempconvert-v4' -H 'Content-Type: application/json' -d '{
    "celsius": 31    
}'


{"result":87.8}
```

## Conclusion

We have now updated our legacy SOAP service to also handle JSON requests and JSON responses too.  We haven’t interrupted the existing SOAP service, as that just operates the same as before any of our changes.  However, we’ve added a new Flow that is only triggered by a JSON request.  So now our consumers have the best of both worlds and can use either SOAP envelopes or JSON.\


Payload or Message transformation is one of the core features of an API Gateway and there are a very broad range of options (or Policies as we call them) available.  And it’s not just payload transformation. There are other Policies available to perform security validation, token introspection, SSL enforcement, threat protection, response caching, HTTP callouts, custom scripts, dynamic routing, mock responses and many others!
