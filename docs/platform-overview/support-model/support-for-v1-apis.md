---
description: This page details the go-forward strategy for supporting v1 APIs in APIM
---

# Support for v1 APIs

## Overview

This document outlines how we intend to manage and support v1 APIs in future versions of APIM. The following FAQs present the details:&#x20;

* [Can a user create v1 APIs today?](support-for-v1-apis.md#can-a-user-create-v1-apis-today)
* [What happens when APIM is updated from \~3.15 to 4.0?](support-for-v1-apis.md#what-happens-when-apim-is-updated-from-3.15-to-4.0)
* [When will v1 APIs stop running on the Gateway?](support-for-v1-apis.md#when-will-v1-apis-stop-running-on-the-gateway)
* [Why include the upgrader in the backend and not in the UI?](support-for-v1-apis.md#why-include-the-upgrader-in-the-backend-and-not-in-the-ui)
* [What will happen to users who still have v1 APIs in 5.0?](support-for-v1-apis.md#what-will-happen-to-users-who-still-have-v1-apis-in-5.0)
* [What will happen to the v1 API code?](support-for-v1-apis.md#what-will-happen-to-the-v1-api-code)

Although v1 APIs have been **deprecated**, they are still supported. Gravitee uses deprecation to publicly signal that we intend to remove the functionality in a future release.

### Can a user create v1 APIs today?

No. A user cannot create a v1 API in APIM 3.20 or 4.0. In version 3.20, a user can import a v1 API and also specify that they want to convert the API to v2. In version 4.0, users **cannot** import v1 APIs.

### What happens when APIM is updated from \~3.15 to 4.0?

Many customers are running versions of APIM that support creating v1 APIs (e.g., APIM 3.15). If these users upgrade their existing APIM environments to 4.0, the following behavior will occur:

* v1 APIs will **continue running** on the Gateway. Client applications will continue to be able to call the deployed v1 APIs.
* In the v4 UI, the API will appear in the list but be **read only**. A banner present for v1 APIs prompts the user to upgrade the API to the v2 definition.
* Currently, users can still create, publish, deprecate, and close plans for v1 APIs. We **do** plan to remove this feature, likely in 4.1.

### When will v1 APIs stop running on the Gateway?

For version 4.0, v1 APIs will **continue running** on the Gateway but will be read only. We will not prevent v1 APIs from running on the Gateway until we release APIM 5.0. The earliest release date for APIM 5.0 will be in summer of 2024.

### Why include the upgrader in the backend and not in the UI?

We expect that customers who still use and manage v1 APIs will be comfortable managing APIM through the configuration files, and devoting time to develop a v1 frontend will be at the expense of adding valuable features to the UI. We have therefore elected to keep v1 behind-the-scenes and only expose it for customers who need this particular feature.

### What will happen to users who still have v1 APIs in 5.0?

For users with v1 APIs who upgrade to 5.0, their v1 APIs will appear in the UI as in-error with an invalid version. Any running v1 APIs will be stopped and "undeployed" by the Management API, and the 5.0 Gateway will ignore v1 APIs upon start-up. The v1 upgrader will still be present and will run whenever the management API starts assuming its `enabled` property is set to `true`.

### What will happen to the v1 API code?

The code to run v1 APIs will be entirely removed from the APIM codebase. However, the v1 code from previous versions of the codebase will be obtainable from the version history in GitHub.
