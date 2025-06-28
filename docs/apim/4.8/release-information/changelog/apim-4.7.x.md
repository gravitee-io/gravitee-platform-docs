# APIM 4.7.x

## Gravitee API Management 4.7.3 - April 17, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Bug in io.gravitee.connector.http.HttpConnection.java exceptionHandler [#10439](https://github.com/gravitee-io/issues/issues/10439)

**Console**

* Logs filter display Unpublished plan [#10480](https://github.com/gravitee-io/issues/issues/10480)

</details>

## Gravitee API Management 4.7.2 - April 11, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* XSLT Transformation not applied when in response phase of v4 APIs [#10354](https://github.com/gravitee-io/issues/issues/10354)
* IP filtering policy does not check all the IPs for a host in white/blacklist [#10373](https://github.com/gravitee-io/issues/issues/10373)
* Unbounded Gateway memory growth in Openshift Kubernetes cluster [#10483](https://github.com/gravitee-io/issues/issues/10483)

**Management API**

* Failed association of groups to APIs [#10211](https://github.com/gravitee-io/issues/issues/10211)
* Custom API Key not taken into account when created through API Plan [#10324](https://github.com/gravitee-io/issues/issues/10324)
* Prevent Primary Owner removal when updating application's membership via cURL [#10382](https://github.com/gravitee-io/issues/issues/10382)
* Data export inconsistencies in APIv4 (members, metadata, and plans) [#10459](https://github.com/gravitee-io/issues/issues/10459)
* v4 api : Unable to manage groups for all api types [#10471](https://github.com/gravitee-io/issues/issues/10471)
* Adding an unknown group id to excluded groups on a plan in v4 apis removes all excluded groups and prevents exports of the API [#10473](https://github.com/gravitee-io/issues/issues/10473)

**Console**

* Failed association of groups to APIs [#10211](https://github.com/gravitee-io/issues/issues/10211)
* V4 Flows cannot be duplicated or disabled [#10242](https://github.com/gravitee-io/issues/issues/10242)
* Unable to update Alert Rate Condition after clearing aggregation field [#10332](https://github.com/gravitee-io/issues/issues/10332)
* Newly created applications are not associated to groups that have "Associate automatically to every new application" enabled [#10457](https://github.com/gravitee-io/issues/issues/10457)
* Resolver parameter for JWT plan none accessible [#10476](https://github.com/gravitee-io/issues/issues/10476)

**Portal**

* Saved application alert in Dev Portal fails to display percentage value [#10446](https://github.com/gravitee-io/issues/issues/10446)
* Registration Confirmation URL incorrectly includes full path and query parameters [#10456](https://github.com/gravitee-io/issues/issues/10456)

</details>

## Gravitee API Management 4.7.1 - April 4, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway stops syncing apis after failing to connect to jdbc datasource [#10441](https://github.com/gravitee-io/issues/issues/10441)

**Management API**

* API key is not working for API subscriptions when we use Shared API key [#10122](https://github.com/gravitee-io/issues/issues/10122)
* Adding an unknown group id to excluded groups on a plan removes all excluded groups and prevents exports of the API [#10389](https://github.com/gravitee-io/issues/issues/10389)

**Console**

* API key is not working for API subscriptions when we use Shared API key [#10122](https://github.com/gravitee-io/issues/issues/10122)
* Account page broken in multi-environment installation [#10451](https://github.com/gravitee-io/issues/issues/10451)
* API Export does not "respect" selected export options [#10455](https://github.com/gravitee-io/issues/issues/10455)
* Display only http methods in debug mode tool [#10467](https://github.com/gravitee-io/issues/issues/10467)

**Portal**

* NewDevPortal - Swagger expands outside of allowed frame [#10461](https://github.com/gravitee-io/issues/issues/10461)
* Unable to show Swagger docs for Native api on Portal-Next [#10462](https://github.com/gravitee-io/issues/issues/10462)

**Other**

* Groups not automatically added to new applications when they should be [#10470](https://github.com/gravitee-io/issues/issues/10470)

</details>
