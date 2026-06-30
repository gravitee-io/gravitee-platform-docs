---
description: Changelogs
metaLinks:
  alternates:
    - changelog.md
---


# Changelogs
<!--INSERT_BELOW-->
## v1.0.0

## Changelog
### Features
* 31db8fb281f0941c85feb0350722753ef76450a9 feat: Add Kubernetes kind cluster setup for local development and testing
* a99dca58576448d3f1ed20ff12b127d932980a66 feat: Add multiple certificate support and rotation acceptance test
* 3fb1d0fb4f500deb3b11f51132ea767fdeb011a6 feat: allow binding groups to APIs and Applications
* 0877efab2f5fc10204786f41932c06d7efb6279b feat: custom API key field
* f567429845c89b533afd8d2dbf866d6882f2a621 feat: dictionary
* 11a08eb4dc470fff8b6b07673cde7251bcce6a05 feat: export to HCL
* 779dacac4fd95892c78299a982e3767c4a152cb1 feat: groups
* 8ece8b1f3057c33443bd85dc930fe3a026409754 feat: manage API Keys with revocation
* 60ba6fedc8c0dab30434c76194d616b5ac00979d feat: support of API console notifications
* 324a80b7547c7a729f7b3e22479c34f962f0adb5 feat: webhook APIs
### Bug Fixes
* 8db0db5ccaff8705f93c8fb1f1331c860a468a35 fix: Remove the beta status
* 768f17ca14b538d83e0fb11bbdf7adc0b9a1aaca fix: add an example for HTTP Proxy with shared endpoint configuration
* aaa60413d5f6f42f5a3b98f0c123accc0202eeb4 fix: add branch name to slack notifications
* bce6ff753a7f88f1366ff992e588df8f7b0faa26 fix: add default name to acceptance test
* 449535079e0d8e7f51ce7a917523f5cbee4b42db fix: add empty metadata for update
* 338014744fd1ca852d1e2ad0589a87c0dd23c721 fix: add missing fields for analytics and native plan
* c3ed60aaee31fb348a7aa0cee2e3560a38dfc2c2 fix: add timeout to http client in export_test.go
* d7252e9844137014d94f2702d9ef42af4b34a486 fix: apply PoC changes in OAS + overlay
* 34b1305caebb2339812db566efcd0126eb4cd4ac fix: apply test exclusion to Tofu tests
* cb5273a5da006dd54e4f2c67a4b3b9393f60dc95 fix: bits and bobc
* 931e5e9eab97acbb29f82bc306da6e8f5eb8976e fix: failing unit tests
* 22ef1ebd4196695512bfabb3416b300ad8edd79c fix: forbid changes to immutable fields and add test for them
* ada0aad61754dc497b1fe0c8156ced3e440cd82c fix: forgotten section in the README.md for APIM
* 11567bc92bdc35bd7ce0cf6418d98df7850e5bff fix: gemini fixes
* 09bb97ac3be90b6c11a63da16f6200ef0e6a908b fix: handle trailing slash in listener
* 186681828791d555cd32c70c72e432d764cae515 fix: ignore fetcher test on master
* 7ce27c7aa544083b0af551d75d7c596699df9b4b fix: oas check branch name
* c31cf245294ca72491010d37ba7d5283d9431147 fix: provisioning
* bbcee81259833040064f1bd2d019296f049467cd fix: refactor code to use common importStateIDFunc
* cf27c81b4562e21d626cf23dbc2e8aeb961b5e51 fix: regenerate with latest and without build optimization
* 7577c7c74e02b32d47f762ff8d597fbd8567b42c fix: remove archi add apim in CODEOWNERS
* 1666d1496271c79371b68855a3e3fa57bb936f90 fix: review
* efc41f196202028103f65b0e4ffda358d7bbdd62 fix: set up minimal image/chart to speed up tests
* debae449f022824bf231b9c74ea15155cf585ebf fix: skip example use-cases and tutorials for unsupported versions
* 4f832aee7441d654cdc27093058a65ada94a070a fix: ssl changes in APIM
* 46a861e3c91752950055c54446fa40cd98f794f5 fix: sync OAS
* 27666a18b0895a5c98d47c099110c517a117ff01 fix: update OAS and add overlay for new flow step attribute
* 051d813afe66a0c68b6314237c7e4c42fe280bfc fix: update OAS and fix test API_KEY added to enum
### Other
* 4028c26b48d35008d78e3a7a5a728148567cc213 docs: add instructions for running kind with a released version
* 53c2f4a36fcc366c619a24dfcc5951983714e38d docs: add link and description for OpenTofu prerequisite
* 8e5f8b5f81ebca66183c9c70532e1af5c0ff80b6 docs: move issue tracking to contribution doc
* 19e9e689d062cc967406347ced8a7fab12c68def test: add acceptance tests for subscription metadata
* 48dd1e5af4982ec187653be7be05ee8785b13aac test: add new test case for settings both app and oauth
* 3c7f92534240d4733dacbd135ef8123e5a2b6e74 test: add new test cases for custom types and plan modifiers
* aa66c57d4e2b42dd989fcc53c47c6502631bdb16 test: add unit tests for Immutable plan modifier
* c559f8eb4042169804f2583fc835ded80e06e762 test: fix semaphore direction
* f99f9cbbafd689800219f179fff74b38277bf142 test: skip export test for image tag 4.9 and 4.10
* 54f7942b5feae07967d9be0f838b49e26d5402a7 test: skip export test for image tag 4.9 and 4.10
* 3adf1f2df8259fd0bf10bc842d8c3dd7c480464d test: skip immutable fields for 4.9




## 0.5.x

### Features

* Application supports multiple mTLS client certificates with optional start/end dates
* Subscription metadata support
* Experimental: API HCL export

### Improvements

* More tutorials in the registry docs
* `failure_condition` and `force_next_endpoint_on_failure` have been added to the API's failover configuration

### Bugs

* Subscription `plan_hrid` update is silently ignored by the API

### Notable changes

* The endpoint name is now mandatory
* Flow phase, hence flow property `connect` has been renamed to `entrypoint_connect` for `NATIVE` APIs
