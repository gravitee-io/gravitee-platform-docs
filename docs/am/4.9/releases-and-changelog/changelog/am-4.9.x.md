---
description: >-
  This page contains the changelog entries for AM 4.9.0 and any future minor or
  patch AM 4.9.x releases
---

# AM 4.9.x

## Gravitee Access Management 4.9.0 - October 16, 2025

<details>

<summary>Bug fixes</summary>

**Gateway**

* France Connect V2 - Review wording of error message [#10738](https://github.com/gravitee-io/issues/issues/10738)
* Enhance idp plugin redeployment to avoid downtime [#10778](https://github.com/gravitee-io/issues/issues/10778)
* Am Is Creating Discrepancies With the Issuer Claim (`iss`) in Generated Access Tokens [#10779](https://github.com/gravitee-io/issues/issues/10779)
* NullPointerException upon first login with password expiration [#10780](https://github.com/gravitee-io/issues/issues/10780)

**Management API**

* Sanitize the redirect_uri to avoid empty segment when cockpit try to connect on the console [#10805](https://github.com/gravitee-io/issues/issues/10805)
* AM Upgrader are failing with list of mongo servers [#10850](https://github.com/gravitee-io/issues/issues/10850)
* Secrets for old applications can't be renewed [#10871](https://github.com/gravitee-io/issues/issues/10871)
* Regression in the way DataPlanes are loaded in the MAPI [#10883](https://github.com/gravitee-io/issues/issues/10883)
* API client Authentication Breakes after Upgrade to 4.8.8 [#10887](https://github.com/gravitee-io/issues/issues/10887)
* ApplicationClientSecretsUpgrader doesn't manage properly secret algorithm [#10890](https://github.com/gravitee-io/issues/issues/10890)



**Other**

* Extension Grant - Allow using a JWKS URL to retrieve public keys [#10687](https://github.com/gravitee-io/issues/issues/10687)
* [Perf] Reduce the number of threads with MongoDB Backend [#10713](https://github.com/gravitee-io/issues/issues/10713)
* Introduce common connection pool for MongoIDP [#10719](https://github.com/gravitee-io/issues/issues/10719)
* FreeMarker template error [#10722](https://github.com/gravitee-io/issues/issues/10722)
* Incorrect audit log file formatting [#10757](https://github.com/gravitee-io/issues/issues/10757)
* Closing LDAP connections properly  [#10769](https://github.com/gravitee-io/issues/issues/10769)
* Replace Bitnami Mongo [#10789](https://github.com/gravitee-io/issues/issues/10789)
* Issue AM update [#10801](https://github.com/gravitee-io/issues/issues/10801)
* Error searching for users in the UI [#10808](https://github.com/gravitee-io/issues/issues/10808)
* AWS HSM Certificate Plugin logs remain at DEBUG level despite global INFO configuration, and Helm chart indentation/mapping issue for extraLoggers. [#10824](https://github.com/gravitee-io/issues/issues/10824)
* Limit the batchSize on Mongo Reporter request [#10846](https://github.com/gravitee-io/issues/issues/10846)
* Add helm.sh/chart to pod template annotations [#10849](https://github.com/gravitee-io/issues/issues/10849)
* User registration completion UI widget is broken [#10865](https://github.com/gravitee-io/issues/issues/10865)
* Conversion session.timeout for helm value incorrect [#10867](https://github.com/gravitee-io/issues/issues/10867)
* Improve logging in EnrichAuthFlowPolicy [#10875](https://github.com/gravitee-io/issues/issues/10875)
* Avoid useless VertxHttpRequest creation [#10877](https://github.com/gravitee-io/issues/issues/10877)
* Make datasource configurable using helm values [#10884](https://github.com/gravitee-io/issues/issues/10884)

</details>


#### Gravitee Access Management 4.9 - Oct 9, 2025 <a href="#gravitee-access-management-4.8" id="gravitee-access-management-4.8"></a>

<details>

<summary>What's new</summary>

## OpenID provider improvement

The [OpenID identity provider ](../../guides/identity-providers/social-identity-providers/openid-connect.md)has been updated to support the `application/jwt` content type at the [UserInfo Endpoint](https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse).&#x20;

The system accepts only signed JWT tokens. Signature validation is handled by the [Public Key Resolver](../../guides/identity-providers/social-identity-providers/openid-connect.md#public-key-resolver) defined in the provider's configuration.

## Support schema with PostgreSQL backend

You can now specify the [schema](https://www.postgresql.org/docs/current/ddl-schemas.html) when Access Management is configured with a PostgreSQL backend. For more information, see the [repositories](../../getting-started/configuration/configure-repositories.md#jdbc) section.

## Rate Limit policy

Access Management now offers a Rate Limit policy that is functionally identical to the Rate Limit policy in API Management. You can use Gravitee Expression Language to enforce a limit per client ID.

## Audit logs

A new audit log is generated for multi-factor authentication (MFA). When a user selects the "remember device" option during the MFA challenge phase, an MFA\_REMEMBER\_DEVICE audit [event](../../guides/audit-trail.md#event-types) is created.

The improved MongoDB audit log implementation now uses secondary nodes for search requests. This behavior is [configurable](../../getting-started/configuration/configure-reporters.md#mongodb-reporter) in the `gravitee.yaml` of the Management API.

The [File Reporter](../../getting-started/configuration/configure-reporters.md#file-reporter) implementation now provides a retention duration for files. This retention time can be configured at the platform level using the `gravitee.yml` file, or directly in the UI per reporter instance.

## Extension Grant improvement

The [Extension Grant](../../guides/auth-protocols/oauth-2.0/extension-grants.md) plugin now supports using a JWKS\_URL to retrieve the public key that processes the `assertion` parameter.

## Events Retention

Access Management version 4.9 implements a 90-day retention policy on the events table. To achieve this, a TTL (Time-to-Live) index is created for installations that use a MongoDB backend. For installations that use an RDBMS backend, a purge service runs daily, at 11:00 PM by default.&#x20;

## Prompt password changed when password is expired

A new option is available to require users to reset their passwords after a configurable time period has elapsed since their last reset. Upon successful login, if the password has expired, users are immediately prompted to set a new password before continuing the login flow. See the [force reset password page](../../guides/login/force-reset-password-on-expiration.md) for more details.

</details>

<details>

<summary>Breaking Changes</summary>

### MongoDB search for user profile

Starting with AM versions 4.5.20, 4.6.14, 4.7.8, and 4.8.1, GitHub issue [10573](https://github.com/gravitee-io/issues/issues/10573) was implemented to mitigate performance problems with user search requests on MongoDB. This was achieved by introducing a new option to disable case-insensitive regex search when the SCIM operators `sw`, `ew` or `co` are used.

In version 4.9.0, this option is enabled by default, making MongoDB queries for SCIM and user searches on the Management API case-sensitive. To revert to the previous behavior of case-insensitive searches, you must explicitly configure this option in the `gravitee.yaml` file:

```
legacy:
  mongodb:
    regexCaseInsensitive: true
```

Alternatively, you can specify this option as an environment variable:&#x20;

```
gravitee_legacy_mongodb_regexCaseInsensitive=true
```

### Resource HTTP Factor

The version 4.0 of the resource plugin [gravitee-am-resource-http-factor](https://download.gravitee.io/#graviteeio-ee/am/plugins/resources/gravitee-am-resource-http-factor/) has been released. This version requires AM 4.9.0 or later. The version 3.0 of the resource http factor plugin remains compatible with AM 4.9.0.&#x20;

</details>
