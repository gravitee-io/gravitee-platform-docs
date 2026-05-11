
# V4 API Import: Matching Strategies and Restrictions

For complete import procedures, see [Import or Update a V4 API from OpenAPI or Gravitee Definition](import-or-update-a-v4-api-from-openapi-or-gravitee-definition.md).

## Update Matching Strategy

When updating an existing API, the system matches imported resources to existing resources using a fallback hierarchy. **Plans** are matched first by `crossId` (if present in both import and database), then by plan `id` if no `crossId` match is found. Plans present in the database but absent from the import definition are automatically deleted. **Pages** are matched first by `crossId`, then by `type` and `name` if no `crossId` match is found. Unmatched pages are created as new resources. **Flows** (OpenAPI re-import only) are matched by HTTP selector key (path + alphabetically sorted methods); matching flows preserve their existing IDs, while new flows receive generated IDs.

## Restrictions

- Only V4 API definitions are supported; V2 APIs use the legacy import component
- WSDL import format is not yet implemented (UI option disabled)
- Remote source mode requires CORS-enabled endpoints; status 0 errors indicate CORS or reachability issues
- Context path conflicts with existing APIs return HTTP 400
- Invalid image formats in `apiPicture` or `apiBackground` fields return HTTP 400
- Flow ID preservation during OpenAPI re-import requires exact HTTP selector key match (path + sorted methods); changes to path or methods generate new flow IDs
- Duplicate HTTP flow keys in persisted flows log a warning and retain the first flow ID encountered
- Plans absent from the import definition are automatically deleted during update (no "close" option)
- Documentation pages created from OpenAPI specifications are automatically published
