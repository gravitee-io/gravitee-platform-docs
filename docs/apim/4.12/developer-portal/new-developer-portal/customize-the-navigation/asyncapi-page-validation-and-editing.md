# AsyncAPI Page Validation and Editing

## AsyncAPI Validation

AsyncAPI content is validated before saving to ensure it is valid YAML and contains a properly formatted `asyncapi` version field. The version must be a semantic version string matching the pattern `/^\d+\.\d+\.\d+/` (for example, `3.0.0` or `2.6.0`). Empty or whitespace-only content is rejected.

The platform does not validate the full AsyncAPI specification schema—only the presence and format of the version field. Validation is skipped when content is empty or whitespace-only (returns `true` without error).

Real-time validation runs on every content change. The Save button is disabled when `contentControl.invalid === true` or `contentControl.pristine === true`. Validation does not show snackbar notifications during real-time validation (only on save attempt).

The AsyncAPI editor implements `ControlValueAccessor` for Angular forms integration and supports disabled state propagation. The preview is optimized for the Console's side-by-side layout. New AsyncAPI pages are created with a starter AsyncAPI 3.0 template.

## Existing OpenAPI Page Migration

Existing OpenAPI pages that had no viewer configuration before this feature are treated as Redoc pages, preserving prior portal behavior. The `OpenApiPortalPageContentConfigurationUpgrader` (order 720) runs on startup and automatically sets default configuration `{"viewer":"REDOC"}` for existing OpenAPI pages without configuration.
