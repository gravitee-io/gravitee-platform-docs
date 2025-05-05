= AWS Lambda

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-aws-lambda/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-aws-lambda/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-aws-lambda/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-aws-lambda.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-aws-lambda"]
endif::[]

== Phase

[cols="4*", options="header"]
|===
^|onRequest
^|onResponse
^|onRequestContent
^|onResponseContent

^.^| X
^.^| X
^.^| X
^.^| X

|===

== Compatibility with APIM

|===
|Plugin version    | APIM version       | JDK version

| 2.x              | 4.7.x and later    | 21
| 1.x              | 3.x to 4.6.x       | 17

|===

WARNING: The version 1.3.0 should not be used.


== Description

AWS Lambda policy can be used to request a Lambda instead of or in addition to the backend.

By default, the lambda is called in addition to the backend, meaning the consumer will not receive the response from Lambda.


== Configuration

|===
|Property |Required |Description |Type |Default

.^|scope
^.^|X
|The scope on which apply the policy (Only relevant for v2 APIs)
^.^|string
^.^|REQUEST

.^|region
^.^|X
|The AWS region
^.^|string
^.^|us-east-1

.^|accessKey
^.^|
|AWS Access Key
^.^|string
^.^|-

.^|secretKey
^.^|
|AWS Secret Key
^.^|string
^.^|-

.^|function
^.^|X
|The name of the AWS Lambda function to call
^.^|string
^.^|-

.^|payload
^.^|
|Payload of the request to AWS Lambda function
^.^|string
^.^|-

.^|variables
^.^|
|The variables to set in the execution context when retrieving content of HTTP call (support EL)
^.^|List of variables
^.^|-

.^|sendToConsumer
^.^|
|Check this option if you want to send the response of the lambda to the initial consumer without going to the final upstream (endpoints) selected by the gateway.
^.^|boolean
^.^|false

.^|invocationType
^.^|X
|RequestResponse (default) – Invoke the function synchronously. Keep the connection open until the function returns a response or times out. The API response includes the function response and additional data.
Event – Invoke the function asynchronously. Send events that fail multiple times to the function's dead-letter queue (if one is configured). The API response only includes a status code.
DryRun – Validate parameter values and verify that the user or role has permission to invoke the function.
^.^|string
^.^|RequestResponse

.^|qualifier
^.^|-
|Specify a version or alias to invoke a published version of the function.
^.^|string
^.^|-

.^|logType
^.^|X
|Set to Tail to include the execution log in the response. Applies to synchronously invoked functions only.
^.^|string
^.^|None

.^|roleArn
^.^|-
|The arn of the role to be assumed. This is used when authentication is relying on the AWS Security Token Service (STS) to assume a Role and create temporary, short-lived sessions to use for authentication.
^.^|string
^.^|-

.^|roleSessionName
^.^|-
|An identifier for the assumed role session (Only used when authentication is based on AWS Security Token Service (STS)
^.^|string
^.^|gravitee

|===

== Examples

[source, json]
----
"configuration": {
    "variables": [
      {
        "name": "lambdaResponse",
        "value": "{#jsonPath(#lambdaResponse.content, '$')}"
      }
    ],
    "secretKey": "secretKey",
    "accessKey":"accessKey",
    "payload": "{ \"key\": \"value\" }",
    "scope": "REQUEST",
    "function": "lambda-example",
    "region": "us-east-1",
    "sendToConsumer": true,
    "endpoint": "http://aws-lambda-url/function"
}
----

== Errors

=== Default error

|===
|Code |Message

.^| ```500```
| Request processing broken

|===

=== Override errors

You can override the default response provided by the policy with the response templates feature. These templates must be defined at the API level with the APIM Console *Proxy > Response Templates* function.

The error keys sent by this policy are as follows:

[cols="3*", options="header"]
|===
^|Key
^|Default status
^|Parameters

.^|AWS_LAMBDA_INVALID_RESPONSE
^.^|500
^.^|-

.^|AWS_LAMBDA_INVALID_STATUS_CODE
^.^|400
^.^|-

|===