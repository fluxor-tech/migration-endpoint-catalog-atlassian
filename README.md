# Atlassian Migration Endpoint Catalog

Catalog of Atlassian Cloud REST endpoints useful for migration discovery, extraction, transformation, loading, validation, and post-migration repair.

This repository is not an SDK and does not replace Atlassian's official documentation. Each catalog entry should link back to the official vendor documentation and explain why the endpoint matters in migration work.

## Scope

Initial scope:

- Jira Cloud Platform REST API v3
- Confluence Cloud REST API v2
- Jira Service Management Cloud REST API

Out of scope for the first pass:

- Atlassian Data Center APIs
- Marketplace app APIs
- Product-specific private or undocumented endpoints
- Automation rule internals not covered by public APIs

## Repository Layout

```text
catalog/
  jira-cloud.yml
  confluence-cloud.yml
  jira-service-management-cloud.yml
examples/
  requests/
  responses/
notes/
  auth-and-permissions.md
  migration-use-cases.md
schemas/
  endpoint.schema.json
sources/
  official-docs.md
```

## Entry Model

Each endpoint entry should capture:

- Product and API family
- Method and path
- Migration phase and migration use
- Authentication and permissions/scopes
- Pagination and rate-limit considerations
- Official documentation URL
- Operational notes and caveats

Use `schemas/endpoint.schema.json` as the canonical shape for YAML/JSON catalog entries.

## Status Values

- `candidate`: identified from official docs, not yet reviewed for migration usage.
- `reviewed`: checked against official docs and migration purpose is clear.
- `validated`: tested against a real tenant with documented behavior.
- `deprecated`: retained only for historical context.

## Source Policy

Only add endpoints from official Atlassian documentation unless an entry is clearly marked as tenant-specific evidence in `notes`. Public catalog entries should prefer official docs over observed behavior.

