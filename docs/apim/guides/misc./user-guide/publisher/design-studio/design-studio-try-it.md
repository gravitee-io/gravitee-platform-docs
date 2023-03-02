<span class="label label-version">New in version 3.11</span>

# Overview

You can use Design Studio Try-it Mode to test a non deployed API. This
mode allows you to modify your API without saving or deploying it.

# Get Started With Try It Mode

1.  link:{{
    */apim/3.x/apim\_publisherguide\_design\_studio\_create.html* |
    relative\_url }}\[Design your API^\].

2.  Click **TRY IT**.

3.  Send a request to your API with whatever parameters you’d like to
    try.

# How To Test Your API Concept With Try It Mode

You can test your **API** through the HTTP client available in the **TRY
IT** tab.

image:{% link
images/apim/3.x/api-publisher-guide/design-studio/try-it/try-it-view.png
%}\[HTTP Client\]

With this client, you can call your **API,** and test and experiment
with the following:

1.  HTTP Method.

2.  Path (and query params).

3.  Headers.

4.  Request body.

image:{% link
images/apim/3.x/api-publisher-guide/design-studio/try-it/try-it-example.png
%}\[Try it example\]

# Limitations

Some features are not testable with Try It Mode:

1.  Rate Limit & Quota.

2.  Health-Check.

3.  Virtual hosts (the first host is selected).
