---
description: Configuration and setup guide for user settings.
---

# User Settings

You can configure various user options:

* `user.login.defaultApplication`: `boolean` (default: `true`): Creates a new application for all new users
* `user.creation.token.expire-after`: `number` (default: `86400`): Number of seconds before the user registration token expires
* `user.reference.secret`: `32 characters` (default: `s3cR3t4grAv1t33.1Ous3D4R3f3r3nc3`): Secret used to generate a unique anonymous reference to a user; **You must change this value**
* `user.anonymize-on-delete:enabled`: `boolean` (default: `false`): If true, the user's first name, last name, and email are anonymized when a user is deleted
