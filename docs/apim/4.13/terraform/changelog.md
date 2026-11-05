---
description: Changelogs
metaLinks:
  alternates:
    - changelog.md
---


# Terraform changelog
<!--INSERT_BELOW-->
## v1.2.0

### Features
* feat(portal): add the apim_portal resource and data source to manage a next-gen developer portal, its top navigation bar and its active theme
* feat(portal-listing): add the apim_portal_listing resource and data source to publish APIs in the portal navigation
* feat(documentation-portal): add the apim_documentation_portal resource and data source for portal pages and the homepage
* feat(documentation-api): add the apim_documentation_api resource and data source for API documentation pages
* feat(portal-link): add the apim_portal_link resource and data source for links in the portal navigation
* feat(api-link): add the apim_api_link resource and data source for links in the API documentation
* feat(portal-theme): add the apim_portal_theme resource and data source
* feat(apiv4): add portal_navigation and the APIM 4.13 settings path_mappings, request_validation, cors.allow_private_network, connection_events and tracing.redaction
* feat(dictionary): add encrypted_properties to manual dictionaries and encrypt_on_fetch to dynamic dictionaries


## v1.1.0

### Features
* feat(apiv4,application): add ignore_groups to leave groups to the Console
* feat(group): add default_member_roles and ignore_members
* feat: bring support for MCP proxies

### Bug Fixes
* fix(GKO-3100): suppress empty response_templates.headers map drift
* fix(apiv4): keep the override_access APIM stores when it is not configured
* fix(apiv4): reject a console notification without events at plan time
* fix(cloud): validate resource scope against cloud token at apply time
* fix(dictionary): mark HTTP provider header values as sensitive
* fix(group,apiv4,application): keep plans and imports clean when the platform owns members or groups
* fix(mcp): rename connection and send authentication write-only
* fix: send X-Gravitee-Set-Hrid on Terraform 1.16 export import

### Other
* docs(guides): name the strings a secret URI stands for
* test(apiv4): ignore override_access on import verification
* test: add test for groovy policy idempotency


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
