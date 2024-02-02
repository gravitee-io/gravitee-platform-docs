---
description: >-
  This page contains the changelog entries for APIM 4.2.x and any future patch
  APIM 4.2.x releases
---

# APIM 4.2.x

## Gravitee API Management 4.2.2 - February 2, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Unable to populate attributes using the Assign Attributes policy due to enabled v4 Engine [#9420](https://github.com/gravitee-io/issues/issues/9420)
* Conditional logging [#9486](https://github.com/gravitee-io/issues/issues/9486)
* Timeout when connecting to WebSocket API using header Connection:Upgrade,Keep-Alive [#9487](https://github.com/gravitee-io/issues/issues/9487)

**Management API**

* Cannot Create API with Webhook Only Entrypoint [#9462](https://github.com/gravitee-io/issues/issues/9462)
* Use legacy configuration when upgrading to 4.2.x [#9483](https://github.com/gravitee-io/issues/issues/9483)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Add API ID in healthcheck logs [#9493](https://github.com/gravitee-io/issues/issues/9493)

</details>

## Gravitee API Management 4.2.1 - January 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Sometimes path-mapping is not working [#9450](https://github.com/gravitee-io/issues/issues/9450)
* Management API does not encode a value in the URL used in a pipe [#9461](https://github.com/gravitee-io/issues/issues/9461)
* gRPC backend received unexpected headers [#9463](https://github.com/gravitee-io/issues/issues/9463)

**Management API**

* Unable to switch to gRPC endpoint type from the Console UI [#9456](https://github.com/gravitee-io/issues/issues/9456)
* Updating an API reset the gRPC type of the endpoint [#9464](https://github.com/gravitee-io/issues/issues/9464)

**Console**

* Unable to edit Dictionaries anymore [#9451](https://github.com/gravitee-io/issues/issues/9451)
* Navigation in a multi-environments console is messed up [#9467](https://github.com/gravitee-io/issues/issues/9467)

**Portal**

* Docs not loaded instantly [#9452](https://github.com/gravitee-io/issues/issues/9452)

**Helm Charts**

* Backward incompatibility during Helm upgrade with old `values.yml` [#9446](https://github.com/gravitee-io/issues/issues/9446)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Access request host property in Expression Language [#9453](https://github.com/gravitee-io/issues/issues/9453)

</details>
