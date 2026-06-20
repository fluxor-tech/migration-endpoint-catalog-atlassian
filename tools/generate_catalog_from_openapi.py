import json
import re
from datetime import date
from pathlib import Path

import yaml


HTTP_METHODS = {"get", "post", "put", "patch", "delete"}

PRODUCTS = [
    {
        "source": "sources/jira-cloud-openapi.json",
        "target": "catalog/jira-cloud.yml",
        "vendor": "Atlassian",
        "product": "Jira Cloud",
        "api_family": "Jira Cloud Platform REST API v3",
        "base_url_template": "https://{site}.atlassian.net",
        "official_root": "https://developer.atlassian.com/cloud/jira/platform/rest/v3/",
        "auth_doc": "https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#authentication-and-authorization",
    },
    {
        "source": "sources/confluence-cloud-openapi.json",
        "target": "catalog/confluence-cloud.yml",
        "vendor": "Atlassian",
        "product": "Confluence Cloud",
        "api_family": "Confluence Cloud REST API v2",
        "base_url_template": "https://{site}.atlassian.net/wiki",
        "official_root": "https://developer.atlassian.com/cloud/confluence/rest/v2/",
        "auth_doc": "https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#authentication-and-authorization",
    },
    {
        "source": "sources/jira-service-management-cloud-openapi.json",
        "target": "catalog/jira-service-management-cloud.yml",
        "vendor": "Atlassian",
        "product": "Jira Service Management Cloud",
        "api_family": "Jira Service Management Cloud REST API",
        "base_url_template": "https://{site}.atlassian.net",
        "official_root": "https://developer.atlassian.com/cloud/jira/service-desk/rest/",
        "auth_doc": "https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/#authentication-and-authorization",
    },
]


def slugify(value):
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def group_slug(tags):
    if not tags:
        return "ungrouped"
    return slugify(tags[0])


def doc_url(root, tags):
    if not tags:
        return root
    return root.rstrip("/") + f"/api-group-{slugify(tags[0])}/"


def operation_category(method, path, summary):
    text = f"{method} {path} {summary}".lower()
    if method == "GET":
        if any(token in text for token in ["search", "get", "find", "list", "retrieve"]):
            return "read"
        return "read"
    if method in {"POST", "PUT", "PATCH"}:
        if any(token in text for token in ["create", "add", "update", "edit", "transition", "assign", "link", "upload"]):
            return "write"
        return "write"
    if method == "DELETE":
        return "delete"
    return "other"


def use_cases(method, path, summary, tags):
    tag = tags[0] if tags else "resource"
    category = operation_category(method, path, summary)
    if category == "read":
        uses = [f"{tag} inventory, lookup, reporting, or validation"]
    elif category == "write":
        uses = [f"{tag} creation, update, automation, or backfill"]
    elif category == "delete":
        uses = [f"{tag} cleanup, removal, or reconciliation"]
    else:
        uses = [f"{tag} operation"]
    return uses


def status_for(operation):
    if operation.get("deprecated"):
        return "deprecated"
    return "reviewed"


def pagination_style(parameters):
    names = {p.get("name", "").lower() for p in parameters}
    if {"cursor", "nextpagetoken"} & names:
        return "cursor"
    if {"startat", "start", "limit", "maxresults"} & names:
        return "page"
    return None


def scopes(operation):
    result = {}
    security = operation.get("security") or []
    values = []
    for item in security:
        for scope_list in item.values():
            if isinstance(scope_list, list):
                values.extend(scope_list)
    if values:
        result["granular"] = sorted(set(values))
    return result or None


def build_endpoint(root, path, method, operation):
    method_upper = method.upper()
    tags = operation.get("tags") or []
    summary = operation.get("summary") or operation.get("operationId") or f"{method_upper} {path}"
    parameters = operation.get("parameters") or []
    endpoint = {
        "id": slugify(f"{group_slug(tags)}-{method_upper}-{path}"),
        "status": status_for(operation),
        "method": method_upper,
        "path": path,
        "summary": summary,
        "operation_id": operation.get("operationId"),
        "api_group": tags[0] if tags else None,
        "operation_category": operation_category(method_upper, path, summary),
        "use_cases": use_cases(method_upper, path, summary, tags),
        "permissions": ["See official documentation for product permissions and visibility constraints"],
        "scopes": scopes(operation),
        "pagination": None,
        "official_doc_url": doc_url(root, tags),
    }
    page_style = pagination_style(parameters)
    if page_style:
        endpoint["pagination"] = {"style": page_style}
    return {k: v for k, v in endpoint.items() if v not in (None, [], {})}


def generate(product):
    spec = json.loads(Path(product["source"]).read_text(encoding="utf-8"))
    endpoints = []
    for path in sorted(spec.get("paths", {})):
        path_item = spec["paths"][path]
        for method in sorted(path_item):
            if method not in HTTP_METHODS:
                continue
            endpoints.append(build_endpoint(product["official_root"], path, method, path_item[method]))

    data = {
        "vendor": product["vendor"],
        "product": product["product"],
        "api_family": product["api_family"],
        "base_url_template": product["base_url_template"],
        "official_docs": {
            "root": product["official_root"],
            "authentication": product["auth_doc"],
            "openapi_source": product["source"],
        },
        "catalog_status": "active",
        "last_reviewed": date.today().isoformat(),
        "generation": {
            "source": "official_openapi",
            "endpoint_count": len(endpoints),
        },
        "endpoints": endpoints,
    }
    Path(product["target"]).write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=False, width=120),
        encoding="utf-8",
    )
    return product["target"], len(endpoints)


def main():
    for product in PRODUCTS:
        target, count = generate(product)
        print(f"{target}: {count} endpoints")


if __name__ == "__main__":
    main()
