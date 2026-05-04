# APIM 4.12

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:APIM-13752 -->
#### **Hazelcast Rate Limit Repository**

* The Hazelcast rate limit repository is now available as an alternative to Redis for distributed rate limiting across gateway instances.
* Supports both standalone deployments (TCP-IP discovery) and Kubernetes environments (automatic service discovery via the Helm chart).
* Configure by setting `ratelimit.type=hazelcast` in `gravitee.yml` and providing a `hazelcast-ratelimit.xml` configuration file (sample included in the distribution).
* Kubernetes deployments using the Helm chart automatically provision the required Service, RBAC permissions, and discovery configuration when `apim.managedServiceAccount=true`.
* When RBAC is disabled, each gateway pod operates as a single-member cluster, which multiplies rate limit budgets by the replica count.
<!-- /PIPELINE:APIM-13752 -->

<!-- PIPELINE:APIM-13822 -->
#### **JWT Policy Nested Claim Extraction**

* The JWT policy now supports dot-notation syntax (e.g., `realm_access.preferred_username` or `act.repository`) to extract user identities and client IDs from nested JWT claims.
* When a claim path contains a dot, the policy first checks for a top-level claim with that exact literal name, then traverses nested Map values if no flat claim exists, preserving backward compatibility.
* Configure nested claim extraction using the **User Claim** and **Client ID Claim** fields in the JWT policy settings—existing flat claim configurations continue to work unchanged.
<!-- /PIPELINE:APIM-13822 -->


## Improvements


<!-- PIPELINE:APIM-13462 -->
#### **Policy Description Tracing**

* Policy execution spans in OpenTelemetry traces now include a `gravitee.policy.description` attribute when verbose tracing is enabled. This feature improves observability and troubleshooting.
* The description is populated from the Description field configured on each policy step in API flows and Shared Policy Groups.
* The attribute is only emitted when a non-blank description is set and verbose tracing is enabled at both the API and gateway level.
* Applies to v2 APIs, v4 HTTP/Proxy APIs, v4 Message APIs, and Shared Policy Groups.
<!-- /PIPELINE:APIM-13462 -->

## Bug Fixes
