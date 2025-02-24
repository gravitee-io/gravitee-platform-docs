= WS Security Authentication Policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-wssecurity-authentication/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-wssecurity-authentication/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-wssecurity-authentication/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-wssecurity-authentication.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-wssecurity-authentication"]
endif::[]

== Phase

[cols="2*", options="header"]
|===
^|onRequestContent
^|onResponse

^.^| X
^.^|

|===

== Description

You can use the `wssecurity-authentication` policy to manage security part from a soap call. The policy compares the username and password sent in the soap header to an APIM user to determine if the user credentials are valid.

To use the policy in an API, you need to:

* configure an LDAP, inline or http resource for your API plan, which specifies where the APIM users are stored
* configure a WS-Security authentication policy for the API flows

=== Example
In the example below, the policy will extract *foo* & *bar* from the payload.
[source, XML]
----
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Header>
        <wsse:Security xmlns:wsse="http://schemas.xmlsoap.org/ws/2003/06/secext">
            <wsse:UsernameToken>
                <wsse:Username>foo</wsse:Username>
                <wsse:Password>bar</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soap:Header>
    <soap:Body>
        ...
    </soap:Body>
</soap:Envelope>
----

NOTE: LDAP, inline and http resources are not part of the default APIM configuration, so you must download these resource plugins from https://download.gravitee.io/#graviteeio-apim/plugins/resources/[here]

== Compatibility with APIM

|===
|Plugin version | APIM version
|1.x            | 3.x
|2.x            | 4.0 and later

|===

== Configuration

The policy configuration is as follows:

|===
|Property |Description |Type

|authenticationProviders||List of strings
