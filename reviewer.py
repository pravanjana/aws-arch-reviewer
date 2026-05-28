import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()

# Create the Anthropic client
client = Anthropic()


# Builds the prompt we send to Claude
def build_prompt(parsed_iac):
    resources_json = json.dumps(parsed_iac["resources"], indent=2)
    iac_type = parsed_iac["type"]

    prompt = f"""
You are a senior AWS Solutions Architect reviewing an IaC template.

Template type: {iac_type}

Resources to review:
{resources_json}

Analyze these resources and return ONLY a JSON array of findings.
Each finding must have these exact fields:
- resource: the resource name
- category: one of "Security", "CDN", "Cost"
- severity: one of "HIGH", "MEDIUM", "LOW"
- issue: a short description of the problem
- recommendation: a clear fix

Return ONLY the JSON array. No explanation, no markdown, no extra text.
"""
    return prompt


# Sends the parsed IaC to Claude and returns findings as a Python list
def review_iac(parsed_iac):
    prompt = build_prompt(parsed_iac)

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the text response from Claude
    raw_text = response.content[0].text

    # Strip markdown code fences if Claude wrapped the JSON in ```json ... ```
    clean_text = raw_text.strip()
    if clean_text.startswith("```"):
        clean_text = clean_text.split("```")[1]
        if clean_text.startswith("json"):
            clean_text = clean_text[4:]
        clean_text = clean_text.strip()

    # Parse the JSON array Claude returned
    findings = json.loads(clean_text)

    return findings
