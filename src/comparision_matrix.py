import numpy as np
import pandas as pd
import os
import json

def build_matrix_with_ports(component_graph):
    """Convert nodes+edges JSON into adjacency matrix with port numbers if available."""
    if not component_graph:
        return None

    nodes = component_graph.get("nodes", [])
    edges = component_graph.get("edges", [])
    node_ids = [n["id"] for n in nodes]

    size = len(node_ids)
    matrix = [["0"] * size for _ in range(size)]

    id_to_idx = {nid: i for i, nid in enumerate(node_ids)}

    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src in id_to_idx and tgt in id_to_idx:
            src_idx = id_to_idx[src]
            tgt_idx = id_to_idx[tgt]
            src_port = edge.get("source_port")
            tgt_port = edge.get("target_port")

            if src_port or tgt_port:
                matrix[src_idx][tgt_idx] = f"{src_port or ''}->{tgt_port or ''}".strip("->")
            else:
                matrix[src_idx][tgt_idx] = "1"

    # Return as a pandas DataFrame for readability
    return pd.DataFrame(matrix, index=node_ids, columns=node_ids)

def save_matrix_csv(folder, fname, node_ids, matrix):
    df = pd.DataFrame(matrix, index=node_ids, columns=node_ids)
    out_path = os.path.join(folder, fname.replace("_components.json", "_matrix.csv"))
    # Write adjacency matrix section
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Adjacency Matrix\n")
        df.to_csv(f)
        f.write("\nEdge List with Ports\n")
        # Load the original graph JSON to get port info
        json_path = os.path.join(folder, fname)
        with open(json_path, "r", encoding="utf-8") as jf:
            graph = json.load(jf)
        edges = graph.get("edges", [])
        # Write header
        f.write("source,target,source_port,target_port\n")
        for edge in edges:
            src = edge.get("source", "")
            tgt = edge.get("target", "")
            src_port = edge.get("source_port", "")
            tgt_port = edge.get("target_port", "")
            f.write(f"{src},{tgt},{src_port},{tgt_port}\n")
    print(f"Matrix and edge list saved: {out_path}")


def batch_convert_all_json_to_csv(folder):
    for fname in os.listdir(folder):
        if fname.endswith('_components.json'):
            json_path = os.path.join(folder, fname)
            with open(json_path, 'r', encoding='utf-8') as f:
                try:
                    graph = json.load(f)
                except Exception as e:
                    print(f"Skipping {fname}: {e}")
                    continue
            if not graph or 'nodes' not in graph or 'edges' not in graph:
                print(f"Skipping {fname}: invalid graph structure")
                continue
            node_ids = [n['id'] for n in graph['nodes']]
            matrix = [["0"] * len(node_ids) for _ in node_ids]
            id_to_idx = {nid: i for i, nid in enumerate(node_ids)}
            for edge in graph['edges']:
                src = edge.get('source')
                tgt = edge.get('target')
                if src in id_to_idx and tgt in id_to_idx:
                    src_idx = id_to_idx[src]
                    tgt_idx = id_to_idx[tgt]
                    src_port = edge.get('source_port')
                    tgt_port = edge.get('target_port')
                    if src_port or tgt_port:
                        matrix[src_idx][tgt_idx] = f"{src_port or ''}->{tgt_port or ''}".strip("->")
                    else:
                        matrix[src_idx][tgt_idx] = "1"
            save_matrix_csv(folder, fname, node_ids, matrix)

if __name__ == "__main__":
    image_folders = [
        "extracted_images/ML94459A_Capacity-Sector-Add_6_Ready to BOM_Approved_2025-02-25",
        "extracted_images/SE03939D_A_M_2024-01-30_v2_"
    ]
    base_dir = os.path.dirname(__file__)
    for rel_folder in image_folders:
        folder = os.path.join(base_dir, rel_folder)
        print(f"Processing folder: {folder}")
        batch_convert_all_json_to_csv(folder)
