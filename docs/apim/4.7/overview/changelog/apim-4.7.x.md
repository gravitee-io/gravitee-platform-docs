# APIM 4.7.x
 
## Gravitee API Management 4.7.5 - May 9, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* CompositeByteBuf is creating a high volume of logs [#10539](https://github.com/gravitee-io/issues/issues/10539)
* Problems with HTTP code 502 because of keepalive

**Management API**

*  Rollback does not work for the v4 emulation button [#10190](https://github.com/gravitee-io/issues/issues/10190)
* Application search does not work if search term pattern matches _id pattern [#10487](https://github.com/gravitee-io/issues/issues/10487)

**Console**

* Local link to internal section dose not work in documentation [#10180](https://github.com/gravitee-io/issues/issues/10180)
* APIM API Throwing HTTP 500 On a Specific Returned Page [#10372](https://github.com/gravitee-io/issues/issues/10372)
* Settings-> Groups : 'Allows invitation via user search' is NOT working as expected [#10485](https://github.com/gravitee-io/issues/issues/10485)
* Application search does not work if search term pattern matches _id pattern [#10487](https://github.com/gravitee-io/issues/issues/10487)
* UX problem in condition alerting threshold [#10514](https://github.com/gravitee-io/issues/issues/10514)

**Other**

* Response time different between log file and UI [#10301](https://github.com/gravitee-io/issues/issues/10301)
* Schema registry resource URL not fully taken into account [#10530](https://github.com/gravitee-io/issues/issues/10530)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Use Gravitee GPG Key to sign RPM package [#10450](https://github.com/gravitee-io/issues/issues/10450)

</details>


 
## Gravitee API Management 4.7.4 - April 25, 2025
<details>

<summary>Bug Fixes</summary>

**Management API**

* Global Alert configuration page does not refresh properly after change [#10436](https://github.com/gravitee-io/issues/issues/10436)
* Issue with Policy Execution Order [#10486](https://github.com/gravitee-io/issues/issues/10486)

**Console**

* API Traffic Settings page is not visible for V4 Message APIs due to permission issue for default roles [#10386](https://github.com/gravitee-io/issues/issues/10386)

**Portal**

* Portal-Next shows all Unpublished apis  [#10505](https://github.com/gravitee-io/issues/issues/10505)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Type of application is removed after update\[ApplicationType \[null] cannot be found]. [#10359](https://github.com/gravitee-io/issues/issues/10359)

</details>


 
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
* v4 api : Unable to manage groups for all api types  [#10471](https://github.com/gravitee-io/issues/issues/10471)
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


