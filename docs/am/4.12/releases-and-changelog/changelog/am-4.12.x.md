---
description: >-
  This page contains the changelog entries for AM 4.12.0 and any future minor or
  patch AM 4.12.x releases.
---

# AM 4.12.x

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

