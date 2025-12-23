# 📡 Circuit Diagram Extraction & Graph Visualization

## 🔍 Overview

This project focuses on **automatically extracting circuit diagrams from PDF files**, identifying **components and their interconnections**, and converting the extracted information into **structured graph representations**.
The final output is an **interactive D3.js visualization** that helps understand complex telecom and circuit configurations intuitively.

The project is designed around **real-world telecom circuit diagrams** (5G, LTE, FDD, TDD, SRAN systems), not synthetic examples.

---

## 🧠 Problem Statement

Circuit diagrams in PDFs are difficult to analyze programmatically.
This project addresses that by:

- Extracting diagrams as images
- Structuring components and connections as graph data
- Enabling visualization and analysis using graph theory concepts

---

## ⚙️ Processing Pipeline

```text
PDF File
  ↓
High-resolution Image Extraction
  ↓
Component & Connection Extraction (JSON)
  ↓
Adjacency / Comparison Matrix (CSV)
  ↓
Interactive D3 Graph Visualization (HTML)
```

---

## 📂 Project Structure

```text
ImageExtraction-Circuits/
│
├── src/
│   ├── image_extract.py          # PDF → images
│   ├── component_extraction.py   # Image → components & connections (JSON)
│   ├── comparison_matrix.py      # JSON → adjacency matrix (CSV)
│   └── visualize_d3graph.py      # JSON → interactive D3 graph
│
├── extracted_images/
│   ├── <PDF_Name>/
│   │   ├── *.png
│   │   ├── *_components.json
│   │   ├── *_matrix.csv
│   │   └── *_components.html
│
├── docs/
│   └── sample_circuit.png
│
├── requirements.txt
└── README.md
```

---

## 🧩 Key Features

- 📄 Extracts circuit diagrams from PDF files
- 🖼️ Converts each page into high-resolution images
- 🔌 Represents components and connections as graph nodes and edges
- 📦 Stores structured data in JSON format
- 📊 Generates adjacency/comparison matrices for analysis
- 🌐 Produces interactive D3.js HTML visualizations
- 📡 Tailored for real telecom and network infrastructure diagrams

---

## 📷Sample input image
<img width="1427" height="2203" alt="Configuration 56790EZ_SR_T" src="https://github.com/user-attachments/assets/87274a6f-0639-468d-a54a-0e4cc788a14d" />

## 🛠️ Technologies Used

- **Python**
- **PyMuPDF (fitz)** – PDF processing
- **Pandas / NumPy** – data handling
- **JSON / CSV** – structured storage
- **d3graph & D3.js** – graph visualization

---

## 🚀 How to Run

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Extract images from PDF

```bash
python src/image_extract.py input.pdf
```

### 3️⃣ Generate adjacency matrix

```bash
python src/comparison_matrix.py
```

### 4️⃣ Visualize graph

```bash
python src/visualize_d3graph.py
```

---

## 📊 Output Artifacts

- `*_components.json` → Nodes & edges representation
- `*_matrix.csv` → Adjacency / comparison matrix
- `*_components.html` → Interactive circuit graph

<img width="931" height="688" alt="image" src="https://github.com/user-attachments/assets/ffc853a2-a12d-42d4-9ba4-67094121d118" />

## 📌 Use Cases

- Telecom infrastructure analysis
- Circuit documentation & auditing
- Graph-based system understanding
- Network visualization & education
- Preprocessing for ML-based diagram understanding

---

## 👩‍💻 Author

**Tanishka Ravirala**
Work at SHI Solutions India Pvt. Ltd.

---

## 📄 License

This project is released under the MIT License.
