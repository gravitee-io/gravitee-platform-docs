---
description: >-
  This page contains the changelog entries for AM 4.9.0 and any future minor or
  patch AM 4.9.x releases
---

# AM 4.9.x

## Gravitee Access Management 4.9.9 - January 19, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* Retrieve clientID from context for AccountFactorsEndpointHandler::sendChallenge [#11023](https://github.com/gravitee-io/issues/issues/11023)





**Other**

* [Helm] Dataplane volume are missing for JDBC backend [#11008](https://github.com/gravitee-io/issues/issues/11008)
* Unable to sign in when username contains Capital [#11015](https://github.com/gravitee-io/issues/issues/11015)
* Create Index on ScopeApproval [#11020](https://github.com/gravitee-io/issues/issues/11020)
* ErrorDescription encoded in the errorHash [#11054](https://github.com/gravitee-io/issues/issues/11054)

</details>


## Gravitee Access Management 4.9.8 - January 2, 2026

<details>

<summary>Bug fixes</summary>







**Other**

* AuthenticationFlow: missing transactionId [#11033](https://github.com/gravitee-io/issues/issues/11033)
* LDAP provider role mapping no longer working [#11038](https://github.com/gravitee-io/issues/issues/11038)
* Unable to add multiple virtual hosts in Gravitee AM [#11048](https://github.com/gravitee-io/issues/issues/11048)

</details>


## Gravitee Access Management 4.9.7 - December 19, 2025

<details>

<summary>Bug fixes</summary>







**Other**

* Apply jemalloc to dockerfile for Gateway/MAPI (4.7+) [#10991](https://github.com/gravitee-io/issues/issues/10991)
* Audit logs output incorrect JSON [#11000](https://github.com/gravitee-io/issues/issues/11000)
* Introduce setting to avoid fallback on HMAC [#11018](https://github.com/gravitee-io/issues/issues/11018)
* The default am gateway helm chart does not include mappings for custom purge settings. [#11024](https://github.com/gravitee-io/issues/issues/11024)
* Enhance logging in gateway consent failure handler [#11025](https://github.com/gravitee-io/issues/issues/11025)
* MFA challenge is always presented when session is expired and Remember Me cookie bypasses login [#11029](https://github.com/gravitee-io/issues/issues/11029)

</details>


## Gravitee Access Management 4.9.6 - December 10, 2025

<details>

<summary>Bug fixes</summary>







**Other**

* Specify application on User preRegistration using SCIM [#11003](https://github.com/gravitee-io/issues/issues/11003)
* Fix docker image size [#11016](https://github.com/gravitee-io/issues/issues/11016)

</details>


## Gravitee Access Management 4.9.5 - December 5, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* MFA RateLimit doesn't work when MFA Challenge policy is define at domain level [#10998](https://github.com/gravitee-io/issues/issues/10998)

**Management API**

* WebAuthn - credentials are not removed when a user is deleted [#10990](https://github.com/gravitee-io/issues/issues/10990)



**Other**

* The default helm chart currently does not reflect our suggested {{maxAcquireTime}} and {{maxCreateConnectionTime}} values. [#10983](https://github.com/gravitee-io/issues/issues/10983)
* Implement retry on HSM sign/verify [#10992](https://github.com/gravitee-io/issues/issues/10992)
* Allow implicit authentication on CloudHSM plugin [#10996](https://github.com/gravitee-io/issues/issues/10996)
* Session clean up on Registration & resetPassword confirmation [#10999](https://github.com/gravitee-io/issues/issues/10999)
* Email notification fails for Certificate expiry [#11007](https://github.com/gravitee-io/issues/issues/11007)

</details>


## Gravitee Access Management 4.9.4 - November 21, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* JSON Logging for AM Token Endpoint [#10943](https://github.com/gravitee-io/issues/issues/10943)
* Filter CLIENT\_AUTHENTICATION success audit logs [#10954](https://github.com/gravitee-io/issues/issues/10954)
* translate email from name [#10958](https://github.com/gravitee-io/issues/issues/10958)
* Vertx eventLoop ThreadBlocked when HSM plugin is used [#10969](https://github.com/gravitee-io/issues/issues/10969)

**Management API**

* Error creating identities in 4.7.X [#10940](https://github.com/gravitee-io/issues/issues/10940)

**Other**

* Vertx eventLoop ThreadBlocked with ExtensionGrant [#10968](https://github.com/gravitee-io/issues/issues/10968)
* Update docker-compose to be able to run without changes [#10972](https://github.com/gravitee-io/issues/issues/10972)
* UI broken for Endpoints when user assigned role to application [#10976](https://github.com/gravitee-io/issues/issues/10976)
* STS Client is not closed in HSM implementation [#10977](https://github.com/gravitee-io/issues/issues/10977)
* Unable to update Virtual host [#10979](https://github.com/gravitee-io/issues/issues/10979)

</details>

## Gravitee Access Management 4.9.3 - November 7, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* VertX Thread Blocked when JWKS is loaded [#10932](https://github.com/gravitee-io/issues/issues/10932)
* Upgrade Spring Data R2DBC [#10936](https://github.com/gravitee-io/issues/issues/10936)
* Improve Thread Management for RDBMS backend [#10938](https://github.com/gravitee-io/issues/issues/10938)

**Other**

* Reduce log verbosity on MFA validation failure [#10903](https://github.com/gravitee-io/issues/issues/10903)

</details>

## Gravitee Access Management 4.9.2 - October 30, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* StackOverflowError when logging out [#10928](https://github.com/gravitee-io/issues/issues/10928)

**Console**

* Unable to delete a user when the IDP has been removed [#10915](https://github.com/gravitee-io/issues/issues/10915)

</details>

## Gravitee Access Management 4.9.1 - October 24, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* Account's password is expired error when using account linking [#10851](https://github.com/gravitee-io/issues/issues/10851)
* Password policy applies to LDAP IdP [#10874](https://github.com/gravitee-io/issues/issues/10874)
* Fix performance degradation introduced in 4.9.0 [#10876](https://github.com/gravitee-io/issues/issues/10876)
* Add Domain object to EL context for HTTP IDP [#10881](https://github.com/gravitee-io/issues/issues/10881)

**Management API**

* Domain deletion does not remove all entities [#10899](https://github.com/gravitee-io/issues/issues/10899)

**Console**

* Client secrets - Renew - Wording needs be altered [#10891](https://github.com/gravitee-io/issues/issues/10891)

**Other**

* Support posix groups in LDAP mappings [#10848](https://github.com/gravitee-io/issues/issues/10848)

</details>

#### Gravitee Access Management 4.9 - Oct 9, 2025 <a href="#gravitee-access-management-4.8" id="gravitee-access-management-4.8"></a>

<details>

<summary>What's new</summary>

#### OpenID provider improvement

The [OpenID identity provider ](../../guides/identity-providers/social-identity-providers/openid-connect.md)has been updated to support the `application/jwt` content type at the [UserInfo Endpoint](https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse).

The system accepts only signed JWT tokens. Signature validation is handled by the [Public Key Resolver](../../guides/identity-providers/social-identity-providers/openid-connect.md#public-key-resolver) defined in the provider's configuration.

#### Support schema with PostgreSQL backend

You can now specify the [schema](https://www.postgresql.org/docs/current/ddl-schemas.html) when Access Management is configured with a PostgreSQL backend. For more information, see the [repositories](../../getting-started/configuration/configure-repositories.md#jdbc) section.

#### Rate Limit policy

Access Management now offers a Rate Limit policy that is functionally identical to the Rate Limit policy in API Management. You can use Gravitee Expression Language to enforce a limit per client ID.

#### Audit logs

A new audit log is generated for multi-factor authentication (MFA). When a user selects the "remember device" option during the MFA challenge phase, an MFA\_REMEMBER\_DEVICE audit [event](../../guides/audit-trail.md#event-types) is created.

The improved MongoDB audit log implementation now uses secondary nodes for search requests. This behavior is [configurable](../../getting-started/configuration/configure-reporters.md#mongodb-reporter) in the `gravitee.yaml` of the Management API.

The [File Reporter](../../getting-started/configuration/configure-reporters.md#file-reporter) implementation now provides a retention duration for files. This retention time can be configured at the platform level using the `gravitee.yml` file, or directly in the UI per reporter instance.

#### Extension Grant improvement

The [Extension Grant](../../guides/auth-protocols/oauth-2.0/extension-grants.md) plugin now supports using a JWKS\_URL to retrieve the public key that processes the `assertion` parameter.

#### Events Retention

Access Management version 4.9 implements a 90-day retention policy on the events table. To achieve this, a TTL (Time-to-Live) index is created for installations that use a MongoDB backend. For installations that use an RDBMS backend, a purge service runs daily, at 11:00 PM by default.

#### Prompt password changed when password is expired

A new option is available to require users to reset their passwords after a configurable time period has elapsed since their last reset. Upon successful login, if the password has expired, users are immediately prompted to set a new password before continuing the login flow. See the [force reset password page](../../guides/login/force-reset-password-on-expiration.md) for more details.

</details>

<details>

<summary>Breaking Changes</summary>

**MongoDB search for user profile**

Starting with AM versions 4.5.20, 4.6.14, 4.7.8, and 4.8.1, GitHub issue [10573](https://github.com/gravitee-io/issues/issues/10573) was implemented to mitigate performance problems with user search requests on MongoDB. This was achieved by introducing a new option to disable case-insensitive regex search when the SCIM operators `sw`, `ew` or `co` are used.

In version 4.9.0, this option is enabled by default, making MongoDB queries for SCIM and user searches on the Management API case-sensitive. To revert to the previous behavior of case-insensitive searches, you must explicitly configure this option in the `gravitee.yaml` file:

```
legacy:
  mongodb:
    regexCaseInsensitive: true
```

Alternatively, you can specify this option as an environment variable:

```
gravitee_legacy_mongodb_regexCaseInsensitive=true
```

**Resource HTTP Factor**

The version 4.0 of the resource plugin [gravitee-am-resource-http-factor](https://download.gravitee.io/#graviteeio-ee/am/plugins/resources/gravitee-am-resource-http-factor/) has been released. This version requires AM 4.9.0 or later. The version 3.0 of the resource http factor plugin remains compatible with AM 4.9.0.

</details>
