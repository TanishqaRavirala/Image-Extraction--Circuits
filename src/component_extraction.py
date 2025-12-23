import boto3
import json
import base64

# Initialize AWS clients once
s3_client = boto3.client("s3")
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")  # adjust region if needed


def load_image_bytes_from_s3(bucket_name, key):
    """Load image bytes from S3."""
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    return response["Body"].read()


def call_claude_4_with_image(image_bytes, prompt):
    """Send an image + prompt to Claude Sonnet 4 and return assistant JSON text."""
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    if not image_b64:
        raise ValueError("Image base64 string is empty. Check your image loading logic.")

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",  # change if needed
                            "data": image_b64,
                        },
                    },
                ],
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.2,
    }

    response = bedrock_client.invoke_model(
        modelId="us.anthropic.claude-sonnet-4-20250514-v1:0",
        body=json.dumps(request_body),
    )

    raw_output = json.loads(response["body"].read().decode())

    # Extract assistant’s text response
    text_outputs = [item["text"] for item in raw_output.get("content", []) if item.get("type") == "text"]
    if not text_outputs:
        raise ValueError("No text output found in Claude response.")
    return text_outputs[0]


bucket_name = "circuit-diagrams"

# ---------- Automated batch extraction ----------
import os
import re
prompt = """
Identify all components, subcomponents, and their relationships (edges and nodes) in this circuit image.
Return the output as a structured JSON with two lists: 'nodes' for components and subcomponents, and 'edges' for connections.

Each node should have:
- id (unique string identifier)
- label (component/subcomponent name)

Each edge should have:
- source (node id)
- target (node id)
- optional 'source_port' (if a port number/label is shown on the source side)
- optional 'target_port' (if a port number/label is shown on the target side)

Ensure that if a port number is visible in the diagram, it is included in the JSON edge object.
"""

bucket_name = "circuit-diagrams"
image_folders = [
    "extracted_images/ML94459A_Capacity-Sector-Add_6_Ready to BOM_Approved_2025-02-25",
    "extracted_images/SE03939D_A_M_2024-01-30_v2_"
]

for folder in image_folders:
    folder_path = os.path.join(folder)
    # List all PNG images in the folder
    for img_name in os.listdir(folder_path):
        if img_name.lower().endswith(".png"):
            image_key = f"{folder}/{img_name}"
            print(f"Processing: {image_key}")
            try:
                image_bytes = load_image_bytes_from_s3(bucket_name, image_key)
                result_json_text = call_claude_4_with_image(image_bytes, prompt)
                print("Raw Claude response:")
                print(result_json_text)
                # Extract JSON from response
                match = re.search(r'```json\s*(\{.*?\})\s*```', result_json_text, re.DOTALL)
                if match:
                    json_str = match.group(1)
                else:
                    match = re.search(r'(\{.*\})', result_json_text, re.DOTALL)
                    if match:
                        json_str = match.group(1)
                    else:
                        json_str = result_json_text
                try:
                    component_graph = json.loads(json_str)
                except Exception:
                    component_graph = None
                # Only save if valid
                out_name = f"{img_name.rsplit('.', 1)[0]}_components.json"
                out_path = os.path.join(folder_path, out_name)
                if component_graph is not None:
                    with open(out_path, "w", encoding="utf-8") as f:
                        json.dump(component_graph, f, indent=2)
                    print(f"Saved: {out_path}")
                else:
                    print(f"Skipped saving for {image_key}: response was not valid JSON.")
                    # Optionally log error to a file
                    err_path = os.path.join(folder_path, f"{img_name.rsplit('.', 1)[0]}_error.log")
                    with open(err_path, "w", encoding="utf-8") as ef:
                        ef.write(result_json_text)
            except Exception as e:
                print(f"Error processing {image_key}: {e}")
