# AWS Architecture Reviewer — Claude Code Context

## Project Purpose
A CLI tool that analyzes CloudFormation (YAML/JSON) and Terraform (.tf) files
for security gaps, CDN/CloudFront misconfigurations, and cost optimization issues.
Uses the Anthropic Claude API to generate findings and outputs results to both
the terminal and a Markdown report file.

## Owner
Solutions Architect with CDN/AWS/Azure background.
Beginner-level Python — keep code simple, well-commented, and beginner-friendly.

## Stack
- Python 3 (command: python3)
- Anthropic Claude API (model: claude-sonnet-4-20250514)
- Libraries: anthropic, python-dotenv, pyyaml, python-hcl2, rich
- Config: .env file for ANTHROPIC_API_KEY

## Project Structure
- parser.py     → detects IaC type, extracts resource blocks
- reviewer.py   → sends content to Claude API, returns structured findings
- cli.py        → entry point, pretty terminal output using rich
- reporter.py   → generates timestamped Markdown report
- samples/      → sample CloudFormation and Terraform files for testing

## Run Command
python3 cli.py --file samples/sample.yaml
python3 cli.py --file samples/sample.tf

## Coding Conventions
- Use clear variable names, no clever one-liners
- Add a comment above every function explaining what it does
- All API calls go in reviewer.py only
- Never hardcode API keys — always use python-dotenv
- Findings returned from Claude should be structured JSON

## Environment Variables (.env)
ANTHROPIC_API_KEY=your_key_here

## Review Focus Areas
1. Security gaps (open ports, missing encryption, wildcard IAM policies)
2. CDN / CloudFront misconfigurations (missing HTTPS, no WAF, bad cache behavior)
3. Cost optimization (over-provisioned resources, missing lifecycle policies)

## Known Gotchas
- HCL2 parser can be finicky with complex Terraform files — keep samples simple
- CloudFormation files can be YAML or JSON — parser.py must handle both
- Always test with samples/ before trying real IaC files
