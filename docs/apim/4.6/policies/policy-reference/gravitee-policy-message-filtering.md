= Message Filtering policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-message-filtering/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-message-filtering/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-message-filtering/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-message-filtering.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-message-filtering"]
image:https://f.hubspotusercontent40.net/hubfs/7600448/gravitee-github-button.jpg["Join the community forum", link="https://community.gravitee.io?utm_source=readme", height=20]
endif::[]

== Phases

[cols="4*", options="header"]
|===
^|onRequest
^|onMessageRequest
^|onResponseContent
^|onMessageResponse

^.^|
^.^| X
^.^|
^.^| X

|===

== Description

You can use the `message-filtering` policy to filter the messages before they are propagated.

== Configuration

You can configure the policy with the following options:

|===
|Property |Required |Description |Type |Default

.^|filter
^.^|X
|The filter's rule.
^.^|string
^.^|-

|===

== Example

If my messages looks like :

[source, json]
----
{
    "productId": "1234",
    "value": "any value"
}
----

I will be able to filter any messages according to subscriptions metadata `productId` by configuring the policy as bellow :

[source, json]
----
 {
    "name": "Products filter",
    "description": "Filter messages based on subscription product id",
    "enabled": true,
    "policy": "message-filtering",
    "configuration": {
        "filter": "#jsonPath(#message.content, '$.productId') == '#subscription.metadata.productId'"
    }
}
----
