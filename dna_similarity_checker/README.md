# 🧬 DNA Sequence Similarity Checker

An interactive, beginner-friendly bioinformatics web application built with **Python 3**, **Streamlit**, **Biopython**, **Matplotlib**, and **Pandas**. 

This application performs a position-by-position comparison between two DNA sequences, calculates their similarity percentage, validates input nucleotide fidelity (A, T, G, C, N), visualizes aligned sequences in color, and generates publication-style graphical charts.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Directory Structure](#-directory-structure)
- [File Purpose & Architecture](#-file-purpose--architecture)
- [Installation Guide](#-installation-guide)
- [Running the Application](#-running-the-application)
- [Verification & Test Cases](#-verification--test-cases)
- [Positional Comparison vs. Biological Alignment](#-positional-comparison-vs-biological-alignment)
- [License](#-license)

---

## 🎯 Project Overview

In bioinformatics and molecular biology, comparing DNA sequences is a core procedure used to detect mutations (such as Single Nucleotide Polymorphisms or SNPs), measure genetic divergence, and study evolutionary relationships.

This project implements a transparent, position-by-position comparison algorithm:
$$\text{Similarity (\%)} = \left( \frac{\text{Number of Matching Positions}}{\max(\text{Length}_1, \text{Length}_2)} \right) \times 100$$

For sequences of unequal length, missing positions in the shorter sequence are treated as gaps (`-`) and counted as non-matches.

---

## ✨ Key Features

1. **Dual Sequence Input Modes**:
   - Paste raw DNA sequences manually.
   - Upload FASTA files parsed automatically using Biopython (`Bio.SeqIO`).
2. **Robust Nucleotide Validation**:
   - Converts lowercase letters to uppercase and removes all whitespace/linebreaks.
   - Accepts standard DNA nucleotides (`A`, `T`, `G`, `C`) and optionally `N` (unknown/ambiguous base).
   - Detailed error reporting highlighting exact positions of any invalid characters.
3. **Comprehensive Metrics Dashboard**:
   - Sequence 1 length & GC content percentage.
   - Sequence 2 length & GC content percentage.
   - Number and percentage of matching positions.
   - Number and percentage of mismatching positions.
   - Number and percentage of gap positions.
   - Positional similarity score (0.0% to 100.0%).
4. **Color-Coded Visual Alignment**:
   - **Green** (`#10B981` / `#DCFCE7`): Matching nucleotides.
   - **Red** (`#EF4444` / `#FEE2E2`): Mismatching nucleotides.
   - **Grey** (`#9CA3AF` / `#F1F5F9`): Gaps / trailing missing positions.
   - Position numbers and match indicator symbols (`|`, `•`, `—`).
5. **Scientific Visualizations**:
   - **Positional Bar Chart**: Breakdown of Matches, Mismatches, and Gaps.
   - **Donut Chart**: Circular display of overall positional similarity percentage.
   - **Linear Sequence Distribution Track**: Visual map across sequence length.
6. **Result Exports**:
   - Download position-by-position comparison table as CSV.
   - Download formatted text report (`.txt`) for lab notebooks or assignments.

---

## 🛠️ Technology Stack

| Library / Tool | Version | Purpose in Project |
| :--- | :--- | :--- |
| **Python** | 3.10+ | Core programming logic and execution |
| **Streamlit** | >= 1.30.0 | Interactive web UI, sidebar navigation, metric cards, reactive widgets |
| **Biopython** | >= 1.80 | Reading and parsing FASTA files (`Bio.SeqIO`) and biological sequences (`Bio.Seq`) |
| **Matplotlib** | >= 3.7.0 | High-DPI bar charts, donut charts, and linear sequence track plots |
| **Pandas** | >= 2.0.0 | Tabular data representation, position indexing, and CSV generation |

---

## 📁 Directory Structure

```text
dna_similarity_checker/
│
├── app.py                 # Streamlit web application & user interface
├── sequence_utils.py      # Core bioinformatics logic: validation, Biopython FASTA parsing, math
├── visualization.py       # Matplotlib figures and HTML color-coded alignment views
├── requirements.txt       # Python dependencies list
└── README.md              # Project documentation and user guide
```

---

## 🔍 File Purpose & Architecture (Beginner-Friendly Explanation)

### 1. `sequence_utils.py`
This module acts as the "computational engine" of the application:
- **`clean_sequence(raw_sequence)`**: Strips out whitespace, newlines, and tabs, then converts lowercase letters to uppercase.
- **`validate_dna_sequence(sequence, allow_n)`**: Checks every single nucleotide against `{A, T, G, C, N}` and reports any illegitimate symbols with their exact positions.
- **`parse_fasta(file_or_text)`**: Uses Biopython's `SeqIO.parse` to extract sequence IDs and nucleotide sequences from uploaded `.fasta` files.
- **`calculate_gc_content(sequence)`**: Computes the percentage of Guanine and Cytosine bases in a sequence.
- **`calculate_positional_similarity(seq1, seq2)`**: Compares nucleotides at each index, pads unequal lengths with `-`, and calculates matching, mismatching, and gap counts.
- **`generate_text_report(stats, ...)`**: Formats analysis metrics into a clean, printable text report.

### 2. `visualization.py`
This module is responsible for rendering all graphics:
- **`plot_comparison_barchart(stats)`**: Creates a Matplotlib bar graph showing the counts and percentages for Matches, Mismatches, and Gaps.
- **`plot_similarity_donut(stats)`**: Generates a donut chart displaying overall similarity percentage.
- **`plot_position_track(comparison_rows)`**: Renders a barcode-style linear track illustrating the location of matches and mismatches along the 5' to 3' sequence.
- **`render_html_sequence_alignment(...)`**: Builds clean HTML/CSS elements to render nucleotide boxes color-coded in green, red, and grey with position numbers.

### 3. `app.py`
This is the Streamlit frontend script that glues everything together:
- Manages the multi-page sidebar navigation (`Home`, `Sequence Comparison`, `Results & Analytics`, `About the Project`).
- Provides sample preset buttons (Standard Test, Unequal Length, Sickle Cell Allele).
- Renders responsive metric cards and interpretation callout banners.
- Provides interactive download buttons for CSV tables and `.txt` reports.

---

## 🚀 Installation Guide

### Prerequisites
Make sure Python 3.10 or newer is installed on your computer.

### Step 1: Open a terminal / command prompt
Navigate to the project directory:
```bash
cd "d:\ayush biopython\dna_similarity_checker"
```

### Step 2: Install dependencies
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

---

## 💻 Running the Application

To start the Streamlit local server:
```bash
streamlit run app.py
```

Streamlit will launch the web application in your default browser at:
```text
http://localhost:8501
```

---

## 🧪 Verification & Test Cases

### Test Case 1: Standard Reference vs. Variant (From Prompt)
- **Sequence 1**: `ATGCGTACGTAG`
- **Sequence 2**: `ATGCGTTCGTAG`
- **Expected Results**:
  - Length of Sequence 1: `12` nt
  - Length of Sequence 2: `12` nt
  - Matching positions: `11`
  - Mismatching positions: `1` (Position 7: A vs T)
  - Gap positions: `0`
  - Similarity percentage: **91.67%** (Interpretation: *Very High Positional Similarity*)

### Test Case 2: Unequal Sequence Lengths
- **Sequence 1**: `ATGCGTAGCTAGCTAGCTA` (19 nt)
- **Sequence 2**: `ATGCGTAGCTAG` (12 nt)
- **Expected Results**:
  - Max Length: `19`
  - Matches: `12`
  - Gaps: `7`
  - Similarity: **63.16%** (Positions 13–19 counted as non-matching gaps)

### Test Case 3: Invalid Characters
- **Sequence 1**: `ATGCXTYZ`
- **Expected Results**: Validation error clearly displayed:
  > *"Invalid character(s) detected: X, Y, Z. DNA sequences must only contain A, T, G, C, N."*

---

## 🔬 Positional Comparison vs. Biological Alignment

In a beginner project, comparing sequences position-by-position is intuitive and demonstrates string indexing and algorithmic counting. However, bioinformaticians must understand the difference:

| Feature | Positional Comparison (This Project) | Global Alignment (Needleman-Wunsch) | Local Alignment (Smith-Waterman / BLAST) |
| :--- | :--- | :--- | :--- |
| **Method** | Index-by-index ($i$ with $i$) | Dynamic programming with gap penalties | Identifies high-scoring local regions |
| **Indels / Frameshifts** | A single insertion at the beginning causes all following bases to mismatch | Inserts optimal gaps to realign downstream matches | Finds matching blocks regardless of offset |
| **Best Used For** | Point mutation/SNP verification in pre-aligned sequences | Full-length homologous gene comparison | Finding conserved domains & database searches |
| **Complexity** | $O(N)$ linear time | $O(N \times M)$ quadratic time | $O(N \times M)$ dynamic programming |

---

## 📄 License
This educational project is distributed as open-source for classroom, academic, and beginner bioinformatics training.
