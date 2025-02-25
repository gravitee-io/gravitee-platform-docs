= HTML to JSON transformation policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-html-json/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-html-json/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-html-json/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-html-json.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-html-json"]
image:https://f.hubspotusercontent40.net/hubfs/7600448/gravitee-github-button.jpg["Join the community forum", link="https://community.gravitee.io?utm_source=readme", height=20]
endif::[]

== Scope

|===
|onRequest|onResponse|onRequestContent|onResponseContent
||||X
|===

== Description

You use the `html-json` transformation policy to transform the response content.

This policy is based on the https://jsoup.org[jsoup^] HTML parser.
In APIM, all you need to do is provide your JSON field names with the
associated selectors.

== Compatibility with APIM

|===
|Plugin version | APIM version

|1.x            | All supported versions
|===

== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type
|jsonName |true|Name of the JSON field to contain the result of the selection|String
|selector |true|HTML/CSS selector used to select an element and get the text|String
|array    |false|Used to determine whether the selection needs to be returned as an array|Boolean
|===

== Examples

[source, json]
----
"html-json": {
    "selectors":
        [
            {
                "array": false,
                "jsonName": "test",
                "selector": ".class h1"
            },
            {
                "array": true,
                "jsonName": "testArray",
                "selector": ".container ul"
            }
        ]
    }
}
----
