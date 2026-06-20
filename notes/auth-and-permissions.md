# Authentication and Permissions Notes

Atlassian Cloud endpoint behavior depends on both authentication method and product permissions.

Common authentication modes:

- Basic authentication with Atlassian account email and API token
- OAuth 2.0 3LO
- Forge app authentication
- Connect app authentication where applicable

Migration work usually needs a deliberately privileged account or app with access to all source and target projects/spaces involved in the migration.

## Practical Checks

- Confirm Browse Projects for Jira extraction.
- Confirm issue security visibility before treating search totals as complete.
- Confirm Create Issues and Edit Issues before load/backfill operations.
- Confirm Link Issues before relationship restoration.
- Confirm Confluence page/space view and edit permissions before page extraction or publishing.
- For Jira Service Management, distinguish agent, customer, and admin perspectives.

## Account IDs

Jira Cloud identifies users by account ID. Migration mappings should avoid usernames and legacy user keys unless they are only retained as historical source identifiers.

