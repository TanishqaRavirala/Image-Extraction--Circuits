import json
import pandas as pd
from d3graph import d3graph
import os

image_folders = [
    "extracted_images/ML94459A_Capacity-Sector-Add_6_Ready to BOM_Approved_2025-02-25",
    "extracted_images/SE03939D_A_M_2024-01-30_v2_"
]

for folder in image_folders:
    # List all JSON files in the folder
    json_files = [f for f in os.listdir(folder) if f.endswith('.json')]

    for json_file in json_files:
        json_path = os.path.join(folder, json_file)
        print(f"Processing {json_path} ...")

        # Load JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Combine edges (same as before)
        edge_map = {}
        for edge in data['edges']:
            src, tgt = edge['source'], edge['target']
            s_port, t_port = str(edge.get('source_port', '')), str(edge.get('target_port', ''))
            key = (src, tgt)
            edge_map.setdefault(key, []).append((s_port, t_port))

        # Build adjacency matrix
        nodes = sorted({node["id"] for node in data["nodes"]})
        adjmat = pd.DataFrame(0, index=nodes, columns=nodes)
        for (src, tgt) in edge_map.keys():
            adjmat.loc[src, tgt] = 1

        # Build and plot graph
        d3 = d3graph()
        d3.graph(adjmat)

        # Set node labels
        node_labels = {node['id']: node['label'] for node in data['nodes']}
        d3.set_node_properties(label=node_labels)

        # Prepare edge labels
        graph_edges = list(d3.edge_properties.keys())
        edge_labels = []
        for src, tgt in graph_edges:
            ports = edge_map.get((src, tgt), [])
            label_parts = [f"{s_port}->{t_port}" if s_port and t_port else s_port or t_port for s_port, t_port in ports]
            edge_labels.append(", ".join(label_parts))
        d3.set_edge_properties(label=edge_labels)

        # Show generates the temp HTML file
        d3.show()

        # Patch the last temp HTML file to position edge labels properly
        temp_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp', 'd3graph')
        html_files = sorted(
            [f for f in os.listdir(temp_dir) if f.endswith('.html')],
            key=lambda x: os.path.getmtime(os.path.join(temp_dir, x)),
            reverse=True
        )

        if html_files:
            latest_file = os.path.join(temp_dir, html_files[0])
            with open(latest_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            js_patch = '''
            .attr("x", d => (d.source.x + d.target.x) / 2)
            .attr("y", d => (d.source.y + d.target.y) / 2)
            .text(d => d.label);
            '''
            html_content = html_content.replace('.text(d => d.label);', js_patch)

            # Save patched HTML file in the same folder with same basename as JSON but .html
            html_output_path = os.path.join(folder, os.path.splitext(json_file)[0] + '.html')
            with open(html_output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"✅ Saved HTML visualization: {html_output_path}")
        else:
            print(f"⚠️ Could not find temp HTML file for {json_file}")
