---
description: This page provides the technical details of the OpenID Connect UserInfo policy
---

# OpenID Connect UserInfo

## Overview

Functional and implementation information for the OpenID Connect UserInfo policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-23.md#configuration)
* [Changelogs](template-policy-rework-structure-23.md#changelogs)

Use the `policy-openid-userinfo` to get the OpenId Connect user info from an OAuth2 resource through its UserInfo endpoint.

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

{% hint style="info" %}
The request will fail with a 401 status if the policy’s Oauth2 resource is misconfigured or not defined at all. To troubleshoot this, check the `WWW_Authenticate` header for more information.
{% endhint %}

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>oauthResource</td><td>true</td><td>The OAuth2 resource used to get UserInfo</td><td>string</td><td></td></tr><tr><td>extractPayload</td><td>false</td><td>When set to <code>true</code>, the payload of the response from the <code>UserInfo</code> endpoint is set in the <code>openid.userinfo.payload</code> gateway attribute</td><td>boolean</td><td></td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the OpenID Connect UserInfo policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-OpenID-Connect-UserInfo/blob/master/CHANGELOG.md" %}
