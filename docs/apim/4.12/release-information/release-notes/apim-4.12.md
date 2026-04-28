# APIM 4.12

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:APIM-13822 -->
#### **JWT Policy Nested Claim Extraction**

* The JWT policy now supports dot-notation syntax (e.g., `realm_access.preferred_username` or `act.repository`) to extract user identities and client IDs from nested JWT claims.
* When a claim path contains a dot, the policy first checks for a top-level claim with that exact literal name, then traverses nested Map values if no flat claim exists, preserving backward compatibility.
* Configure nested claim extraction using the **User Claim** and **Client ID Claim** fields in the JWT policy settings—existing flat claim configurations continue to work unchanged.
<!-- /PIPELINE:APIM-13822 -->

## Improvements

## Bug Fixes
