# 🔍 AWS Architecture Reviewer

An AI-powered CLI tool that analyzes CloudFormation and Terraform templates
for security gaps, CDN/CloudFront misconfigurations, and cost optimization
issues — using the Anthropic Claude API.

## 🎯 What it does

- Accepts CloudFormation (YAML/JSON) or Terraform (.tf) files as input
- Sends the parsed resources to Claude AI for intelligent review
- Displays color-coded findings in the terminal
- Generates a timestamped Markdown report file

## 🏗️ Architecture

IaC File → parser.py → reviewer.py (Claude API) → cli.py + reporter.py

## 🔒 Review Categories

| Category | Examples |
|----------|---------|
| Security | Open ports, missing encryption, no IAM roles, public S3 buckets |
| CDN | HTTP allowed, missing OAI/OAC, no WAF, no logging |
| Cost | Oversized instances, unconstrained instance types |

## 🚀 Getting Started

### Prerequisites
- Python 3
- Anthropic API key

### Installation

```bash
git clone https://github.com/pravanjana/aws-arch-reviewer.git
cd aws-arch-reviewer
pip3 install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

ANTHROPIC_API_KEY=your_api_key_here

### Usage

```bash
# Analyze a CloudFormation template
python3 cli.py --file samples/sample.yaml

# Analyze a Terraform file
python3 cli.py --file samples/sample.tf

# Analyze any real IaC file
python3 cli.py --file /path/to/your/template.yaml
```

## 📊 Sample Output

╔══════════════════════════════════════╗
║ AWS Architecture Reviewer            ║
╚══════════════════════════════════════╝
Analyzing: samples/real_vpc.yaml
Type: cloudformation
Findings: 11
╭──────────────────────┬────────────┬──────────┬─────────────────────────╮
│ Resource             │ Category   │ Severity │ Issue                   │
├──────────────────────┼────────────┼──────────┼─────────────────────────┤
│ EC2SecurityGroup     │ Security   │ HIGH     │ No egress rules defined  │
│ VPC                  │ Security   │ MEDIUM   │ No VPC flow logs enabled │
│ EC2Host              │ Cost       │ MEDIUM   │ Unconstrained EC2 type   │
╰──────────────────────┴────────────┴──────────┴─────────────────────────╯
✅ Report saved: report_2026-05-27_18-20-44.md

## 🛠️ Tech Stack

- Python 3
- [Anthropic Claude API](https://www.anthropic.com) (claude-sonnet-4-5)
- [Rich](https://github.com/Textualize/rich) — terminal formatting
- PyYAML — CloudFormation YAML parsing
- python-hcl2 — Terraform HCL parsing

## 📁 Project Structure

aws-arch-reviewer/
├── CLAUDE.md         ← Claude Code context file
├── parser.py         ← IaC file parser (CloudFormation + Terraform)
├── reviewer.py       ← Claude API integration
├── cli.py            ← CLI entry point with rich output
├── reporter.py       ← Markdown report generator
├── requirements.txt  ← Python dependencies
└── samples/
├── sample.yaml   ← CloudFormation sample with intentional issues
└── real_vpc.yaml ← Real AWS VPC template

## 👤 Author

Pravanjana — Solutions Architect (AWS SAA-C03, Azure AZ-104)


