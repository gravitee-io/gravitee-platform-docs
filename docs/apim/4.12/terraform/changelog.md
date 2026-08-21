---
description: Changelogs
metaLinks:
  alternates:
    - changelog.md
---


# Changelogs
<!--INSERT_BELOW-->
## v1.0.1

### Other
* a6b6e110fdffff088e84bbe008ac64252af990b8 docs: document commitlint rules in AGENTS.md
* d07e03a221210c33664e3c3295902300b30eacea docs: refresh CLAUDE.md architecture and CI matrix details
* 5de846a5b9deb721ceeab83d7ac484a8bc7ec395 test: add test for groovy policy idempotency



## v1.0.0

### Features

* Add multiple certificate support and rotation acceptance test
* Allow binding groups to APIs and Applications
* Custom API key field
* Dictionary
* Export to HCL
* Groups
* Manage API Keys with revocation
* Support of API console notifications
* Webhook APIs

### Bug Fixes

* Remove the beta status
* Add an example for HTTP Proxy with shared endpoint configuration
* Add branch name to Slack notifications
* Add missing fields for analytics and native plan
* Forbid changes to immutable fields and add test for them
* Handle trailing slash in listener
* SSL changes in APIM

### Documentation

* Add link and description for OpenTofu prerequisite
* Move issue tracking to contribution doc


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
