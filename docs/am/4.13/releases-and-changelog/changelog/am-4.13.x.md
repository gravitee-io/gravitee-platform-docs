---
hidden: false
noIndex: false
description: >-
  This page contains the changelog entries for AM 4.13.0 and any future minor or
  patch AM 4.13.x releases.
---

# AM 4.13.x

## Gravitee Access Management 4.13.7 - November 23, 2026

<details>

<summary>What's new !</summary>



</details>


<details>

<summary>Bug fixes</summary>

**Other**

* This update resolves security fixes.




</details>


## Gravitee Access Management 4.13.6 - November 20, 2026

<details>

<summary>Bug fixes</summary>

**Other**


* This update resolves security fixes.
* Recovery Code factor's selection rule is never evaluated [#12063](https://github.com/gravitee-io/issues/issues/12063)
* SCIM Audit's Actor field missing [#12065](https://github.com/gravitee-io/issues/issues/12065)

</details>


## Gravitee Access Management 4.13.5 - November 16, 2026

<details>

<summary>Bug fixes</summary>

**Other**


* This update resolves security fixes.


</details>


## Gravitee Access Management 4.13.4 - November 16, 2026

<details>

<summary>Bug fixes</summary>




**Gateway**

* Token exchange with User Binding Mappings can cause NPE with postgresdb [#11850](https://github.com/gravitee-io/issues/issues/11850)




**Other**

* [AM Gateway] Support X-Forwarded-* headers for virtual host routing behind a proxy [#12006](https://github.com/gravitee-io/issues/issues/12006)

</details>


## Gravitee Access Management 4.13.3 - November 4, 2026

<details>

<summary>Bug fixes</summary>







**Other**

* [Gateway] Race condition in KryoSecureSecretsCache: concurrent reads of the same cached secret fail, domain left without certificate (empty JWKS / 503) [#11992](https://github.com/gravitee-io/issues/issues/11992)
* Wildcard search does not escape special characters (Mongo and JDBC) [#12007](https://github.com/gravitee-io/issues/issues/12007)
* Loading all domain scopes exhausts the JDBC pool [#12010](https://github.com/gravitee-io/issues/issues/12010)

</details>


## Gravitee Access Management 4.13.2 - October 29, 2026

<details>

<summary>Bug fixes</summary>







**Other**

* Kafka reporter NPE on DOMAIN audits without a target [#11846](https://github.com/gravitee-io/issues/issues/11846)
* JDBC audit reporter retries an unstorable batch forever [#11853](https://github.com/gravitee-io/issues/issues/11853)
* [JDBC] Concurrent logouts duplicate user attributes rows [#11960](https://github.com/gravitee-io/issues/issues/11960)
* Deleting a domain does not delete its bot detections [#11969](https://github.com/gravitee-io/issues/issues/11969)
* Disabled Connect flow aborts loading of the remaining domain flows on gateway startup. [#11990](https://github.com/gravitee-io/issues/issues/11990)

</details>


## Gravitee Access Management 4.13.1 - October 23, 2026

<details>

<summary>Bug fixes</summary>

* This update resolves security fixes.

</details>

