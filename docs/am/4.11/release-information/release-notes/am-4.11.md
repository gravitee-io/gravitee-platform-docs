# AM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-6321 -->
#### **Protected Resource Management and Token Exchange**

* Protected Resources now support secret management, certificate binding, and role-based membership controls for secure server-to-server authentication.
* MCP Servers can exchange subject tokens (access, refresh, ID, or JWT) for new access tokens using the `urn:ietf:params:oauth:grant-type:token-exchange` grant type, with inherited expiration constraints.
* Secret lifecycle operations include creation, renewal, and deletion via dedicated API endpoints, with automatic cleanup when the last secret reference is removed.
* Certificate-based authentication is supported through domain certificate binding, enabling mTLS authentication for Protected Resources.
* Membership management allows assigning users or groups with specific roles to control access to Protected Resource configuration and secrets.
<!-- /PIPELINE:AM-6321 -->

## Improvements

## Bug Fixes
