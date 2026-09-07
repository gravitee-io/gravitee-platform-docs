---
description: >-
  This page contains the changelog entries for AM 4.12.0 and any future minor or
  patch AM 4.12.x releases.
---

# AM 4.12.x

## Gravitee Access Management 4.12.6 - September 3, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* Cookie tracker debbuger [#11773](https://github.com/gravitee-io/issues/issues/11773)
* An application with no token endpoint authentication method set is refused when it authenticates with a client assertion [#11782](https://github.com/gravitee-io/issues/issues/11782)
* TOTP enrollment – user redirected to OTP page after incomplete enrollment [#11787](https://github.com/gravitee-io/issues/issues/11787)

**Management API**

* Console login page returns 500 when an organization social identity provider cannot build a sign-in URL [#11771](https://github.com/gravitee-io/issues/issues/11771)





</details>


## Gravitee Access Management 4.12.5 - August 25, 2026

<details>

<summary>Bug fixes</summary>







**Other**

* Create setting to disable the reporter indexes management [#11712](https://github.com/gravitee-io/issues/issues/11712)
* DefaultReporterUpgrader [#11716](https://github.com/gravitee-io/issues/issues/11716)
* Access and refresh token batch store [#11728](https://github.com/gravitee-io/issues/issues/11728)
* JettyHttpServerProbe leaks one Vert.x NetClient per health check execution since 4.12 [#11733](https://github.com/gravitee-io/issues/issues/11733)
* ClaimRequest mapping issue [#11736](https://github.com/gravitee-io/issues/issues/11736)
* msg() expressions not resolved in "From name" of the MFA Challenge email template [#11756](https://github.com/gravitee-io/issues/issues/11756)

</details>


## Gravitee Access Management 4.12.4 - August 7, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* Convert trustedIssuer list as Map once the domain is Loaded to speedup the lookup [#11686](https://github.com/gravitee-io/issues/issues/11686)
* Improve Login performance [#11687](https://github.com/gravitee-io/issues/issues/11687)
* Avoid StackOverflowException during domain lookup [#11708](https://github.com/gravitee-io/issues/issues/11708)

**Management API**

* Permission keys cache problem [#11700](https://github.com/gravitee-io/issues/issues/11700)

**Console**

* Default Scopes and Allowed Scopes are not consistently saved during OpenID Client Registration configuration [#11684](https://github.com/gravitee-io/issues/issues/11684)

**Other**

* MSSQL 4.11 TokenRevocation issue [#11694](https://github.com/gravitee-io/issues/issues/11694)

</details>


## Gravitee Access Management 4.12.3 - July 30, 2026

<details>

<summary>Bug fixes</summary>

**Gateway**

* User is not deleted after API deletion [#11676](https://github.com/gravitee-io/issues/issues/11676)







</details>


## Gravitee Access Management 4.12.2 - July 24, 2026

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


## Gravitee Access Management 4.12.1 - July 14, 2026

<details>

<summary>Bug fixes</summary>



**Management API**

* Application Flows are not accessible for APPLICATION_OWNER roles [#11592](https://github.com/gravitee-io/issues/issues/11592)



**Other**

* AM Management UI CrashLoopBackOff on IPv4-only EKS [#11557](https://github.com/gravitee-io/issues/issues/11557)
* Mutualize hmac and noop Certificates across domains [#11582](https://github.com/gravitee-io/issues/issues/11582)
* Partial PATCHes of login settings cause disabled settings to be disabled in subsequent updates [#11600](https://github.com/gravitee-io/issues/issues/11600)
* Improve Audit Search query [#11602](https://github.com/gravitee-io/issues/issues/11602)

</details>

