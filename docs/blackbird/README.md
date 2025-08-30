# Welcome

Blackbird is an API development tool designed to streamline the way you build, test, and mock API services. With features like AI-assisted spec generation, dynamic mocking, local and ephemeral environment testing, and safe pre-production deployments, Blackbird empowers you to focus on API business logic and deliver results faster.

> **Note:** For the best experience, use a screen resolution of 1280 or higher to view the full content of this documentation site. Some elements may not display correctly on smaller screens.

## Blackbird users

Blackbird is built for API architects, developers, and QA engineers who want an efficient way to develop APIs. Whether you're building a new API from scratch or refining an existing API, Blackbird simplifies your workflow and reduces time-to-production.

## Blackbird features

Blackbird supports your API development lifecycle as you design, implement, and test your API specs.

<figure><img src=".gitbook/assets/bb 0.png" alt=""><figcaption></figcaption></figure>

## Design

Instead of building your API spec from scratch, use the following Blackbird features to accelerate development.

* **AI spec generation** – Use our AI tool to create an initial OpenAPI specification that provides a consistent, standardized structure. You can provide a prompt with information about the API you want to create and then provide additional prompts to refine the API spec before adding it to your API catalog.
* **API refinement** – Use our editing tools to manually refine your spec, or leverage our AI editing capabilities to ensure schema accuracy, optimize endpoints, and enhance API reliability.

## Implement

After your API spec is designed, Blackbird can help you collaborate and run your code efficiently.

* **Code generation** – Generate code for an existing OpenAPI specification so you can interact with it more efficiently during development. Blackbird uses OpenAPI Generator to generate server or client code automatically. Learn more in our [code](usage-guides/code/ "mention") guide.
* **Mocks** – Create dynamic or static mock instances based on your OpenAPI specification to enable seamless collaboration for frontend and backend developers. Dynamic mocking generates responses based on input parameters, whereas static mocking returns fixed, predefined responses based on hardcoded data. Learn more in our [mock-instances.md](usage-guides/mock-instances.md "mention") guide.
* **Code run** – Run your script to test the behavior of your API spec, analyze request/response data, and troubleshoot issues. Learn more in our [code-run-and-debug.md](usage-guides/code/code-run-and-debug.md "mention") guide.

## Test

Blackbird provides multiple tools for testing your API spec across different environments.

* **Code debug** – Debug your code in a dedicated Blackbird environment with production-like traffic. Learn more in our [code-run-and-debug.md](usage-guides/code/code-run-and-debug.md "mention") guide.
* **Remote clusters** – Locally run and debug your service while seamlessly interacting with the rest of your Kubernetes cluster. You can also intercept traffic to your service by routing requests from the cluster to your local machine as if were running remotely. Learn more in our [remote-clusters-telepresence](usage-guides/code/remote-clusters-telepresence/ "mention") guide.
* **Deploy** – Deploy your API to a dedicated, non-production environment to validate functionality before impacting live systems. Learn more in our [deployments.md](usage-guides/deployments.md "mention") guide.
