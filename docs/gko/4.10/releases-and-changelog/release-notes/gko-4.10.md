---
Gravitee Kubernetes Operator 4.10 Release Notes.
---

# GKO 4.10

## Highlights

This release brings bug fixes and new features focused on HTTP Client configuration.

## New Features

**GKO HTTP Client configuration enhancements**

* Management APIs connection through proxy. 
* Support for custom CA certificates outside of `/etc/ssl/certs`.
* Connection timeout

Refer to the Helm Chart section to know how to configure proxy URL & auth, timeouts and CAs.
All of the above were back-ported to 4.8.x and 4.9.x versions of GKO.

**Windowed Count Sample Strategy**

This release adds support for the Windowed Count sampling strategy for message APIs.