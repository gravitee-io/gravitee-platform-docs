### Searching Protected Resources

Search Protected Resources by sending a GET request to `/protected-resources?q=<query>`. The system performs case-insensitive matching across the `name` and `clientId` fields. Use `*` as a wildcard character, which is converted to SQL `%` or regex `.*` depending on the backend. If the `q` parameter is absent, the system falls back to type-based filtering. Results are ordered by `updated_at` in descending order.
