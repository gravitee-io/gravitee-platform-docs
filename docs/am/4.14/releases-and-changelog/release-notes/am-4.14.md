# AM 4.14

## Highlights
* You can now configure Lightweight JWT in an application's OAuth settings through the Management API to control which claims AM keeps in access, refresh, and ID tokens.

## Breaking Changes

## Custom plugins

## New Features

#### **Lightweight JWT Configuration in the Management API**

* When you patch an application through the Management API, you can now set Lightweight JWT in its OAuth settings: whether it's enabled, which claims AM keeps in access and refresh tokens, and which claims AM keeps in ID tokens, in addition to the reserved claims.
* Lightweight JWT is disabled by default and when its settings are absent, both claim lists are empty by default, and a listed claim is kept only if AM issues it.
* Claim lists sent in a patch replace the stored ones, a patch that disables Lightweight JWT keeps the lists it carries, and the same claim name can appear in both lists.
* Lightweight JWT settings aren't part of the Dynamic Client Registration contract, so registration updates and client secret renewals keep the stored settings.
* Claim names are validated even when Lightweight JWT is disabled: names can't be blank and can be at most 128 characters, and an invalid list fails the request with HTTP `400` that reports only the first error, checking the access and refresh token list before the ID token list.
