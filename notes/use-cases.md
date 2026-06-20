# Use Cases

This catalog is a complete Atlassian endpoint inventory. It is useful for API discovery, integration design, automation, governance, reporting, migration planning, and operational support.

## API Discovery

Inventory Atlassian capabilities by product and API group:

- Projects and spaces
- Issue types, statuses, workflows
- Fields, contexts, and schemas
- Request types and portal fields
- Link types and relationship semantics

## Integration And Automation

Identify endpoints for controlled reads and writes:

- Issue, page, and request creation
- Field and configuration updates
- Workflow transitions
- Attachments and comments
- Webhooks and automation-adjacent operations

## Reporting And Governance

Use read endpoints to support:

- Configuration inventory
- Permission and access analysis
- Field governance
- Usage and metadata reporting
- Audit and validation checks

## Migration

The same complete catalog can be filtered for migration workflows.

### Discover

Inventory source and target configuration:

- Projects and spaces
- Issue types, statuses, workflows
- Fields, contexts, and schemas
- Request types and portal fields
- Link types and relationship semantics

### Extract

Read source data:

- Issues and selected fields
- Changelog entries
- Attachments and metadata
- Confluence pages and spaces
- JSM requests and request metadata

### Transform

Map source values into target-ready values:

- User account IDs
- Field IDs and option IDs
- Status and workflow differences
- Parent/child hierarchy
- Link type directionality

### Load

Write target data:

- Create issues or requests
- Update fields and descriptions
- Restore parents and links
- Create or update Confluence pages

### Validate

Confirm target state:

- Counts by project/type/status
- Spot checks by key mapping
- Required field coverage
- Link and parent completeness
- Portal-facing JSM request behavior

### Reconcile

Repair or explain gaps:

- Changelog-based key mapping
- Lost parent associations after moves
- Removed fields during issue moves
- Link restoration and missing remote issues
- Non-migratable system or app-managed fields
