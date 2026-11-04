## [Unreleased]

### Added

- Fuzzy matching in search results (a1b2c3d)

### Changed

- Search results are sorted by relevance first (d4e5f6a)

### Fixed

- Expired tokens are rejected instead of refreshed (b2c3d4e)

### Removed

- Legacy list_users endpoint (c3d4e5f)
  BREAKING CHANGE: list_users is removed. Callers must use
  list_customers, which takes the same arguments.

Excluded, not hidden: e5f6a7b (chore, dependency bump) is not
user-facing, so it gets no changelog line.
