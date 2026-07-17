---
description: Release notes for Gravitee Access Management 4.13, including highlights, breaking changes, new features, improvements, and bug fixes.
---

# AM 4.13

## Highlights

## Breaking Changes

## New Features

#### Consent page scope selection and required scopes

* Administrators can now configure whether scopes are preselected or require explicit opt-in on the OAuth 2.0 consent page. This gives organizations control over how you grant permissions during authorization flows.
* Required scopes can be marked as mandatory. These permissions are always checked and disabled on the consent page, and you cannot proceed without granting them.
* The consent page automatically adapts its layout based on the number of scopes. Applications with more than 10 scopes and at least one required scope display required permissions in a collapsible section, while optional scopes appear in a searchable, filterable table with bulk-select controls.
* To configure these settings, in the Management Console, navigate to **Applications → \[Your Application] → Settings → OAuth2 / OIDC → Scopes**.

## Improvements

## Bug Fixes
