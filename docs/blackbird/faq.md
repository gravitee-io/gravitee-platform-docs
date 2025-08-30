# FAQ

## What are the main features of Blackbird?

Blackbird provides the following primary features:

* **Custom API specifications:** Use AI to generate and edit API specifications based on your use case.
* **API mocks:** Use dynamic or static mocking instances that enable parallel development of your frontend and backend components.
* **API code generation:** Covert your API specification into boilerplate code to help you get started with testing.
* **Code run and debug options:** Use a local container that uses rerouted traffic from the cloud to run and debug your code.
* **Code deployment:** Use a containerized environment to run and test your code in a production-like environment.

## What resources are available to learn about Blackbird?

Refer to the following resources as you get started with Blackbird:

* [quick-start](quick-start/ "mention") guide
* [Ambassador YouTube channel](https://www.youtube.com/c/AmbassadorLabs)
* [Support knowledge base](https://support.datawire.io/) (Requires a subscription to Blackbird Developer, Blackbird Platform, or Blackbird Enterprise. For more information, see [Blackbird Pricing](https://www.getambassador.io/blackbird-pricing).)

## Which features are available in the CLI?

For a full list of commands, see the [blackbird-cli](technical-reference/blackbird-cli/ "mention") commands reference or run `blackbird help` in the Blackbird CLI.

## How does code generation work in Blackbird?

After you upload or create an API in Blackbird, you can generate code using the `blackbird code generate` command in the CLI. Blackbird’s code generation speeds up API development by converting your API specification into boilerplate code in `Go`. You can then test and debug your APIs against production-like traffic, which allows you to inspect and troubleshoot in real-time before promoting it to production. For more information, see [code-quickstart.md](quick-start/code-quickstart.md "mention").

## What type of code does Blackbird generate?

Blackbird generates boilerplate code in `Go` for both client and server-side APIs based on your OpenAPI specification. For more information, see [code-quickstart.md](quick-start/code-quickstart.md "mention").

## How can I manage my users and organization in Blackbird?

In the [Blackbird UI](https://blackbird.a8r.io/dashboard), use the **Settings** page to manage your users, organization, subscription, and billing. For more information, see [user-management.md](user-management.md "mention").
