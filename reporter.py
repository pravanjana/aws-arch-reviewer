import os
from datetime import datetime


# Groups findings by category (Security, CDN, Cost)
def group_by_category(findings):
    grouped = {}
    for finding in findings:
        category = finding["category"]
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(finding)
    return grouped


# Counts findings by severity (HIGH, MEDIUM, LOW)
def count_by_severity(findings):
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for finding in findings:
        severity = finding["severity"]
        if severity in counts:
            counts[severity] += 1
    return counts


# Generates a timestamped filename for the report
def generate_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"report_{timestamp}.md"


# Builds the full Markdown report as a string
def build_report(findings, file_path, iac_type):
    grouped = group_by_category(findings)
    severity_counts = count_by_severity(findings)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []

    # Header
    lines.append("# AWS Architecture Review Report\n")
    lines.append(f"**File Analyzed:** `{file_path}`")
    lines.append(f"**IaC Type:** {iac_type}")
    lines.append(f"**Generated:** {timestamp}")
    lines.append(f"**Total Findings:** {len(findings)}\n")

    # Summary table
    lines.append("## Summary\n")
    lines.append("| Severity | Count |")
    lines.append("|----------|-------|")
    lines.append(f"| 🔴 HIGH   | {severity_counts['HIGH']} |")
    lines.append(f"| 🟡 MEDIUM | {severity_counts['MEDIUM']} |")
    lines.append(f"| 🟢 LOW    | {severity_counts['LOW']} |")
    lines.append("")

    # Findings grouped by category
    lines.append("## Findings\n")

    category_icons = {
        "Security": "🔒",
        "CDN": "🌐",
        "Cost": "💰"
    }

    for category, category_findings in grouped.items():
        icon = category_icons.get(category, "📋")
        lines.append(f"### {icon} {category}\n")

        for finding in category_findings:
            severity = finding["severity"]
            lines.append(f"#### {finding['resource']}")
            lines.append(f"- **Severity:** {severity}")
            lines.append(f"- **Issue:** {finding['issue']}")
            lines.append(f"- **Recommendation:** {finding['recommendation']}")
            lines.append("")

    return "\n".join(lines)


# Main function — builds and saves the report to a file
def generate_report(findings, file_path, iac_type):
    report_content = build_report(findings, file_path, iac_type)
    filename = generate_filename()

    with open(filename, "w") as f:
        f.write(report_content)

    return filename
