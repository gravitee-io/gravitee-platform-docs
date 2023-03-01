# Overview

You can define dictionaries in APIM to reuse sets of properties in APIs.
While API Publishers can create properties for their own APIs,
dictionaries provide a way to manage properties independently of
individual APIs, making it possible to apply them across APIs and
maintain them globally by a different user profile, such as an
administrator.

Dictionary properties are based on key-value pairs. You can create two
types of dictionaries:

-   Manual dictionaries, with static properties defined manually at
    dictionary creation time

-   Dynamic dictionaries, with properties updated continually, based on
    a schedule and source URL defined at dictionary creation time

Dictionaries need to be deployed to APIM Gateway before you can use
them. You can see the date and time the dictionary was last deployed in
the dictionary list:

image:{% link
images/apim/3.x/installation/configuration/configure-dict-list.png
%}\[\]

You can access dictionary properties using the link:{{
*/apim/3.x/apim\_publisherguide\_expression\_language.html* |
relative\_url }}\[Expression Language^\] `#dictionaries` statement.

See also: link:{{
*/apim/3.x/apim\_publisherguide\_design\_studio\_create.html#api-properties*
| relative\_url }}\[Define properties for your API flows^\].

# How are dictionaries used?

You can use dictionaries anywhere in APIM where link:{{
*/apim/3.x/apim\_publisherguide\_expression\_language.html* |
relative\_url }}\[Gravitee Expression Language^\] is supported, such as
when defining policies for API flows. You can access dictionary
properties with the Expression Language statement `#dictionaries`.

# Create a new dictionary

1.  Click **Settings &gt; Dictionaries**.

2.  Click the plus icon images:icons/plus-icon.png\[role="icon"\].

3.  Enter a name and description for the dictionary.

4.  Select a **Manual** or **Dynamic** dictionary type.

## Create a manual dictionary

Your manual dictionary is not available until you click **DEPLOY**.

1.  Click **CREATE**, then specify the properties for the dictionary as
    key-value pairs.

2.  Click **SAVE PROPERTIES** when you are done, and **DEPLOY** to
    deploy your dictionary to APIM Gateway.

## Create a dynamic dictionary

Your dynamic dictionary does not start updating properties until you
click **START**.

1.  Specify the schedule for the trigger to create dynamic properties.

2.  In the **Provider** section, specify the details of the source of
    the properties:

    -   A **Type** of **Custom (HTTP)**.

    -   The URL and method of the API providing the properties.

    -   The request body.

    -   One or more HTTP headers.

    -   The transformation to apply to the response, in JOLT format.

3.  Click **CREATE** to create the dictionary.

4.  When you are ready to begin retrieving the dynamic properties, click
    **START**.

    APIM retrieves the properties at the interval defined and lists them
    in the **Properties** section.

5.  Select any properties you want to delete and click **DELETE**.

6.  Click **DEPLOY** when you are ready to deploy your dictionary to
    APIM Gateway.

The following example creates a list of properties based on extracting
the names and versions from the JSON at the defined URL and assigning
them to the property keys and values:

image:{% link
images/apim/3.x/installation/configuration/configure-dict-dynamic-property-def.png
%}\[\]

When you click **START**, the properties are added to the list according
to the defined schedule:

image:{% link
images/apim/3.x/installation/configuration/configure-dict-dynamic-property-list.png
%}\[\]
