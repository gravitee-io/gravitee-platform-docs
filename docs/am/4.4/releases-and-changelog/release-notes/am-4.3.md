---
description: >-
  This article covers the new features released in Gravitee Access Management
  4.3
hidden: true
---

# AM 4.3

## Audit logs

Gravitee 4.3 captures audit logs for client authentications and MFA events so that an AM admin can understand where an authentication flow fails. Audit entries are written for each occurrence of the events listed below.

**Client authentication**

* Authentication success or failure
* Token creation (sign in, refresh, step-up)
  * The tokenId reference and number of tokens created are also logged
* Token provisioning (refresh, new sign in, etc.)

**MFA events**

* MFA enrolled
* MFA successful
* Code sent
* Wrong code
* (Check for Brute Force event)

To learn more, refer to the [Audit Trail](docs/am/4.4/guides/audit-trail.md) documentation.
