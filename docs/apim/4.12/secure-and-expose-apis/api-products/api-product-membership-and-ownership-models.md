# API Product Membership and Ownership Models

## Key Concepts

### Primary Owner Mode

The primary owner mode determines whether an API Product's primary owner must be a user, a group, or either. The mode is configured globally via the `api.product.primary.owner.mode` parameter and defaults to `HYBRID`.

* **USER mode**: Only individual users can be primary owners.
* **GROUP mode**: Only groups with at least one member holding a PRIMARY_OWNER role for API_PRODUCT scope can be primary owners.
* **HYBRID mode**: Both users and groups are permitted as primary owners.

The primary owner mode is read at API Product creation and does not retroactively affect existing products. To change the primary owner of an existing product, use the Transfer Ownership action.

### Direct and Inherited Members

API Products support two membership types:

* **Direct members**: Added individually with specific roles. Direct members appear in the members table with editable roles (except for the primary owner).
* **Inherited members**: Derived from attached groups. Inherited members are displayed in read-only cards below the direct members table, grouped by their source group. Role changes for inherited members must be made in the group management UI.

When a user is both a direct member and a member through a group, their effective role is the maximum of their direct role and all group roles.

{% hint style="info" %}
Detaching a group removes inherited access for its members on that product, but does not remove direct memberships.
{% endhint %}

### Transfer Ownership

Transferring ownership reassigns the primary owner role to a new user or group and assigns a new role to the current primary owner. The transfer requires either a new primary owner ID (technical identifier) or a user reference (identity provider reference). The current primary owner cannot retain the PRIMARY_OWNER role after the transfer.

When transferring from a group primary owner, the group remains attached to the API Product. This differs from API ownership transfers, which remove the group.
