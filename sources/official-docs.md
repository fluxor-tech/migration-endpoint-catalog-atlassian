# Official Atlassian Documentation Sources

Primary sources for this catalog:

- Jira Cloud Platform REST API v3: <https://developer.atlassian.com/cloud/jira/platform/rest/v3/>
- Confluence Cloud REST API v2: <https://developer.atlassian.com/cloud/confluence/rest/v2/>
- Jira Service Management Cloud REST API: <https://developer.atlassian.com/cloud/jira/service-desk/rest/>

OpenAPI source files stored in this repository:

- `sources/jira-cloud-openapi.json`
- `sources/confluence-cloud-openapi.json`
- `sources/jira-service-management-cloud-openapi.json`

Reference areas covered by the generated catalog include:

- Jira issue search
- Jira issues
- Jira issue fields
- Jira custom field contexts
- Jira projects
- Jira issue link types
- Jira issue links
- Jira workflows and statuses
- Jira user search
- Jira attachments
- Confluence pages
- Confluence spaces
- Confluence attachments
- Jira Service Management service desks
- Jira Service Management request types
- Jira Service Management requests

## Review Rules

1. Every endpoint must include an `official_doc_url`.
2. Prefer product-level REST API documentation over secondary docs or blog posts.
3. Mark endpoints as `candidate` until their migration purpose and permission model have been reviewed.
4. Mark endpoints as `validated` only after tenant testing has confirmed request/response behavior.
