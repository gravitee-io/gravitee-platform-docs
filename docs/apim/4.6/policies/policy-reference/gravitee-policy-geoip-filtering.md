= GeoIP filtering policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-geoip-filtering/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-geoip-filtering /blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-geoip-filtering/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-geoip-filtering.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-geoip-filtering"]
endif::[]


IMPORTANT: To use this policy, you must first install plugin https://download.gravitee.io/#plugins/services/[gravitee-service-geoip]
This plugin loads the `geoip` databases in memory, so you need to adjust the JVM Heap settings of your APIM Gateways accordingly.

== Phase

|===
|onRequest |onResponse

|X
|

|===

== Description

You can use the `geoip-filtering` policy to control access to your API by filtering IP addresses.
You can allow IPs by country or distance.

Toggle the `Expose GeoIP Matching` option to expose the GeoIP response as context attributes.
You can reference the GeoIP matched response data using Expression Language (e.g.:  `{#context.attributes['geoIP_country_name']}` ), such as adding the country to the payload or applying a condition onto another policy.

Whitelist mode excludes all IP addresses except the addresses included in the whitelist.

== Configuration
You can configure the policy with the following options:

|===
|Property |Required |Description |Type |Default

|failOnUnknown
|Yes
|If set to `true`, each unknown IP is reject.
|boolean
|`true`

|exposeGeoIpMatching
|No
|If set to `true`, the following context attributes will be populated; geoIP_remote_address, geoIP_country_iso_code, geoIP_country_name, geoIP_region_name, geoIP_city_name, geoIP_timezone
|boolean
|`false`

|whitelistRules
|No
|A list of allowed rules
|Whitelist Rule
|`empty`

|===

=== Whitelist rule

|===
|Property |Required |Description |Type |Default

|Type
|Yes
|type of rule COUNTRY or DISTANCE
|enum
|COUNTRY

|Country
|No
|Country (must be defined in case type is set to COUNTRY)
|enum
|A1

|Latitude
|No
|Latitude (must be defined in case type is set to DISTANCE)
|number
|0.0

|Longitude
|No
|Longitude (must be defined in case type is set to DISTANCE)
|number
|0.0

|Distance (in meters)
|No
|Distance max (must be defined in case type is set to DISTANCE)
|integer
|10000
|===

== Examples

[source, json]
----
"geoip-filtering": {
  "failOnUnknown": true,
  "whitelistRules": [
    {
        "type": "COUNTRY",
        "country": "FR"
    },
   {
       "type": "DISTANCE",
       "distance": "50000"
   }
  ],
}
----

== Errors

=== HTTP status code

|===
|Code |Message

| ```403```
| You're not allowed to access this resource

|===

== Compatibility with APIM

|===
|Plugin version | APIM version

|2.x and upper                  | 4.0.x to latest
|1.x                            | Up to 3.20.x
|===
