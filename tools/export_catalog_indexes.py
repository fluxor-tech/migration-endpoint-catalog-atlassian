import csv
from pathlib import Path

import yaml


CATALOG_DIR = Path("catalog")
OUTPUT_DIR = Path("catalog/indexes")


def iter_endpoints():
    for path in sorted(CATALOG_DIR.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for endpoint in data["endpoints"]:
            yield {
                "catalog": path.name,
                "vendor": data["vendor"],
                "product": data["product"],
                "api_family": data["api_family"],
                "api_group": endpoint.get("api_group", ""),
                "id": endpoint["id"],
                "status": endpoint["status"],
                "method": endpoint["method"],
                "path": endpoint["path"],
                "summary": endpoint["summary"],
                "operation_category": endpoint["operation_category"],
                "use_cases": "; ".join(endpoint.get("use_cases", [])),
                "official_doc_url": endpoint["official_doc_url"],
            }


def main():
    rows = list(iter_endpoints())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = OUTPUT_DIR / "all-endpoints.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    by_product = {}
    by_category = {}
    for row in rows:
        by_product[row["product"]] = by_product.get(row["product"], 0) + 1
        by_category[row["operation_category"]] = by_category.get(row["operation_category"], 0) + 1

    md_lines = [
        "# Atlassian Endpoint Catalog Index",
        "",
        f"Total endpoints: {len(rows)}",
        "",
        "## By Product",
        "",
        "| Product | Endpoints |",
        "| --- | ---: |",
    ]
    for product, count in sorted(by_product.items()):
        md_lines.append(f"| {product} | {count} |")
    md_lines.extend([
        "",
        "## By Operation Category",
        "",
        "| Category | Endpoints |",
        "| --- | ---: |",
    ])
    for category, count in sorted(by_category.items()):
        md_lines.append(f"| {category} | {count} |")
    md_lines.extend([
        "",
        "## Files",
        "",
        "- `all-endpoints.csv`: flat index for spreadsheet filtering.",
        "- `../jira-cloud.yml`: full Jira Cloud endpoint catalog.",
        "- `../confluence-cloud.yml`: full Confluence Cloud endpoint catalog.",
        "- `../jira-service-management-cloud.yml`: full JSM endpoint catalog.",
        "",
    ])
    (OUTPUT_DIR / "README.md").write_text("\n".join(md_lines), encoding="utf-8")
    print(f"wrote {csv_path} ({len(rows)} rows)")
    print(f"wrote {OUTPUT_DIR / 'README.md'}")


if __name__ == "__main__":
    main()
