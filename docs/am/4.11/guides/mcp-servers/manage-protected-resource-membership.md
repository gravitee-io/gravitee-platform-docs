### Add a member

Add a member to delegate management responsibilities for a Protected Resource.

1. Call `POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members` with the following request body:

{% hint style="info" %}
This operation requires the `PROTECTED_RESOURCE_MEMBER[CREATE]` permission.
{% endhint %}

### Remove a member

Remove a member from a Protected Resource.

1. Call `DELETE /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources/{protected-resource}/members/{member}`.

{% hint style="info" %}
This operation requires the `PROTECTED_RESOURCE_MEMBER[DELETE]` permission.
{% endhint %}

Membership changes are audited and reflected in the UI's member management interface.
