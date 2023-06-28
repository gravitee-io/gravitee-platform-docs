# API Fundamentals

The shift from monolithic applications to microservices relies on web APIs to decouple components and their interfacing mechanisms. which were initially synchronous and adhered tightly to the request-response model. Although these components communicated synchronously, the execution flow of applications did not have to be synchronous. As the single-threaded language that powers the web, Javascript is inherently asynchronous because the main execution thread cannot be blocked by synchronous web API communication. Asynchronous communication that decouples information producers from information consumers enables powerful functionality but this requires a restructuring of application logic from the backend to the UI to create a system with an entirely different architectural style referred to as event-driven architecture.

The guides below offer high-level overviews of the components and functionality at the core of the Gravitee platform to provide users with a robust conceptual framework.

<table data-view="cards" data-full-width="false"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>API Basics</td><td></td><td><a href="api-basics.md">api-basics.md</a></td></tr><tr><td></td><td>Web APIs</td><td></td><td><a href="web-apis.md">web-apis.md</a></td></tr><tr><td></td><td>Categorizing Web APIs</td><td></td><td><a href="categorizing-web-apis.md">categorizing-web-apis.md</a></td></tr></tbody></table>

