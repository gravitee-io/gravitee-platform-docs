---
description: Changelogs
metaLinks:
  alternates:
    - changelog.md
---


# Changelogs
<!--INSERT_BELOW-->

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
