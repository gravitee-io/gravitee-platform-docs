# Create an Application

## Overview&#x20;

You can create applications with the New Developer Portal. Unless the API has a keyless plan, a consumer must register an application and subscribe to a published API plan to access an API. Applications act on behalf of the user.

You can create the following application types with the New Developer Portal:

* Simple. A standalone client where you manage your own client\_id. No DCR involved.
* SPA. Front-end JS apps (React, Angular, Vue) using DCR for authentication.
* Web. Server-side web apps (NET, Java) that authenticate users through DCR.
* Native. Mobile and desktop apps (iOS, Android) that authenticate through DCR.
* Backend to backend. Machine-to-machine apps (scripts, daemons, CLIs) using DCR for API access.

## Prerequisites&#x20;

* Enable the New Developer Portal. For more information about enabling the New Developer Portal, see [configure-the-new-portal.md](configure-the-new-portal.md "mention").

## Create an application

To create an application, complete the following steps:

* [#navigate-to-the-create-an-application-screen](create-an-application.md#navigate-to-the-create-an-application-screen "mention")
* [#create-an-application-1](create-an-application.md#create-an-application-1 "mention")

### Navigate to the create an application screen

1.  From the New Developer Portal, click your **profile icon**, and then click **Applications**.<br>

    <figure><img src="../../.gitbook/assets/24CEDF9D-C4AF-4AE9-85FB-B38CBB209138.jpeg" alt=""><figcaption></figcaption></figure>
2.  From the **Applications** screen, click **+ Create**.<br>

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>The Create button is visible only for users with he <code>ENVIRONMENT:APPLICATION:CREATE</code> permission.</p></div>



    <figure><img src="../../.gitbook/assets/FBEA8614-26C9-47AF-9EB3-FE0F3E1DD40C_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>

### Create an application

1. Create an application by following the steps for the application type that you want to create:

{% tabs %}
{% tab title="Simple" %}
1) In the **Application name** field, type the name of the application. For example, my first application.
2) (Optional) In the **Description (optional)** field, type a description for the application. For example, `Test`.&#x20;
3) (Optional) Configure the security for the application. To configure the security for the application, complete the following sub-steps:
   1. In the **Type** field, type the type of application. For example, `mobile` .
   2. In the **Client ID** field, type the **client\_id** of the application.
   3. (PEM Only) In the **Client Certificate (PEM Only),** type the **client\_certificate** for the application.
{% endtab %}

{% tab title="SPA" %}
1. In the **Application name** field, type the name of the application. For example, My first application.
2. (Optional) In the **Description (optional)** field, type a description for the application. For example, `Test`.&#x20;
3. Configure the security for the application. To configure the security for the application, complete the following sub-steps:
   1. (Optional) Depending on the grant types that your application uses, turn off the **Authorization Code** toggle.
   2. (Optional) Depending on the grant types that your application uses, turn on the **Implicit** toggle.
   3. In the **Redirect URIs** field, type the redirect URIs for the application.
   4. (PEM Only) In the **Client Certificate (PEM Only),** type the **client\_certificate** for the application.
   5. In the **Additional Client Metadata** (optional) field, type the **KEY** and **VALUE** names.&#x20;
{% endtab %}

{% tab title="Web" %}
1. In the **Application name** field, type the name of the application. For example, My first application.
2. (Optional) In the **Description (optional)** field, type a description for the application. For example, `Test`.&#x20;
3. Configure the security for the application. To configure the security for the application, complete the following sub-steps:
   1. (Optional) Depending on the grant types that your application uses, turn on the **Refresh Token** toggle.
   2. (Optional) Depending on the grant types that your application uses, turn on the **Implicit** (**Hybrid)** toggle.
   3. In the **Redirect URIs** field, type the redirect URIs for the application.
   4. (PEM Only) In the **Client Certificate (PEM Only),** type the **client\_certificate** for the application.
   5. (Optional) In the **Additional Client Metadata** (optional) field, type the **KEY** and **VALUE** names.&#x20;
{% endtab %}

{% tab title="Native" %}
1. In the **Application name** field, type the name of the application. For example, My first application.
2. (Optional) In the **Description (optional)** field, type a description for the application. For example, `Test`.&#x20;
3. Configure the security for the application. To configure the security for the application, complete the following sub-steps:
   1. (Optional) Depending on the grant types that your application uses, turn on the **Refresh Token** toggle.
   2. (Optional) Depending on the grant types that your application uses, turn on the **Resource Owner Password** toggle.
   3. (Optional) Depending on the grant types that your application uses, turn on the **Implicit** (**Hybrid)** toggle.
   4. In the **Redirect URIs** field, type the redirect URIs for the application.
   5. (PEM Only) In the **Client Certificate (PEM Only),** type the **client\_certificate** for the application.
   6. (Optional) In the **Additional Client Metadata** (optional) field, type the **KEY** and **VALUE** names.&#x20;
{% endtab %}

{% tab title="Backend to Backend" %}
1. In the **Application name** field, type the name of the application. For example, My first application.
2. (Optional) In the **Description (optional)** field, type a description for the application. For example, `Test`.&#x20;
3. (Optional) Configure the security for the application. To configure the security for the application, complete the following sub-steps:
   1. (PEM Only) In the **Client Certificate (PEM Only),** type the **client\_certificate** for the application.
   2. In the **Additional Client Metadata** (optional) field, type the **KEY** and **VALUE** names.&#x20;
{% endtab %}
{% endtabs %}

2.  Click **Create**.<br>

    <figure><img src="../../.gitbook/assets/image (176).png" alt=""><figcaption></figcaption></figure>

## Verification&#x20;

You are brought to the application's **Analytics & Logs** screen.&#x20;

<figure><img src="../../.gitbook/assets/0751EBF1-6A7D-4444-863A-D489A3BB2263_1_201_a.jpeg" alt=""><figcaption></figcaption></figure>
