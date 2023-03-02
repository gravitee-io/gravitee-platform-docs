From APIM 3.5.x, the recommended method for adding policies to plans is
with link:{{
*/apim/3.x/apim\_publisherguide\_design\_studio\_create.html#flow-policies*
| relative\_url }}\[Design Studio^\].

# Configure flows and policies in Design Studio

1.  Find your plan in the **Plans** page of the API.

    image::{% link
    images/apim/3.x/api-publisher-guide/plans-subscriptions/staging-plan.png
    %}\[\] . Click the design icon image:{% link
    images/icons/design-icon.png %}\[role="icon"\].

    APIM opens the plan in Design Studio, where you can configure flows
    and policies, as described in the link:{{
    */apim/3.x/apim\_publisherguide\_design\_studio\_create.html* |
    relative\_url }}\[Design Studio Guide\].

# Configure policies on the Policies page of a plan

In some APIs created in earlier versions of APIM, you configure policies
on the **Policies** page of a new or existing plan. You can configure a
single policy, or a chain of policies. Policy chains can be of the same
or different types.

1.  To edit an existing plan:

    1.  In APIM Console, select your API.

    2.  Click **Portal &gt; Plans**.

    3.  Click the edit icon image:{% link images/icons/edit-icon.png
        %}\[role="icon"\]. On the **Policies** page:

    4.  Choose a policy type from the list and click **ADD**.

        image::{% link
        images/apim/3.x/api-publisher-guide/plans-subscriptions/add-plan-policies.png
        %}\[\]

    5.  Depending on the policy type, specify any other required details
        of the policy.

    6.  If you want to create a policy chain, repeat the same steps for
        each policy in the chain.

2.  Click **SAVE** to save your plan.
