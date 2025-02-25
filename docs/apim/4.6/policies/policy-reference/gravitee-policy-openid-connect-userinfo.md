= OpenID Connect user info policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-openid-connect-userinfo/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-openid-connect-userinfo/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-openid-connect-userinfo/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-openid-connect-userinfo.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-openid-connect-userinfo"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequest
^|onResponse

^.^| X
^.^|

|===

== Description

Use the `policy-openid-userinfo` to get the OpenId Connect user info from an OAuth2 resource through its UserInfo endpoint.

NOTE: The request will fail with a 401 status if the policy's Oauth2 resource is misconfigured or not defined at all. To troubleshoot this, check the `WWW_Authenticate` header for more information.

== Configuration

Use the following options to configure the policy:

|===
|Property |Required |Description |Type |Default

|oauthResource|X|The OAuth2 resource used to get UserInfo|string|
|extractPayload||When set to  `true`, the payload of the response from the `UserInfo` endpoint is set in the `openid.userinfo.payload` gateway attribute|boolean|