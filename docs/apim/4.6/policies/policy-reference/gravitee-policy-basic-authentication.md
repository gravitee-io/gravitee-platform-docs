= Basic authentication policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-basic-authentication/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-basic-authentication/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-basic-authentication/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-basic-authentication.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-basic-authentication"]
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

You can use the `basic-authentication` policy to manage basic authentication headers sent in API calls. The policy compares the user and password sent in the basic authentication header to an APIM user to determine if the user credentials are valid.

To use the policy in an API, you need to:

* configure an LDAP, inline or http resource for your API plan, which specifies where the APIM users are stored
* configure a basic authentication policy for the API flows

NOTE: LDAP, inline and http resources are not part of the default APIM configuration, so you must configure an LDAP, inline or http resource for APIM first, as described in the link:/apim/3.x/apim_devguide_plugins.html[Developer Guide^].

== Compatibility with APIM

|===
| Plugin version | APIM version

| 1.4.x and upper             | 3.15.x to latest
| Up to 1.x                   | Up to 3.14.x
|===

=== Connected user

After successful authentication, connected username is stored in context attributes, accessible with `context.attributes['user']` expression language.

In order to display the connected username in API logging, you can enable the environment setting `Gateway > API logging > Display end user on API Logging`.

This adds a `user` column in the logs table.

== Configuration

The policy configuration is as follows:

|===
|Property |Description |Type

|authenticationProviders||List of strings
|realm||string
|===
