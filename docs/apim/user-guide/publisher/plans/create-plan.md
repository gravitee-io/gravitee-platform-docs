# create-plan

There are two ways to create a plan in APIM.

## Create a plan when you create your API

You can create a plan as part of creating an API.

image::

\[]

Learn more about creating plans using this method in link:\{{ _/apim/3.x/apim\_publisherguide\_create\_apis.html_ | relative\_url \}}\[Create APIs^].

Plans you create as part of the API creation process are more limited in scope than plans created using the method below. You can use this method to get up and running quickly, then go back and update the plan later if needed.

## Create or update a plan for an existing API

You can select an existing API and create or update plans for it.

image::

\[]

To create or update a plan for an existing API:

1. Click **APIs** and select your API.
2. Click **Portal > Plans**.
3.  Click the edit icon image:\{% link images/icons/edit-icon.png %\}\[role="icon"] on an existing plan, or click the plus icon image:

    \[role="icon"] at the bottom of the **Plans** page.
4.  On the **Define** page, enter the plan definition:

    image::\{% link images/apim/3.x/api-publisher-guide/plans-subscriptions/create-plan-define.png %\}\[] .. Enter a name and description. .. In **Characteristics**, enter labels you want to use to tag the plan. .. Select a page containing the general conditions of use.

    You must create the page first. Learn more about link:\{{ _/apim/3.x/apim\_publisherguide\_plan\_general\_conditions.html#create\_a\_general\_conditions\_page_ | relative\_url \}}\[creating a general conditions of use page]

    1. If you want subscriptions to be validated without manual intervention, toggle on the **Auto validate subscription** option.
    2. If you require consumers to provide a comment when subscribing to the plan, toggle on the **Consumer must provide a comment when subscribing to the plan** option. You can also provide a custom message to display to consumers (for example, ask them to provide specific information in their comment).
    3. In **Deployment**, enter details of sharding tags.
    4. In **Access Control**, select groups which are not allowed to subscribe to the plan.
5. Click **NEXT** to link:\{{ _/apim/3.x/apim\_publisherguide\_plan\_security.html#configure\_security_ | relative\_url \}}\[configure plan security].
