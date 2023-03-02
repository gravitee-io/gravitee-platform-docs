# api-consumer-ui

## Overview

This guide walks you through creating your first application and subscribing to your first API with APIM Portal. For a brief overview of how to set up your first API, see the **Publish your first API** section of the Quick Start Guide.

APIM includes several ways to access and secure an API, as described in (link:\{{ _/apim/3.x/apim\_publisherguide\_plans\_subscriptions.html_ | relative\_url \}}\[API Publisher Plans and subscriptions]).\ In\ this\ example,\ we\ will\ access\ an\ API\ using\ an\ link:\{{\ _/apim/3.x/apim\_policies\_apikey.html_\ |\ relative\_url\ \}}\[API\ Key]. Only trusted applications can access the API data by requesting an API Key. Let’s see how to create an application and generate an API Key.

## Create your application and subscribe to an API

1. link:\{{ _/apim/3.x/apim\_quickstart\_portal\_login.html_ | relative\_url \}}\[Log in to APIM Portal^].
2. Click **Applications** in the top menu.
3.  Click **CREATE AN APP** in the sub-menu.

    image::\{% link images/apim/3.x/quickstart/consume/graviteeio-create-first-app-1.png %\}\[]
4.  Give your application a name and a description. Click **NEXT**.

    image::\{% link images/apim/3.x/quickstart/consume/graviteeio-create-first-app-2.png %\}\[]
5.  Specify the type of application. Click **NEXT**.

    Because you are subscribing to an **API Key** plan, you do not need to specify a Client ID.

    image::\{% link images/apim/3.x/quickstart/consume/graviteeio-create-first-app-3.png %\}\[]
6.  Search for your API and select it.

    image::\{% link images/apim/3.x/quickstart/consume/graviteeio-create-first-app-4.png %\}\[]

    The API plan is displayed.

    image::\{% link images/apim/3.x/quickstart/consume/graviteeio-create-first-app-5.png %\}\[]
7.  Click **SUBSCRIBE**.

    image::\{% link images/apim/3.x/quickstart/consume/graviteeio-create-first-app-6.png %\}\[]
8. Click **NEXT**.
9.  You can check your application information in this summary. When you are ready, click **CREATE THE APP**.

    image::\{% link images/apim/3.x/quickstart/consume/graviteeio-create-first-app-7.png %\}\[]

    Congratulations! Your new application and subscription to the Echo API have been created.

    image::\{% link images/apim/3.x/quickstart/consume/graviteeio-create-first-app-8.png %\}\[]
