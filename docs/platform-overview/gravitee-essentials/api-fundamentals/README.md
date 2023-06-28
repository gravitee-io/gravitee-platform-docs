# API Fundamentals

The shift from monoliths to microservices relies on web APIs to decouple application components and interfacing. Although web API communication was initially synchronous, adhering tightly to the request-response model, application execution flow was not similarly constrained. On the contrary, JavaScript, the single-threaded language that powers the web, is inherently asynchronous to ensure that the main execution thread is never blocked.&#x20;

Asynchronous communication that decouples information producers from information consumers enables powerful functionality. However, the adoption of an alternative communication paradigm required restructuring the entirety of the application logic, from the backend to the UI. The resultant system follows a completely different architectural style referred to as event-driven architecture.

The guides below offer high-level overviews of the components and functionality at the core of the Gravitee platform to provide users with a robust conceptual framework.

<table data-view="cards" data-full-width="false"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>API Basics</td><td></td><td><a href="api-basics.md">api-basics.md</a></td></tr><tr><td></td><td>Web APIs</td><td></td><td><a href="web-apis.md">web-apis.md</a></td></tr><tr><td></td><td>Categorizing Web APIs</td><td></td><td><a href="categorizing-web-apis.md">categorizing-web-apis.md</a></td></tr></tbody></table>

