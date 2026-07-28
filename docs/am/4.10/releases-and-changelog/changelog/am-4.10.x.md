---
description: >-
  This page contains the changelog entries for AM 4.10.0 and any future minor or
  patch AM 4.10.x releases.
---

# AM 4.10.x

## Gravitee Access Management 4.10.18 - July 24, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* Not closing webClient for OIDC idp [#11632](https://github.com/gravitee-io/issues/issues/11632)
* SCIM user create returns 500 on concurrent duplicate username [#11664](https://github.com/gravitee-io/issues/issues/11664)





**Other**

* VHost domain case insensitive [#11389](https://github.com/gravitee-io/issues/issues/11389)
* Cap the maxNumber of thread when Executors.newCachedThreadPool() is used [#11608](https://github.com/gravitee-io/issues/issues/11608)
* character '&' break the URLParameterUtils [#11618](https://github.com/gravitee-io/issues/issues/11618)

</details>


## Gravitee Access Management 4.10.17 - July 13, 2026

<details>

<summary>Bug fixes</summary>



**Management API**

* Application Flows are not accessible for APPLICATION_OWNER roles [#11592](https://github.com/gravitee-io/issues/issues/11592)



**Other**

* AM Management UI CrashLoopBackOff on IPv4-only EKS [#11557](https://github.com/gravitee-io/issues/issues/11557)
* Mutualize hmac and noop Certificates across domains [#11582](https://github.com/gravitee-io/issues/issues/11582)
* Partial PATCHes of login settings cause disabled settings to be disabled in subsequent updates [#11600](https://github.com/gravitee-io/issues/issues/11600)

</details>


## Gravitee Access Management 4.10.16 - June 26, 2026

<details>

<summary>Bug fixes</summary>







**Other**

* MAPI doesn't start when HTTP idp is invalid [#11561](https://github.com/gravitee-io/issues/issues/11561)
* User search error trying to use equality filters SCIM 2.0 query syntax (filterCriteriaParser) [#11564](https://github.com/gravitee-io/issues/issues/11564)

</details>


## Gravitee Access Management 4.10.15 - June 16, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* OIDC IdP error response (query string) not propagated to client redirect URI in Auth Code PKCE flow [#11499](https://github.com/gravitee-io/issues/issues/11499)

**Other**

* Search Domain doesn't work with '_' [#11508](https://github.com/gravitee-io/issues/issues/11508)
* OIDC login fails with SignatureException due to kid: "default" collision between System and Own certificates [#11509](https://github.com/gravitee-io/issues/issues/11509)
* Filter out empty scopes in auth request [#11523](https://github.com/gravitee-io/issues/issues/11523)
* Missing user.groups property in EL [#11524](https://github.com/gravitee-io/issues/issues/11524)
* Add userId/username to error SCIM response  [#11539](https://github.com/gravitee-io/issues/issues/11539)
* Extension Grant is not managing PS256 [#11542](https://github.com/gravitee-io/issues/issues/11542)

</details>

## Gravitee Access Management 4.10.14 - June 8, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* Request-object signature pre-check NPE [#11486](https://github.com/gravitee-io/issues/issues/11486)

**Other**

* Kafka Client OAUTH not working [#11501](https://github.com/gravitee-io/issues/issues/11501)

</details>


## Gravitee Access Management 4.10.13 - June 1, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* TokenValidation should rely on the KID  [#11383](https://github.com/gravitee-io/issues/issues/11383)
* Revert KID initialization using cert alias [#11442](https://github.com/gravitee-io/issues/issues/11442)
* Addition of ClientId in the Gravitee AccessLog [#11471](https://github.com/gravitee-io/issues/issues/11471)







</details>


## Gravitee Access Management 4.10.12 - May 25, 2026

<details>

<summary>Bug fixes</summary>







**Other**

* Sync delay between GW when using DCR [#11443](https://github.com/gravitee-io/issues/issues/11443)
* UI Crash on Device Deletion [#11446](https://github.com/gravitee-io/issues/issues/11446)

</details>


## Gravitee Access Management 4.10.11 - May 15, 2026

<details>

<summary>What's new !</summary>

=**What's new!**

* UserProfile claims extension

</details>


<details>

<summary>Bug fixes</summary>







**Other**

* Improve CPU consumption with thousand of domain [#11411](https://github.com/gravitee-io/issues/issues/11411)
* Addition of access log for the Gateway [#11415](https://github.com/gravitee-io/issues/issues/11415)
* 'Master' attribute value is inconsistent when listing domains vs retrieving a specific domain [#11422](https://github.com/gravitee-io/issues/issues/11422)
* SCIM PUT/PATCH switches internal flag to false [#11425](https://github.com/gravitee-io/issues/issues/11425)
* JWT tokens are invalid with multiple values in the aud claim [#11427](https://github.com/gravitee-io/issues/issues/11427)

</details>


## Gravitee Access Management 4.10.10 - May 1, 2026

<details>

<summary>Bug fixes</summary>







**Other**

* MFA : Sent verification code to active/enrolled factor [#11318](https://github.com/gravitee-io/issues/issues/11318)
* VHost with path "/" throws ArrayIndexOutOfBoundsException [#11358](https://github.com/gravitee-io/issues/issues/11358)
* SMTP resource implict authentication [#11372](https://github.com/gravitee-io/issues/issues/11372)
* IdP Whitelist: Domain validation is case-sensitive [#11386](https://github.com/gravitee-io/issues/issues/11386)

</details>


## Gravitee Access Management 4.10.9 - April 17, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* DCR-created applications are now able to inherit domain flows by default [#11271](https://github.com/gravitee-io/issues/issues/11271)

**Other**

* Resolved issue with MFA Enrollment Stuck in PENDING_ACTIVATION [#11245](https://github.com/gravitee-io/issues/issues/11245)
* User edit form now displays all custom fields within additional information [#11333](https://github.com/gravitee-io/issues/issues/11333)

**CVE**
 
* Remediates: CVE-2026-1605, CVE-2026-33870

</details>

## Gravitee Access Management 4.10.8 - April 9, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* EnrichAuthContext ignored when session is active [#11301](https://github.com/gravitee-io/issues/issues/11301)

**Management API**

* Improve list domain response time [#11315](https://github.com/gravitee-io/issues/issues/11315)

**Console**

* User History - event names are truncated [#11290](https://github.com/gravitee-io/issues/issues/11290)
* Re: Audit Logs - Column "Target" is truncated [#11291](https://github.com/gravitee-io/issues/issues/11291)

**Other**

* Force reset password not prompting user to reset password during login [#11298](https://github.com/gravitee-io/issues/issues/11298)
* Force ordering for application search [#11309](https://github.com/gravitee-io/issues/issues/11309)

</details>


## Gravitee Access Management 4.10.7 - April 3, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* User cannot signin due to EmailFactor issue [#11304](https://github.com/gravitee-io/issues/issues/11304)

**Other**

* Create index based on timestamp for audit logs. [#11258](https://github.com/gravitee-io/issues/issues/11258)
* Error after rollback when MFA flow exist [#11282](https://github.com/gravitee-io/issues/issues/11282)
* Optimize resource for Bulk Email management [#11283](https://github.com/gravitee-io/issues/issues/11283)

</details>

## Gravitee Access Management 4.10.6 - March 27, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* Upgrade avro dependency [#11228](https://github.com/gravitee-io/issues/issues/11228)
* Improve logging of AWS HSM plugin [#11240](https://github.com/gravitee-io/issues/issues/11240)
* Limit the emailLeaseAcquiring attempt for email bulk [#11260](https://github.com/gravitee-io/issues/issues/11260)

**Management API**

* Fix API breaking change on SMTP resource update [#11244](https://github.com/gravitee-io/issues/issues/11244)

**Others**

* Update reporter script [#11262](https://github.com/gravitee-io/issues/issues/11262)

</details>

## Gravitee Access Management 4.10.5 - March 13, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* Limit the number of Thread to process Bulk Email [#11213](https://github.com/gravitee-io/issues/issues/11213)

**Console**

* Audit Logs - Column "Target" is truncated [#11200](https://github.com/gravitee-io/issues/issues/11200)

**Management API**

* IDP - Incorrect status error code for PUT request [#8917](https://github.com/gravitee-io/issues/issues/8917)

**Other**

* Out of Memory Issues caused by LD_PRELOAD [#11232](https://github.com/gravitee-io/issues/issues/11232)
* JDBC: sslMode=require without sslRootCert [#11235](https://github.com/gravitee-io/issues/issues/11235)

</details>

## Gravitee Access Management 4.10.4 - March 3, 2026

<details>

<summary>Bug fixes</summary>

**Other**

* SMTP Connection with OAuth2 Authentication [#11012](https://github.com/gravitee-io/issues/11012)
* Email BULK processing - context not closed properly [#11199](https://github.com/gravitee-io/issues/11199)

</details>

## Gravitee Access Management 4.10.3 - February 23, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* Improve reliability of email emission during SCIM Bulk [#11150](https://github.com/gravitee-io/issues/issues/11150)

**Other**

* Update Facebook IdP to latest Graph API [#11162](https://github.com/gravitee-io/issues/issues/11162)
* \[DCR] Application fails to inherit Access Token validity from AM Templates [#11178](https://github.com/gravitee-io/issues/issues/11178)

</details>

## Gravitee Access Management 4.10.2 - February 16, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* Improve Introspect throughput in 4.10 [#11108](https://github.com/gravitee-io/issues/issues/11108)
* Manage backpressure on email service for SCIM Bulk [#11138](https://github.com/gravitee-io/issues/issues/11138)
* JWKS endpoint cannot validate older tokens [#11157](https://github.com/gravitee-io/issues/issues/11157)

**Management API**

* Fixed 0 value for page field in User's search response [#11125](https://github.com/gravitee-io/issues/issues/11125)

**Console**

* Event name values in the audit log filter are truncated [#11146](https://github.com/gravitee-io/issues/issues/11146)

**Other**

* Docker - SMTP - Basic Auth - Env vars in uppercase stopping emails being sent [#11089](https://github.com/gravitee-io/issues/issues/11089)
* SCIM Bulk: use concatMapEager with configurable maxConcurrency [#11100](https://github.com/gravitee-io/issues/issues/11100)
* Send email asynchronously on PreRegistration [#11106](https://github.com/gravitee-io/issues/issues/11106)
* OpenFGA - Improve ALLOWED icon for tuples [#11110](https://github.com/gravitee-io/issues/issues/11110)

</details>

## Gravitee Access Management 4.10.1 - January 29, 2026

<details>

<summary>Bug fixes</summary>

**Other**

* ErrorDescription encoded in the errorHash [#11054](https://github.com/gravitee-io/issues/issues/11054)
* DCR: Cannot Renew Client Secret [#11058](https://github.com/gravitee-io/issues/issues/11058)
* Issue with Consent Persistence after initial denial [#11066](https://github.com/gravitee-io/issues/issues/11066)
* OIDC IdP: Add support for response\_mode=form\_post (Azure AD long redirect issue) [#11075](https://github.com/gravitee-io/issues/issues/11075)
* OpenID - id\_token flow - Cannot invoke String.indexOf%28String because "s" is null [#11079](https://github.com/gravitee-io/issues/issues/11079)
* Clean authFlowVer in the session [#11081](https://github.com/gravitee-io/issues/issues/11081)

</details>

#### Gravitee Access Management 4.10 - Jan 8, 2026 <a href="#gravitee-access-management-4.8" id="gravitee-access-management-4.8"></a>

<details>

<summary>What's new</summary>

#### Enhanced Kafka Reporting for Audit Logs

Access Management supports Kafka reporter, which enables seamless integration between your audit trails and Kafka topics. You can optimize data flow by selecting specific event types to send to your Kafka cluster.

#### Secret References in Domain-Level Plugins

AM 4.1 extends our Secret Provider capabilities beyond the global `gravitee.yaml` configuration. Administrators can utilize secret references within specific plugin configurations defined at the Domain level.

{% hint style="info" %}
This functionality is currently exclusive to the **Certificate** **Plugin**.
{% endhint %}

#### User Authentication via Certificate

Access Management now supports Certificate-Based Authentication (CBA) as a primary authentication factor. Similar to WebAuthn, CBA uses public-key cryptography to prove identity but utilizes standard X.509 digital certificates.

#### MCP Server Integration

{% hint style="warning" %}
**Tech Preview**: MCP Server support is currently in preview. Features and APIs may change in future releases. This functionality is not production-ready and you should use the feature with caution.
{% endhint %}

We are taking the first steps toward making **Model Context Protocol** (MCP) a first-class citizen within Access Management. This feature introduces a new application type designed specifically for MCP Resource Servers, enabling secure, standardized communication between AI models and your data tools.

#### Authorization Engine (OpenFGA & AuthZen)

{% hint style="warning" %}
**Tech Preview:** The OpenFGA Authorization Engine is in tech preview. Features and APIs may change in future releases. This functionality is not production-ready. Contact Gravitee to get access and discover the feature.

To get access, reach out to your Gravitee customer contact, or [book a demo](https://www.gravitee.io/demo).
{% endhint %}

In this release, we are laying the foundation for Access Management to serve as the primary Policy Decision Point (PDP) and permissions engine for Agentic AI and MCP ecosystems. This feature enables fine-grained, relationship-based access control (ReBAC) for AI tools and resources.

</details>

<details>

<summary>Breaking changes</summary>

#### Optimized Audit Logging for Client Authentication

To improve Gateway performance and reduce log storage overhead, The record of client authentication in the audit logs has been optimized.

* **Conditional Logging:** Starting in this version, successful client authentication attempts are filtered out of the audit logs by default.
* **Security Focus:** Failed authentication attempts continue to be logged in full, ensuring that potential unauthorized access or configuration issues remain visible to administrators.
* **Full Traceability (Optional):** If your compliance requirements necessitate logging every successful authentication, the previous behavior can be restored via configuration.

**Configuration Update**

To enable audit logs again for successful client authentications, update the following property in your `gravitee.yaml`:

```yaml
reporters:
  audits:
    clientAuthentication:
      success:
        enabled: true        
```

**Enhanced Introspection with Audience (aud) Support**

We have updated the OAuth2 Introspection endpoint to include the `aud` (audience) claim in its response. This enhancement allows Resource Servers such as the new MCP Servers to verify that a token was specifically intended for them, which strengthens the security of the token validation process.

**Compatibility Toggle**

While this change improves security, we recognize it may impact existing deployments that do not expect the `aud` claim in the introspection response ([Issue #3111](https://github.com/gravitee-io/issues/issues/3111)). To ensure a smooth transition, A configuration toggle has been included to disable this behavior if necessary.

To remove the `aud` claim from the introspection response, update your `gravitee.yaml` with the following configuration:

```yaml
handlers:
  oauth2:
    introspect:
      allowAudience: false
```

</details>
