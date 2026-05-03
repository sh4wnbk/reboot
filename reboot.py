import argparse
import sys
import requests
import textwrap
import os
import io

# === CONFIGURATION ===
WATSONX_API_KEY = os.environ.get("WATSONX_API_KEY", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "meta-llama/llama-3-3-70b-instruct"

INSTRUCTION = """You are a cognitive state extractor for IBM Bob IDE sessions.
Given a raw Bob session export, extract and compress into a
single paragraph beginning with "RESTORE CONTEXT:" addressed
directly to Bob. Cover: what is being built, why this approach
was chosen over alternatives, what files are in progress, the
exact next step, and any dead ends already ruled out.
No bullet points. No headers. One paragraph only.
Maximum 150 words. Nothing before or after the paragraph.
Do NOT write code. Output the paragraph exactly once.
Stop immediately after the final sentence.
If the export contains multiple tasks, summarize only
the most recent task. Ignore earlier tasks entirely."""

INSTRUCTION_STRUCTURED = """You are a cognitive state extractor for IBM Bob IDE sessions.
Given a raw Bob session export, extract key facts and output ONLY this exact format:

PROJECT:     [project name]
STATE:       [one sentence — what is done and what is broken/pending]
LAST ACTION: [the most recent concrete thing completed]
NEXT:        [single immediate next action]
DEAD ENDS:   [comma separated list of ruled-out approaches]
DEADLINE:    [if mentioned, otherwise omit this line]

No prose. No extra lines. No explanation. Exact format above only.
If the export contains multiple tasks, use only the most recent task."""

FEW_SHOT_PARAGRAPH = """Input:
# Task: Build session resume feature
User: Create a function that reads a markdown file
Bob: Here's the implementation in parser.py
Files Modified: parser.py
Tokens: 1.2k | Cost: 0.02

Output:
RESTORE CONTEXT: We are building X to solve Y using approach Z instead of W because of reason R. File A is complete, File B is in progress. The immediate next step is action N. Do not suggest alternative_approach — it was ruled out because of constraint C."""

FEW_SHOT_STRUCTURED = """Input:
# Task: Build session resume feature
User: Create a function that reads a markdown file
Bob: Here's the implementation in parser.py
Files Modified: parser.py
Tokens: 1.2k | Cost: 0.02

Output:
PROJECT:     Session Resume Feature
STATE:       parser.py complete, main integration pending
LAST ACTION: Implemented markdown file reader in parser.py
NEXT:        Integrate parser with main application flow
DEAD ENDS:   JSON format, XML parsing"""


def get_iam_token(api_key):
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": api_key
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def format_card(fields: dict) -> str:
    separator = "=" * 50
    lines = [separator]
    for key, val in fields.items():
        wrapped = textwrap.wrap(val.strip(), 50) if val.strip() else ["None"]
        lines.append(f"{key:<12} {wrapped[0]}")
        for continuation in wrapped[1:]:
            lines.append(f"{'':12} {continuation}")
    lines.append(separator)
    return "\n".join(lines)


def generate_restoration_string(export_text, token, fmt="paragraph"):
    # Take first 1500 chars (task context) + last 1500 chars (outcome)
    # This ensures we capture both the initial task and the final result
    if len(export_text) > 3000:
        export_text = export_text[:1500] + "\n...\n" + export_text[-1500:]
    instruction = INSTRUCTION if fmt == "paragraph" else INSTRUCTION_STRUCTURED
    few_shot = FEW_SHOT_PARAGRAPH if fmt == "paragraph" else FEW_SHOT_STRUCTURED
    prompt = f"{instruction}\n\n{few_shot}\n\nInput:\n{export_text}\n\nOutput:"

    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 175 if fmt == "paragraph" else 250,
            "min_new_tokens": 50,
            "repetition_penalty": 1.3,
            "stop_sequences": [] if fmt == "structured" else ["\n\n"]
        },
        "project_id": PROJECT_ID
    }

    resp = requests.post(
        f"{WATSONX_URL}/ml/v1/text/generation?version=2023-05-29",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    resp.raise_for_status()
    result = resp.json()["results"][0]["generated_text"].strip()
    
    if fmt == "structured":
        lines = [l for l in result.split("\n") if l.strip()]
        clean = []
        for line in lines:
            clean.append(line)
            if line.startswith("DEADLINE:") or (line.startswith("DEAD ENDS:") and not any(l.startswith("DEADLINE:") for l in lines)):
                break
        result = "\n".join(clean[:6])
    return result


def main():
    # Set stdout to UTF-8 encoding to handle Unicode characters
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # Check environment variables at runtime, not at module load time
    if not WATSONX_API_KEY or not PROJECT_ID:
        print("Error: WATSONX_API_KEY and PROJECT_ID environment variables must be set.")
        print("Run: $env:WATSONX_API_KEY='your-key'")
        print("Run: $env:PROJECT_ID='your-project-id'")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="reB0ot - generate a Restoration String from a Bob session export.")
    parser.add_argument("--export", required=True, help="Path to the Bob session export .md file")
    parser.add_argument("--format", choices=["paragraph", "structured"],
                        default="paragraph", help="Output format")
    args = parser.parse_args()

    try:
        with open(args.export, "r", encoding="utf-8") as f:
            export_text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.export}")
        sys.exit(1)

    print("Authenticating with IBM Cloud...")
    token = get_iam_token(WATSONX_API_KEY)

    print("Generating Restoration String...\n")
    result = generate_restoration_string(export_text, token, args.format)

    if args.format == "structured":
        fields = {}
        for line in result.split("\n"):
            if ":" in line:
                key, _, val = line.partition(":")
                fields[key.strip()] = val.strip()
        print(format_card(fields))
    else:
        print("=" * 60)
        print(result)
        print("=" * 60)


if __name__ == "__main__":
    main()

# Made with Bob
