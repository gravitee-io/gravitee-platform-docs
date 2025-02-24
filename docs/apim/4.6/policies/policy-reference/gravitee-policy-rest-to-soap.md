= REST to SOAP policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-rest-to-soap/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-rest-to-soap/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-rest-to-soap/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-rest-to-soap.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-rest-to-soap"]
endif::[]

== Phase

|===
|onRequest |onResponse

| X
|

|===

== Description

You can use the `rest-to-soap` policy to expose SOAP backend service as a REST API. The policy will pass the SOAP envelope message
to the backend service as a POST request. SOAP envelopes support Expression Language to provide dynamic SOAP actions.

For example, a SOAP API `http(s)://GATEWAY_HOST:GATEWAY_PORT/soap?countryName=France` with the following `rest-to-soap` policy SOAP envelope content:

[source=xml]
----
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope\\\" xmlns:web=\\\"http://www.oorsprong.org/websamples.countryinfo">
   <soap:Header/>
   <soap:Body>
      <web:CountryISOCode>
         <web:sCountryName>{#request.params['countryName']}</web:sCountryName>
      </web:CountryISOCode>
   </soap:Body>
</soap:Envelope>
----

Will give you the ISO country code for `France`.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===

== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type |Default

|SOAP Envelope
|X
|
|SOAP envelope used to invoke WS (supports Expression Language)
|

|SOAP Action
|
|
|'SOAPAction' HTTP header sent when invoking WS
|

|Charset
|
|
|This charset will be appended to the `Content-Type` header value
|

|Preserve Query Parameters
|
|
|Whether the query parameters are propagated to the backend SOAP service
|

|===


[source, json]
.Sample
----
"rest-to-soap": {
  "envelope": "<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:web="http://www.oorsprong.org/websamples.countryinfo">
                 <soap:Header/>
                 <soap:Body>
                    <web:ListOfCountryNamesByName/>
                 </soap:Body>
              </soap:Envelope>",
  "soapAction": null
}
----
