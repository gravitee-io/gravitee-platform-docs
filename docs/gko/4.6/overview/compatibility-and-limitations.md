# Compatibility and Limitations

In its early iterations, the Gravitee Kubernetes Operator (GKO) focused on managing the most important aspect of any API management platform: the APIs themselves. Over time, GKO has evolved to manage API documentation pages, API access controls, API resources (such as authentication servers and caches), and more. In the future, GKO will continue to expand its reach to cover new parts of the API lifecycle.

## Compatibility

Since GKO 4.4, GKO follows a strict compatibility policy where a minor version of GKO requires the same minor version of APIM. So, GKO 4.5 is compatible with only APIM 4.5 and GKO 4.4 is compatible with GKO 4.4.

For the most part, GKO 4.3 is compatible with APIM 4.3, 4.2, and 4.1. GKO 4.3 is based on the same codebase as GKO 0.13.1 and was tagged as 4.3 to make the new support policy easier to follow.

## Known limitations and future direction

Below are some examples of resources that are not managed by GKO. Not all of these will come under GKO management, but some will. Please reach out to us if you'd like to talk about expanding GKO's scope in one of these areas.

**API-level** elements that are not managed by GKO:

* Notification settings
* Picture & background
* Alerts
* Documentation page translations
* Documentation page attached resources (aka API Media)
* Documentation pages of type LINK
* v4 API primary owner management

GKO does not manage any **environment-level** objects such as:

* Shared Policy Groups (coming soon)
* APIM dictionaries (coming soon)
* APIM environment user management (coming soon)
* Platform-level common policies
* Developer Portal themes

GKO does not manage other **Gravitee components** such as:

* Gravitee Gateway
* Gravitee Access Management
* Gravitee Alert Engine
