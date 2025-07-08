---
hidden: true
---

# APIM 4.8.x

## Gravitee API Management 4.8.1 - July 7, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Hardcoded value for health check in 4.7 versions and above in docker images ( for both gateway and mapi ) [#10644](https://github.com/gravitee-io/issues/issues/10644)

**Management API**

* Subscriptions in the subscriptions tab of an application seem to only show the first 10 item [#10529](https://github.com/gravitee-io/issues/issues/10529)
* Users with both group inheritance and individual access to applications are limited in which applications to which they can subscribe [#10601](https://github.com/gravitee-io/issues/issues/10601)
* Hardcoded value for health check in 4.7 versions and above in docker images ( for both gateway and mapi ) [#10644](https://github.com/gravitee-io/issues/issues/10644)
* Debug mode for v4 proxy apis returns a 500 response [#10648](https://github.com/gravitee-io/issues/issues/10648)
* Using jsonPath in Assign Attributes policy prevents sending transformed body in HTTP Callout policy

**Console**

* Wrong display when adding a user to a group [#10558](https://github.com/gravitee-io/issues/issues/10558)
* Prevent API Modification for Unauthorized API Users [#10594](https://github.com/gravitee-io/issues/issues/10594)

**Portal**

* Subscriptions in the subscriptions tab of an application seem to only show the first 10 item [#10529](https://github.com/gravitee-io/issues/issues/10529)

**Other**

* Unable to add a group to an existing user using console [#10378](https://github.com/gravitee-io/issues/issues/10378)
* Console : Categories Page doesn't show updated image for any category [#10523](https://github.com/gravitee-io/issues/issues/10523)
* Primary owner Group should not be removed from an API  [#10580](https://github.com/gravitee-io/issues/issues/10580)
* Custom policy depending on gravitee-resource-oauth2-provider-generic  [#10620](https://github.com/gravitee-io/issues/issues/10620)
* Portal Theme Settings : UNABLE to change Theme color [#10647](https://github.com/gravitee-io/issues/issues/10647)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Enable multi-tenant support for Dictionaries by default [#10637](https://github.com/gravitee-io/issues/issues/10637)

**Other**

* Increase character limit of condition field in flow_selectors table [#10560](https://github.com/gravitee-io/issues/issues/10560)

</details>