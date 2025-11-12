---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.5.
---

# AM 4.5

## AWS Certificate plugin

An AWS certificate plugin is now available as EE feature. Thanks to this plugin you can load certificate provided by AWS Secret Manager.

## Reporters

Reporters have been improved in this new version of Access Management.

First of all you are now able to create additional reporter at organization level as you can already do at domain level. Those additional reporters can be configured as "global" in order to collect audits events coming from all the domains linked to this organization.

{% hint style="info" %}
Events for domain creation and domain deletion are now published in the organization reporters.
{% endhint %}

Second, the kafka reporter has been improved to manage Schema Registry. If configured, you consumers will have access to the audit schema for validation.

{% hint style="danger" %}
The audit message published to Kafka and the file reporter has been updated to include a new embedded object named 'outcome.' This object contains two fields, 'status' and 'message,' to provide the same level of detail as the default reporter.

With the introduction of the 'outcome,' the 'status' field has been marked as deprecated for removal, as the 'outcome' status contains the same value. Please ensure you adapt your ingestion process accordingly if necessary.
{% endhint %}

## OpenID

We improved the OAuth2 / OpenID specification more strictly regarding the usage of the response\_mode parameter. It is now possible to request a response\_mode set to fragment for code flow and all the flows which provide a token are now limited to response\_mode set to fragment.

## Domain creation

It is now possible to disable the creation of the default reporter and the default identity provider during domain creation. See Access Management API [configuration](../../getting-started/configuration/configure-am-api/) section for more details.

## Group mapper

Identity Providers now provide a [Group Mapper](docs/am/4.5/guides/identity-providers/user-and-role-mapping.md) section. In the same way as role mapper, you know have a way to dynamically assign a user to a group based on the user profile provided by the identity provider.

## Token generation

For all domains created from AM 4.5.0 the `sub` claim will not represent the user internalID as it was the case previously. The sub value is now an opaque value computed based on the user externalId and the identity provider identifier. Even if this value is opaque, it will remain the same for a given user across multiple token generations as per the requirement of the OIDC specification. Domains create from AM 4.5.0 also introduce a new claim named `gis` when the tokens are linked to a user profile. This claim is used internally by AM to identify a user.

The `sub` value is now an opaque value computed based on the user externalId and the identity provider identifier. Even if this value is opaque, it remains the same for a given user across multiple token generations as per the requirement of the OIDC specification.

{% hint style="warning" %}
The `gis` claim should not be used or stored by external system as it make sense only within AM.
{% endhint %}

{% hint style="success" %}
All domains which have been created in previous AM version will continue to initialize the sub claim using the user internalID.
{% endhint %}

## Cache Layer

A cache layer has been introduce to limit the Database access during the user authentication flow. AM sessions are stateless and on each request we are looking into the database to retrieve the user profile in order to execute the authentication step. By introducing a cache layer, the AM gateway is looking into the cache to restore the user profile.

In addition of the user profile, AM gateway now have the capability to load roles and groups definitions from the synchronization process to avoid reading the database to get those information during the authentication flow.

## Repositories

A new repository scope named `gateway` has been introduced in AM 4.5.0.

{% hint style="info" %}
The new gateway scope will manage entities which was previously managed by the `oauth2` scope and the `management` scope:

* ScopeApproval
* AuthenticationFlowContext
* LoginAttempts
* RateLimit
* VerifyAttempt
{% endhint %}

{% hint style="warning" %}
If you managed to define two different databases for the `management` and the `oauth2` scopes, please configure the `gateway` scope to target the same database as the `oauth2` scope as ScopeApproval are now managed by the `gateway` scope. If you want to dedicate a database for the gateway scope you will have to migrate the scope\_approvals collection to the new database.
{% endhint %}

{% hint style="danger" %}
Previously, all the settings related to the repositories where define at the root level of the `gravitee.yaml` with the scope name as section name

{% code lineNumbers="true" %}
```yaml
management:
  type: mongodb
  mongodb: 
    uri: ...
    
oauth2:
  type: mongodb
  mongodb: 
    uri: ...
```
{% endcode %}

Starting from 4.5.0, a `repositories` section has been introduce to easily identify the settings related to the repository layer.

<pre class="language-yaml" data-line-numbers><code class="lang-yaml"><strong>repositories:
</strong><strong>  management:
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

* adapt the variable name to include the "repositories" keyword
* add the settings for the gateway scope
{% endhint %}
