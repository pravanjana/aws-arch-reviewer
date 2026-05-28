import json
import yaml
import hcl2


# Detects whether the file is CloudFormation (YAML/JSON) or Terraform (.tf)
def detect_file_type(file_path):
    if file_path.endswith(".tf"):
        return "terraform"
    elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
        return "cloudformation_yaml"
    elif file_path.endswith(".json"):
        return "cloudformation_json"
    else:
        return "unknown"


# Reads a CloudFormation YAML file and returns the Resources section
def parse_cloudformation_yaml(file_path):
    with open(file_path, "r") as f:
        template = yaml.safe_load(f)
    resources = template.get("Resources", {})
    return resources


# Reads a CloudFormation JSON file and returns the Resources section
def parse_cloudformation_json(file_path):
    with open(file_path, "r") as f:
        template = json.load(f)
    resources = template.get("Resources", {})
    return resources


# Reads a Terraform .tf file and returns the parsed content
def parse_terraform(file_path):
    with open(file_path, "r") as f:
        template = hcl2.load(f)
    return template


# Main function — detects file type and calls the right parser
def parse_iac_file(file_path):
    file_type = detect_file_type(file_path)

    if file_type == "cloudformation_yaml":
        resources = parse_cloudformation_yaml(file_path)
        return {"type": "cloudformation", "resources": resources}

    elif file_type == "cloudformation_json":
        resources = parse_cloudformation_json(file_path)
        return {"type": "cloudformation", "resources": resources}

    elif file_type == "terraform":
        resources = parse_terraform(file_path)
        return {"type": "terraform", "resources": resources}

    else:
        raise ValueError(f"Unsupported file type: {file_path}")
