---
hidden: true
noIndex: true
---

# Remote URL Import: Concepts and Security

## Overview

API Import from Remote URL enables administrators to create or update v4 APIs by fetching Gravitee API definitions or OpenAPI specifications from remote HTTP(S) endpoints. This feature streamlines API lifecycle management when definitions are hosted in version control systems, CDNs, or internal repositories.

## Key Concepts

Instead of uploading a local file, you provide the URL of a Gravitee API definition or an OpenAPI specification, and Gravitee retrieves it for you. A remote URL can be used both when creating a new API and when updating an existing one. When you update an API from a remote URL, the API you selected is the one that gets updated — any identifier contained in the fetched file is ignored.

## Security

Because this feature fetches content from URLs you provide, administrators can control where imports are allowed to come from:

* **Allowed URLs**: Restrict imports to an approved list of trusted URLs.
* **Private address protection**: Block imports from private, internal, or loopback addresses so the feature cannot be used to reach internal systems.

These protections are configurable and are not enabled by default, so administrators should configure them to match their organization's security requirements.

## Prerequisites

* **v4 API support**: Remote URL import is available only for v4 APIs. v2 APIs are not supported.
* **Network reachability**: Gravitee must be able to reach the remote URL over HTTP(S).
* **Permissions**: Users need permission to create APIs in the environment to import a new API, or permission to update the target API to update an existing one.
