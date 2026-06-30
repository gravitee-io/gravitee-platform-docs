---
description: Changelogs
metaLinks:
  alternates:
    - changelog.md
---


# Changelogs
<!--INSERT_BELOW-->
## v1.0.0

### Features
* feat: Add multiple certificate support and rotation acceptance test
* feat: allow binding groups to APIs and Applications
* feat: custom API key field
* feat: dictionary
* feat: export to HCL
* feat: groups
* feat: manage API Keys with revocation
* feat: support of API console notifications
* feat: webhook APIs
### Bug Fixes
* fix: Remove the beta status
* fix: add an example for HTTP Proxy with shared endpoint configuration
* fix: add branch name to slack notifications
* fix: add missing fields for analytics and native plan
* fix: forbid changes to immutable fields and add test for them
* fix: handle trailing slash in listener
* fix: ssl changes in APIM
### Other
* docs: add link and description for OpenTofu prerequisite
* docs: move issue tracking to contribution doc


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
