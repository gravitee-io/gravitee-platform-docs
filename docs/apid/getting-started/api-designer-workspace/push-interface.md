# Push interface

You designed your API and now you want to use that design. And that is what this interface is about!

There a two panes …​ **API Settings** and **Push API**

### API Settings

Here you can see and edit (if needed) the basic parameters of the API (name, version, description). You can also download the API design in json format. Last but not least you get to see the documentation.

![documentation](https://docs.gravitee.io/images/cockpit/apid\_documentation.png)

### Push API

![push](https://docs.gravitee.io/images/cockpit/apid\_push.png)

You can push your API to your linked API Management installation in three different ways:

Documented

The API documentation (OAS) is created. The API is not deployed on the gateway nor published on the portal.

Mocked

Same as **Documented** (documentation created) **plus** the API is deployed with a keyless plan on the gateway with a `mock` policy. Consumers can retrieve mock responses from it. The body of the mock response is based on the examples defined in the design interface.

Published

Same as **Mocked** (documentation created, deployed, keyless plan, mock policy) **plus** it is published on the portal. Consumers can subscribe to it.

\
