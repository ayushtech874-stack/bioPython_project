# 🧬 DNA Sequence Similarity Checker

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Biopython](https://img.shields.io/badge/Biopython-1.80%2B-green.svg)](https://biopython.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-orange.svg)](https://matplotlib.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

An interactive, beginner-friendly bioinformatics web application built with **Python 3**, **Streamlit**, **Biopython**, **Matplotlib**, and **Pandas**.

The **DNA Sequence Similarity Checker** allows users to compare two DNA sequences, validate nucleotide fidelity (A, T, G, C, N), calculate percentage similarity, inspect color-coded sequence alignments in real-time, generate high-resolution scientific charts, and export analysis reports.

> 📖 **Comprehensive Masterclass & Viva Guide:** Check out [`ProjectExplanation.html`](file:///d:/ayush%20biopython/ProjectExplanation.html) for complete problem statement analysis, algorithmic derivations, code walk-throughs, and **25+ Viva Voce questions & answers**!

---

## 📑 Table of Contents
- [Project Overview](#-project-overview)
- [How It Works (Algorithm & Formula)](#-how-it-works-algorithm--formula)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture & Directory Structure](#-project-architecture--directory-structure)
- [File Purpose & Explanation](#-file-purpose--explanation)
- [Installation Guide](#-installation-guide)
- [How to Run the Application](#-how-to-run-the-application)
- [Using the Web Application](#-using-the-web-application)
- [Verification & Benchmark Test Cases](#-verification--benchmark-test-cases)
- [Positional Comparison vs. Biological Alignment](#-positional-comparison-vs-biological-alignment)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🎯 Project Overview

In bioinformatics, analyzing genetic sequence variation is fundamental for studying gene function, identifying single nucleotide polymorphisms (SNPs), diagnosing genetic disorders, and mapping evolutionary divergence.

This project implements an intuitive, position-by-position comparison designed for college-level bioinformatics education. It provides an accessible entry point into biological data analysis without requiring complex backend servers or database installations.

---

## 📐 How It Works (Algorithm & Formula)

1. **Input & Sanitization**:
   - The user inputs two DNA sequences either by pasting text or uploading `.fasta` files.
   - All whitespace, newlines, and tabs are removed, and letters are converted to uppercase.
2. **Strict Validation**:
   - Every character is validated against valid DNA bases: `A` (Adenine), `T` (Thymine), `G` (Guanine), `C` (Cytosine), and optionally `N` (unknown/ambiguous base).
   - Any invalid character is detected, and its exact 1-based position is reported to the user.
3. **Position-by-Position Comparison**:
   - The sequences are compared nucleotide-by-nucleotide at index $i = 0, 1, 2, \dots$
   - **Match**: Both sequences have the exact same nucleotide ($c_1 = c_2$).
   - **Mismatch**: Both sequences have different nucleotides ($c_1 \neq c_2$).
   - **Gap**: If sequences have unequal lengths, the shorter sequence is padded with gap characters (`-`) and counted as non-matches.
4. **Similarity Metric**:
   $$\text{Similarity (\%)} = \left( \frac{\text{Number of Matching Positions}}{\max(\text{Length}_1, \text{Length}_2)} \right) \times 100$$
5. **Interpretation Categories**:
   - `90% – 100%`: **Very High Positional Similarity**
   - `70% – 89%`: **High Positional Similarity**
   - `40% – 69%`: **Moderate Positional Similarity**
   - `Below 40%`: **Low Positional Similarity**

> **Note:** These categories are illustrative for educational purposes and do not establish evolutionary or biological relatedness (which require dynamic programming alignment like Needleman-Wunsch or BLAST).

---

## ✨ Key Features

- ✍️ **Dual Input Modes**: Manual text input or `.fasta`/`.fa`/`.fna`/`.txt` file uploads powered by **Biopython** (`Bio.SeqIO`).
- 🛡️ **Robust Validation**: Real-time error handling with character position diagnostic feedback.
- 🎨 **Visual Sequence Alignment**:
  - 🟩 **Green** (`#DCFCE7`): Matching nucleotides (`|`)
  - 🟥 **Red** (`#FEE2E2`): Mismatching nucleotides (`•`)
  - ⬜ **Grey** (`#F1F5F9`): Missing positions / gaps (`—`)
  - Includes nucleotide position rulers and chunked wrapping (15–50 nt per line).
- 📊 **Matplotlib Visualizations**:
  - Positional composition bar chart (Matches vs. Mismatches vs. Gaps).
  - Modern donut chart illustrating overall percentage identity.
  - Linear sequence distribution track ($5' \to 3'$) mapping mutations along the sequence.
- 📥 **Export Reports**:
  - Download position-by-position comparison results as **CSV**.
  - Download formatted plain-text lab analysis report (**`.txt`**).
  - Download complete academic/professional project report in editable Word format (**`.docx`**).
- 📘 **Comprehensive Project Documentation**:
  - Pre-generated editable report: [`DNA_Sequence_Similarity_Checker_Project_Report.docx`](file:///d:/ayush%20biopython/DNA_Sequence_Similarity_Checker_Project_Report.docx) (also in `docs/`).
- 🧪 **Built-in Presets**: Quick-load standard test cases, unequal length pairs, and real biological examples (e.g., Sickle Cell Anemia mutation in human Beta-Globin).

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.10+** | Core programming language |
| **Streamlit** | Modern reactive web UI, metric cards, sidebar navigation |
| **Biopython (`Bio.SeqIO`)** | Industry-standard biological sequence handling and FASTA parser |
| **Matplotlib** | High-DPI bar charts, donut charts, and positional sequence tracks |
| **Pandas** | Tabular data manipulation, DataFrame inspection, and CSV export |

---

## 📁 Project Architecture & Directory Structure

```text
bioPython_project/
│
├── README.md                                          # Complete project documentation & guide
├── requirements.txt                                   # Top-level dependencies list
├── .gitignore                                         # Git ignore rules (pycache, temp files, etc.)
├── run_app.py                                         # Convenience root launcher script
├── generate_docx_report.py                            # Generator script for academic Word report
├── DNA_Sequence_Similarity_Checker_Project_Report.docx # Complete editable Word project report
│
├── docs/
│   └── DNA_Sequence_Similarity_Checker_Project_Report.docx # Backup / documentation folder copy
│
└── dna_similarity_checker/                            # Core application package
    ├── app.py                                         # Streamlit frontend & interactive dashboard
    ├── sequence_utils.py                              # Validation, Biopython FASTA parser, and math
    ├── visualization.py                               # Matplotlib charts & HTML color-coded visualizer
    ├── test_checker.py                                # Automated unit test suite (8 tests)
    ├── requirements.txt                               # Package-specific dependencies
    ├── README.md                                      # Package-level documentation
    ├── DNA_Sequence_Similarity_Checker_Project_Report.docx # Application download asset
    │
    └── sample_data/                                   # Pre-loaded FASTA test files
        ├── seq1.fasta                                 # Standard 12 nt reference sequence
        ├── seq2.fasta                                 # Standard 12 nt sequence with 1 mismatch
        ├── hba_normal.fasta                           # Human Beta-Globin normal allele (HbA)
        └── hbs_sickle.fasta                           # Sickle Cell variant allele (HbS)
```

---

## 🔍 File Purpose & Explanation

### 1. `sequence_utils.py`
The bioinformatics calculation engine:
- `clean_sequence(raw_sequence)`: Strips whitespace, newlines, and converts to uppercase.
- `validate_dna_sequence(sequence, allow_n)`: Checks for illegal characters and returns user-friendly error messages indicating exact positions.
- `parse_fasta(file_or_text)`: Integrates Biopython's `SeqIO.parse` to extract records from FASTA files.
- `calculate_positional_similarity(seq1, seq2)`: Computes positional matching, gap padding, counts, and percentages.
- `calculate_gc_content(sequence)`: Calculates GC% for both sequences.
- `generate_text_report(stats, ...)`: Creates a formatted downloadable text report.

### 2. `visualization.py`
The graphical rendering module:
- `plot_comparison_barchart(stats)`: Renders a bar chart with counts and percentages.
- `plot_similarity_donut(stats)`: Renders a donut chart with centered similarity percentage.
- `plot_position_track(comparison_rows)`: Generates a $5' \to 3'$ positional track plot.
- `render_html_sequence_alignment(...)`: Renders color-coded HTML boxes with nucleotide symbols and position rulers.

### 3. `app.py`
The Streamlit web interface:
- Organizes the multi-page dashboard via the sidebar (`Home`, `Sequence Comparison`, `Results & Analytics`, `About the Project`).
- Provides preset loading buttons and manages session state.
- Renders responsive metric cards, alerts, charts, and file download buttons.

### 4. `test_checker.py`
A comprehensive automated test suite testing:
- Prompt benchmark (12 nt, 1 mismatch = 91.67%).
- Unequal sequence lengths and trailing gap padding.
- Uppercase conversion and whitespace stripping.
- Detection of invalid nucleotides.
- Empty sequence handling.
- Biopython FASTA parsing.
- Matplotlib chart and HTML generation.
- Plain-text report formatting.

---

## 🚀 Installation Guide

### Prerequisites
Make sure **Python 3.10** or higher is installed on your system. You can verify your Python version by running:
```bash
python --version
```

### Step 1: Clone the Repository
```bash
git clone https://github.com/ayushtech874-stack/bioPython_project.git
cd bioPython_project
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run the Application

You can launch the application using either of the following commands:

### Method 1: Using the convenience launcher (Recommended)
```bash
python run_app.py
```

### Method 2: Running Streamlit directly
```bash
streamlit run dna_similarity_checker/app.py
```

Once started, Streamlit will open the application in your default web browser at:
```text
http://localhost:8501
```

---

## 🖥️ Using the Web Application

1. **Navigation**: Use the left sidebar to navigate between sections:
   - **`🏠 Home`**: Background context, formula, and overview.
   - **`🧬 Sequence Comparison`**: Sequence input, comparison, and visual alignment.
   - **`📊 Results & Analytics`**: Matplotlib graphs, track maps, and download links.
   - **`ℹ️ About the Project`**: Scientific theory and comparison with alignment algorithms.
2. **Comparing Sequences**:
   - Enter DNA sequences manually in the text boxes or upload FASTA files.
   - Click the **"🚀 Compare Sequences"** button.
   - Inspect the metric cards (Length, GC Content, Matches, Mismatches, Gaps, Similarity %).
   - View the color-coded nucleotide alignment with position numbers.
3. **Exporting Data**:
   - Go to **`📊 Results & Analytics`** to download your comparison as a **CSV file** or a detailed **Text Report (.txt)**.

---

## 🧪 Verification & Benchmark Test Cases

You can run the automated test suite anytime:
```bash
python dna_similarity_checker/test_checker.py
```

### Benchmark Test 1: Standard Prompt Case
- **Sequence 1**: `ATGCGTACGTAG` (Length: 12 nt, GC: 50.0%)
- **Sequence 2**: `ATGCGTTCGTAG` (Length: 12 nt, GC: 50.0%)
- **Matching Positions**: `11`
- **Mismatching Positions**: `1` (Position 7: A vs T)
- **Gaps**: `0`
- **Similarity Percentage**: **`91.67%`**
- **Interpretation**: **Very High Positional Similarity (90%–100%)**

### Benchmark Test 2: Unequal Sequence Lengths
- **Sequence 1**: `ATGCGTAGCTAGCTAGCTA` (19 nt)
- **Sequence 2**: `ATGCGTAGCTAG` (12 nt)
- **Matching Positions**: `12`
- **Gaps (Trailing Missing Positions)**: `7`
- **Similarity Percentage**: **`63.16%`**
- **Interpretation**: **Moderate Positional Similarity (40%–69%)**

### Benchmark Test 3: Real Biological Variant (Sickle Cell Anemia)
- **HbA (Normal Beta-Globin fragment)**: `ACTCCTGAGGAGAAGTCT`
- **HbS (Sickle Beta-Globin fragment)**: `ACTCCTGTGGAGAAGTCT`
- **Result**: Single point mutation at codon 6 (`GAG` $\to$ `GTG`, A $\to$ T).
- **Matching Positions**: `17` / `18` (Similarity: **`94.44%`**).

---

## 🔬 Positional Comparison vs. Biological Alignment

Students should understand how positional matching compares to biological alignment algorithms:

| Feature | Positional Comparison (This Project) | Global Alignment (Needleman-Wunsch) | Local Alignment (Smith-Waterman / BLAST) |
| :--- | :--- | :--- | :--- |
| **Methodology** | Direct index-by-index comparison | Dynamic programming with gap penalties | Identifies high-scoring matching sub-regions |
| **Frameshift tolerance** | None (a 1-base shift misaligns all downstream bases) | High (inserts optimal gaps inside sequences) | High (detects matching regions regardless of position) |
| **Best Application** | Point mutation/SNP verification in pre-aligned sequences | Full-length comparison of homologous genes | Database searches and remote homology detection |
| **Algorithmic Complexity**| $O(N)$ linear time | $O(N \times M)$ quadratic time | $O(N \times M)$ dynamic programming / heuristic $O(N)$ |

---

## ❓ Troubleshooting

1. **`ModuleNotFoundError: No module named 'Bio'`**:
   - Run `pip install biopython` or `pip install -r requirements.txt`.
2. **`streamlit: command not found`**:
   - Make sure your Python Scripts directory is added to your system `PATH`, or run via `python -m streamlit run dna_similarity_checker/app.py`.
3. **Invalid Character Error**:
   - DNA sequences must strictly contain only `A`, `T`, `G`, `C` (and optionally `N`). Ensure numbers, special characters, or protein amino acid codes (like `P`, `E`, `K`) are removed.

---

## 📜 License

This project is licensed under the MIT License — free for academic, classroom, and educational use.
