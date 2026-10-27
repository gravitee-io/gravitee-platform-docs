# AM 4.14

## Highlights
* Lightweight JWT lets you reduce the access, ID, and refresh tokens that AM returns to a client so they carry only the claims the application needs.

## Breaking Changes

## Custom plugins

## New Features

#### **Lightweight JWT**

* Lightweight JWT reduces the access, ID, and refresh tokens that AM returns to the client so they keep only the reserved protocol claims, plus any claims you choose to allow.
* To turn it on, enable **Enable Lightweight JWT** in the **Lightweight JWT** section of the application's OAuth2 token settings.
* Add claims to the **Allowed access and refresh token claims** and **Allowed ID token claims** lists to keep them in the reduced tokens.
* Lightweight JWT is disabled by default, so an application keeps issuing full tokens until you turn it on.
* Updating a client or renewing its secret through the registration endpoint keeps the application's Lightweight JWT settings.
