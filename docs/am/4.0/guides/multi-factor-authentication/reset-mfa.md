---
description: Configuration guide for Challenge.
---

# Reset MFA

## Overview

If users lose their mobile device or can’t use their authenticator application for any reason, they can ask the security domain administrator to reset their multi-factor authentication (MFA) devices. The MFA factors associated with their user will be removed and MFA configuration screens (Enroll and Challenge) will be displayed during the next login attempt.

## Remove user MFA factors

1. Log in to AM Console.
2. Click **Settings > Users**.
3. Select the user and click the **Multi-Factor Authentication** tab.
4.  Select the MFA factor you want to remove and click the remove icon ![remove icon](https://docs.gravitee.io/images/icons/remove-icon.png).

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-mfa-factor-reset.png" alt=""><figcaption><p>MFA factors</p></figcaption></figure>

You can also reset a user’s MFA with AM API:

{% code overflow="wrap" %}
```sh
curl -H "Authorization: Bearer :accessToken" \
-X DELETE http://GRAVITEEIO-AM-MGT-API-HOST/management/organizations/DEFAULT/environments/DEFAULT/domains/:domainId/users/:userId/factors/:factorId
```
{% endcode %}
