import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from parser import parse_iac_file
from reviewer import review_iac
from reporter import generate_report

# Create a Rich console for pretty output
console = Console()


# Maps severity level to a color for display
def severity_color(severity):
    if severity == "HIGH":
        return "red"
    elif severity == "MEDIUM":
        return "yellow"
    else:
        return "green"


# Displays findings in a color-coded table
def display_findings(findings, file_path, iac_type):
    # Print header panel
    console.print(Panel(
        "[bold cyan]AWS Architecture Reviewer[/bold cyan]",
        box=box.DOUBLE
    ))

    console.print(f"\n[bold]Analyzing:[/bold] {file_path}")
    console.print(f"[bold]Type:[/bold] {iac_type}")
    console.print(f"[bold]Findings:[/bold] {len(findings)}\n")

    # Build the table
    table = Table(box=box.ROUNDED, show_lines=True)
    table.add_column("Resource", style="cyan", width=20)
    table.add_column("Category", style="white", width=10)
    table.add_column("Severity", width=8)
    table.add_column("Issue", width=35)
    table.add_column("Recommendation", width=35)

    # Add each finding as a row
    for finding in findings:
        color = severity_color(finding["severity"])
        table.add_row(
            finding["resource"],
            finding["category"],
            f"[{color}]{finding['severity']}[/{color}]",
            finding["issue"],
            finding["recommendation"]
        )

    console.print(table)


# Main function — entry point of the tool
def main():
    # Set up command line argument parsing
    arg_parser = argparse.ArgumentParser(
        description="AI-powered AWS IaC Architecture Reviewer"
    )
    arg_parser.add_argument(
        "--file",
        required=True,
        help="Path to CloudFormation or Terraform file"
    )
    arg_parser.add_argument(
        "--summary",
        action="store_true",
        help="Show only HIGH severity findings"
    )
    args = arg_parser.parse_args()

    # Step 1 - Parse the IaC file
    console.print(f"\n[cyan]Parsing file:[/cyan] {args.file}")
    parsed = parse_iac_file(args.file)

    # Step 2 - Send to Claude for review
    console.print("[cyan]Sending to Claude for review...[/cyan]\n")
    findings = review_iac(parsed)

    # Step 3 - Filter findings if --summary flag is passed
    if args.summary:
        findings = [f for f in findings if f["severity"] == "HIGH"]
        console.print("[yellow]⚠️  Summary mode — showing HIGH severity only[/yellow]\n")

    # Step 4 - Display findings
    display_findings(findings, args.file, parsed["type"])

    # Step 5 - Generate Markdown report
    report_file = generate_report(findings, args.file, parsed["type"])
    console.print(f"\n[green]✅ Report saved:[/green] {report_file}\n")


# Run main() when script is executed directly
if __name__ == "__main__":
    main()
