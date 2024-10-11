---
description: >-
  This page contains the changelog entries for AM 4.5.x and any future minor or
  patch AM 4.5.x releases
---

# AM 4.5.x

## Gravitee Access Management 4.5 - October 10, 2024

{% hint style="warning" %}
AM 4.5.0 introduce some deprecations which may have an impact on your systems. Please refer to the "Deprecations" section here after for more details.&#x20;
{% endhint %}

<details>

<summary>What's new</summary>

## Repositories

A new repository scope named `gateway` has been introduced in AM 4.5.0.&#x20;

## Token generation

For all domains created from AM 4.5.0 the `sub` claim will not represent the user internalID as it was the case previously.&#x20;

## AWS Certificate plugin

An AWS certificate plugin is now available as EE feature. Thanks to this plugin you can load certificate provided by AWS Secret Manager.

## Reporters

Reporters have been improved in this new version of Access Management:

* additional reporters can be configured as "global" in order to collect audits events coming from all the domains linked to this organization.
* Events for domain creation and domain deletion are now published in the organization reporters.&#x20;
* The kafka reporter has been improved to manage Schema Registry

## OpenID

We improved the OAuth2 / OpenID specification more strictly regarding the usage of the response\_mode paramet

## Group mapper

Identity Providers now provide a [Group Mapper](../../guides/identity-providers/user-and-role-mapping.md) section.

## Cache Layer

A cache layer has been introduce to limit the Database access during the user authentication flow.&#x20;

</details>

<details>

<summary>Breaking Changes</summary>

## Redirect Uris

On application creation or update `redirect_uris` is now required for application with type WEB, NATIVE or SPA.&#x20;

## Token generation

For all domains created from AM 4.5.0 the `sub` claim will not represent the user internalID as it was the case previously. The `sub` value is now an opaque value computed based on the user externalId and the identity provider identifier. Even if this value is opaque, it will remain the same for a given user accross multiple token generations as per the requirement of the OIDC specification.&#x20;

<mark style="color:red;">**NOTE:**</mark> For all domains created in previous version, the sub claim remains the user internalId.

## Repositories

A new repository scope named `gateway` has been introduced in AM 4.5.0.&#x20;

The new gateway scope will manage entities which was previously managed by the `oauth2` scope and the `management` scope:

* ScopeApproval&#x20;
* AuthenticationFlowContext
* LoginAttempts
* RateLimit
* VerifyAttempt

If you managed to define two differente databases for the `management` and the `oauth2` scopes, please configure the `gateway` scope to target the same database as the `oauth2` scope as ScopeApproval are now managed by the `gateway` scope. If you want to dedicate a database for the gateway scope you will have to migrate the scope\_approvals collection to the new database.

Previously, all the settings related to the repositories where define at the root level of the `gravitee.yaml` with the scope name as section name

{% code lineNumbers="true" %}
```yaml
mangement:
  type: mongodb
  mongodb: 
    uri: ...
    
oauth2:
  type: mongodb
  mongodb: 
    uri: ...
```
{% endcode %}

Starting from 4.5.0, a `repositories` section has been introduce to easily identify the settings related to the reposity layer.

<pre class="language-yaml" data-line-numbers><code class="lang-yaml"><strong>repositories:
</strong><strong>  mangement:
</strong><strong>    type: mongodb
</strong>    mongodb: 
      uri: ...
    
  oauth2:
    type: mongodb
    mongodb: 
      uri: ...
  
  gateway:
    type: mongodb
    mongodb: 
      uri: ...
</code></pre>

If you were using environment variable to provide database settings remember to:

* adapt the variable name to includ the "repositories" keyword
* add the settings for the gateway scope

</details>

<details>

<summary>Deprecations</summary>

## Audits

For kafka and File reporters, the `status` attibute has been deprecated for removal. The recommanded way to get access to the status is now the `outcome` structure which contains the `status` and a `message` fields. If you are using one of these reporter, please update your consumer to rely on the outcome structure

</details>
