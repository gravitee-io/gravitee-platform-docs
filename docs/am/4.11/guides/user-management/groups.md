# Groups

## Manage groups

### List groups

1. Log in to AM Console.
2.  Search for groups by clicking **Groups**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-search-groups.png" alt=""><figcaption><p>List of groups</p></figcaption></figure>

### Create a new group

You create groups in a security domain.

1. Log in to AM Console.
2. Click **Settings > Groups**.
3. Click the plus icon ![plus icon](https://docs.gravitee.io/images/icons/plus-icon.png).
4. Give your group a **Name** and click **SAVE**.
5. You will be redirected to the new group’s page.

### Manage members

You can add an new member to your group as follows:

1. In AM Console, click **Settings > Groups**.
2. Select your group, and in the **Members** tab, click **Add members**.
3.  Search for users by username, then click **Add**.

    <figure><img src="https://docs.gravitee.io/images/am/current/graviteeio-am-userguide-um-add-member.png" alt=""><figcaption><p>Add users to group</p></figcaption></figure>

{% hint style="info" %}
Currently, only users created by AM API or the SCIM protocol and external users who have already logged in can be found.
{% endhint %}

### Group roles

You can assign roles to a group in the **Roles** tab. Each member of this group will automatically have these roles after each authentication.
