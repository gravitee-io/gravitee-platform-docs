= IP filtering policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-ipfiltering/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-ipfiltering/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-ipfiltering/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-ipfiltering.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-ipfiltering"]
endif::[]

== Phase

|===
|onRequest |onResponse

|X
|

|===

== Description

You can use the `ip-filtering` policy to control access to your API by filtering IP addresses.
You can allow or deny a specific IP address or range of IP addresses with https://tools.ietf.org/html/rfc1519[CIDR^].

Whitelist mode excludes all IP addresses except the addresses included in the whitelist.
Blacklist mode allows all IP addresses except the addresses included in the blacklist.

The blacklist takes precedence, so if an IP address is included in both lists, the policy rejects the request.

You can specify a host to be resolved and checked against the remote IP.

NOTE: When using domain name, the Gateway is performing DNS Lookup with the DNS server configured on the host by default. If you want to use a specific DNS server, you can configure it at the policy level. See <<_gateway>> for more information.

== Compatibility with APIM

|===
| Plugin version | APIM version
| 1.x            | All supported versions
|===

== Configuration
You can configure the policy with the following options:

=== Policy

At the policy level, you can configure the following options:

|===
|Property |Required |Description |Type |Default

|matchAllFromXForwardedFor
|No
|If set to `true`, the `X-Forwarded-For` header is parsed to extract all IP addresses and check them against the whitelist or blacklist.
|boolean
|`false`

|whitelistIps
|No
|A list of allowed IPs with or without CIDR notation (host is allowed)
|string list
|`empty`

|blacklistIps
|No
|A list of denied IPs with or without CIDR notation (host is allowed)
|string list
|`empty`

|lookupIpVersion
|No
|IP version to use to lookup host name. If you're not sure your DNS server can handle multi-question requests (both V4 and V6) specify a version.
|enum [`IPV4`, `IPV6`, `ALL`]
|`ALL`


|===

[#_gateway]
=== Gateway

At the gateway level, you can configure the DNS server used to perform DNS Lookup for a given name (when using domain name instead of IP).Example:

[source,yaml]
----
policy:
  ip-filtering:
    dns:
      host: 8.8.8.8
      port: 53
----

== Examples

[source, json]
----
"ip-filtering": {
  "matchAllFromXForwardedFor": true,
  "whitelistIps": [
    "10.0.0.1",
    "10.0.0.2/10",
    "gravitee.io"
  ],
  "blacklistIps": [
    null
  ],
  "lookupIpVersion": "IPV4"
}
----

== Errors

=== HTTP status code

|===
|Code |Message

| ```403```
| Your IP (0.0.0.0) or one of the proxies your request passed through is not allowed to reach this resource

|===
