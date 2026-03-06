### Console UI changes

The Console UI adds A2A Proxy to the API type filter in the API list view. APIs display with the "A2A Proxy" label and the `gio-literal:a2a-proxy` icon.

### Policy Studio changes

Policy Studio includes A2A Proxy in flow phase dialogs for compatible policies. Policies that declare A2A Proxy support in their `plugin.properties` file appear in the flow configuration interface for A2A Proxy APIs.

### Management API OpenAPI schema

The Management API OpenAPI schema defines `A2A_PROXY` as a valid `FlowPhase` array type. This allows A2A Proxy APIs to use the same flow phases as other V4 API types.

### UI component library updates

The following UI component libraries were updated to version 17.4.0 to support A2A Proxy rendering:

* `@gravitee/ui-analytics`
* `@gravitee/ui-particles-angular`
* `@gravitee/ui-policy-studio-angular`
* `@gravitee/ui-schematics`

### CI pipeline changes

The CI pipeline now includes a "Lint & test APIM Libs" job that runs when front-end dependencies change. The job triggers on changes to `package.json`, `nx.json`, or `yarn.lock`.
