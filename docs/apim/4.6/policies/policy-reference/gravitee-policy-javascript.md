= JavaScript policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-javascript/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-javascript/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-javascript/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-javascript.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-javascript"]
endif::[]

== Phase

|===
|onRequest|onResponse|onRequestContent|onResponseContent
|X|X|X|X
|===

== Description

You can use the http://www.javascript.com/[JavaScript^] policy to run JavaScript scripts at any stage of request processing through the gateway.

The following example JavaScript script is executed during the OnResponse phase to change HTTP headers:

[source, javascript]
----
response.headers.remove('X-Powered-By');
response.headers.set('X-Gravitee-Gateway-Version', '0.14.0');
----

== Configuration

[source, json]
"javascript": {
    "onRequestScript": "response.headers.remove('X-Powered-By');",
    "onResponseScript": "response.headers.set('X-Gravitee-Gateway-Version', '0.14.0');",
    "onRequestContentScript": "" // Not executed if empty
    "onResponseContentScript": "" // Not executed if empty
}

== Usage and examples

=== onRequest / onResponse

Some variables are automatically bound to the JavaScript script to allow users to use them and define the policy behavior.

[width="100%",cols="2,10",options="header"]
.List of javascript script variables
|===
| Name | Description

| `request` | Inbound HTTP request
| `response` | Outbound HTTP response
| `context` | `PolicyContext` used to access external components such as services and resources
| `result` | JavaScript script result

|===

Request or response processing can be interrupted by setting the result state to `FAILURE`.
By default, it will throw a `500 - internal server error` but you can override this behavior with the following properties:
- `code`: An HTTP status code
- `error`: The error message
- `key`: The key of a response template

[source, javascript]
----
if (request.headers.containsKey('X-Gravitee-Break')) {
    result.key = 'RESPONSE_TEMPLATE_KEY';
    result.state = State.FAILURE;
    result.code = 500
    result.error = 'Stop request processing due to X-Gravitee-Break header'
} else {
    request.headers.set('X-JavaScript-Policy', 'ok');
}
----

To customize the error sent by the policy:

[source, javascript]
----
result.key = 'RESPONSE_TEMPLATE_KEY';
result.state = State.FAILURE;
result.code = 400
result.error = '{"error":"My specific error message","code":"MY_ERROR_CODE"}'
result.contentType = 'application/json'
----

=== OnRequestContent / OnResponseContent

You can also transform request or response body content by applying a JavaScript script on
the `OnRequestContent` phase or the `OnResponseContent` phase.

WARNING: When working with scripts on `OnRequestContent` or `OnResponseContent` phase, the last instruction of the script **must be** the new body content that would be returned by the policy.

The following example shows you how to use the JavaScript policy to transform JSON content:

==== Input body content
[source, json]
----
[
    {
        "age": 32,
        "firstname": "John",
        "lastname": "Doe"
    }
]
----

==== JavaScript script
[source, javascript]
----
var content = JSON.parse(response.content);
content[0].firstname = 'Hacked ' + content[0].firstname;
content[0].country = 'US';

JSON.stringify(content);
----

==== Output body content
[source, json]
----
[
    {
        "age": 32,
        "firstname": "Hacked John",
        "lastname": "Doe",
        "country": "US"
    }
]
----

=== Dictionaries - Properties

Both Dictionaries (defined at the environment level) and Properties (defined at the API level) can be accessed from the JavaScript script, using:

 - `context.dictionaries()` for Dictionaries
 - `context.properties()` for Properties

Here is an example of how to set a request header based on a Property:

[source,javascript]
----
request.headers.set('X-JavaScript-Policy', context.properties()['KEY_OF_MY_PROPERTY']);
----

== Errors

=== HTTP status code

|===
|Code |Message

| ```500```
| The JavaScript script cannot be parsed/compiled or executed (mainly due to a syntax error)

|===

== Coming from Apigee

You will find below the main differences between JS scripts coming from Apigee and the one you will be able to run on the Gravitee platform:


|===
| |Apigee |Gravitee | Comment

|Access to context variables
|`context.getVariable('foo');`
|`context.attributes.foo;`
|

|Setting a context variable
|`context.setVariable('foo', 'bar');`
|`context.attributes.foo = 'bar';`
|

|Changing request or response header
|`context.targetRequest.headers['TARGET-HEADER-X']='foo';`
|`request.headers.set('TARGET-HEADER-X', 'foo');`
|`set` is used to replace the header value.

|Multivalued request or response header
|?
|`response.headers.add('TARGET-HEADER-X', 'foo');
response.headers.add('TARGET-HEADER-X', 'bar');`
|`add` can be used for multivalued headers.

|Changing response code or message
|`targetResponse.status.code = 500;`
|`response.status(500);`
|See `result` if you want to break the policy chain and return an error.

|Changing the body response
|`context.proxyResponse.content = 'foo';`
|`'foo';`
|Just set last instruction of the `OnRequestContent` to override the request body or 'OnResponseContent' to override the response body.

|Print messages
|`print('foo');`
|`print('foo');`
|The `print` statement has no effect and is simply ignored for now.

|Importing another js script
|
|
|This is not supported for now.

|Playing with request / response phases
|
`if (context.flow=="PROXY_RESP_FLOW") {
 // do something;
}`

|Use a script on each phase
|Phases are not exactly the same and gravitee does not allow to use a single script on different phases. You must define one script per phase or let the field blank if no script is necessary.

|Timeout
|`timeLimit` configuration at JavaScript policy level
|
|The timeout is not supported for now.

|Manage errors
|?
|
`result.state = State.FAILURE;
result.code = 400;
result.error = '{"error":"My specific error message","code":"MY_ERROR_CODE"}';
result.contentType = 'application/json';`
|

|Http call
|`httpClient.get("http://example.com", callback);`
|`httpClient.get("http://example.com", callback);`
|/!\ This feature is a draft feature and still in development. It may evolve or not be supported in the final version.
|===

