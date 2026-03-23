# Pagination Controls and Accessibility

## Pagination Controls

Pagination appears at the bottom of the catalog and application selection screens. Use the page size selector to adjust the number of results displayed per page. For the catalog, the default page size options are 5, 10, 20, 50, and 100. For application selection, the page size options are 6, 12, 24, 48, or 96 (default: 6).

Navigate between pages using the previous and next buttons or by clicking direct page number buttons. When the page range is truncated, ellipsis indicators appear to show that additional pages exist.

All pagination controls use semantic HTML buttons with comprehensive ARIA labels for keyboard navigation and screen reader support. The navigation element is labeled "Pagination," page buttons announce "Go to page [number]," and the current page is marked with `aria-current="page"`. The page size selector is labeled "Results per page."

## Restrictions

- Category-based catalog navigation is no longer available; all APIs appear in the unified catalog view
- Infinite scroll pagination has been removed in favor of standard page-based pagination
- Banner display configuration (`portalNext.banner.enabled`) is no longer supported
- The `CategoriesViewComponent`, `CategoryApisComponent`, `TabsViewComponent`, `ApisListComponent`, and `CatalogBannerComponent` have been removed
- Application selection pagination interface changed: `start` and `end` properties removed, replaced with `currentPage`, `totalApplications`, and `pageSize`
