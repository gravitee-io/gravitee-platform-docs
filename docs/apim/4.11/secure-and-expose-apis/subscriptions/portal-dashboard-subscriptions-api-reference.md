# Portal Dashboard Subscriptions API Reference

## Restrictions

- Close subscription button is visible only for subscriptions with `ACCEPTED` or `PAUSED` status
- Subscriptions with `PENDING`, `REJECTED`, or `CLOSED` status can't be closed via the UI
- Query parameters for subscription list API changed from singular (`apiId`, `applicationId`) to plural (`apiIds`, `applicationIds`) and now require arrays
- Maximum inner content width is constrained to 1440px
- Page size selection limited to predefined options: 10, 20, 50, or 100 items

## Related Changes

The subscription list API query parameters migrated from singular to plural names (`apiId` → `apiIds`, `applicationId` → `applicationIds`) and now accept arrays, requiring updates to all API calls. The UI typography system introduced next-gen classes (`.next-gen-h1` through `.next-gen-caption`) with standardized font sizes, weights, and line heights. Material Design overrides added warn-colored outlined button styles and updated dialog container border radius to 8px (from 4px). The close subscription dialog was extracted into a shared `ConfirmDialogComponent` for reuse across the dashboard and API subscriptions tab. Pagination controls replaced numeric-only navigation with Previous/Next buttons and updated button styles (stroked for current page, standard for navigation).

