# AM 4.13

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:AM-7022 -->
#### **Selective scope approval for OAuth 2.0 consent**

* Users can now grant or deny individual OAuth 2.0 scopes during the consent flow instead of accepting or rejecting all permissions as a single block.
* Administrators can configure applications to preselect all scopes by default or require explicit opt-in for each permission, and can mark critical scopes as mandatory to ensure they're always granted.
* The consent page displays scopes in a searchable, filterable table with bulk selection controls when more than 10 scopes are requested.
* Required scopes appear as disabled checkboxes and trigger an `access_denied` error if the user attempts to submit consent without approving them.
<!-- /PIPELINE:AM-7022 -->

## Improvements

## Bug Fixes
