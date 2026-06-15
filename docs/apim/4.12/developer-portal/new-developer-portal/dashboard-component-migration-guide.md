# Dashboard Component Migration Guide

## Related Changes

### Dashboard Component Migration

The `GraviteeDashboardComponent` no longer manages internal filter state. Consumers must provide filters and time ranges via input properties and manage state externally.

#### Before

```typescript
<gd-dashboard
  [dashboard]="dashboard"
  [filters]="filters"
  [defaultPeriod]="'5m'"
  (selectedFilters)="handleFilters($event)"
  (refresh)="handleRefresh()"
/>
```

#### After

```typescript
<gd-dashboard
  [dashboard]="dashboard"
  [requestFilters]="filtersStore.requestFilters()"
  [timeRange]="filtersStore.timeRange()"
  [interval]="filtersStore.interval()"
  [refreshToken]="filtersStore.refreshToken()"
>
  <div gdToolbarBelow>
    <gd-dynamic-filter-bar ... />
    <gd-timeframe-selector ... />
  </div>
</gd-dashboard>
```

#### Removed Inputs

* **Filters** — No longer supported. Use **Request Filters** instead.
* **Default Period** — No longer supported. Use **Time Range** instead.

#### Removed Outputs

* `selectedFilters` — No longer supported. Manage filter state externally.
* `refresh` — No longer supported. Use **Refresh Token** instead.

#### Added Inputs

* **Request Filters** (`requestFilters`)
  * Type: `RequestFilter[]`
  * Default: `[]`
  * External filters to merge with widget-level filters.
* **Time Range** (`timeRange`)
  * Type: `TimeRange`
  * Required
  * Specifies the time range for widget requests.
* **Interval** (`interval`)
  * Type: `number | undefined`
  * Default: `undefined`
  * Optional interval for time-series widgets.
* **Refresh Token** (`refreshToken`)
  * Type: `number`
  * Default: `0`
  * Triggers widget data refresh when value changes.

#### Content Projection

Use the `[gdToolbarBelow]` attribute to project custom filter bars, datepickers, or banners between the dashboard title and widget grid.

#### Removed Exports

* `GenericFilterBarComponent` — Use `DynamicFilterBarComponent` and `TimeframeSelectorComponent` separately.
* `Filter` interface — Use `FilterCondition` and `FilterDefinition`.
* `SelectedFilter` interface — Use `FilterCondition`.

#### New Exports

* `TimeframeSelectorComponent`
* `filter-url.codec` (`encodeViewState`, `decodeViewState`)
* `RequestFilter`, `TimeRange` types

#### URL Encoding Changes

Filters and time ranges are now encoded in a unified `q` query parameter with version marker `v=1`. Legacy `period`, `from`, `to` query parameters are removed during synchronization.

