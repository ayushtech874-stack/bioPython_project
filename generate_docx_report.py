"""
generate_docx_report.py
=======================
Generates a comprehensive, academic/professional project report in Microsoft Word (.docx)
format for the DNA Sequence Similarity Checker.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, fill_hex):
    """Set the background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set cell internal padding."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def create_report(output_path="DNA_Sequence_Similarity_Checker_Project_Report.docx"):
    doc = Document()

    # Page Margins: 1 inch all around
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    COLOR_NAVY = RGBColor(15, 23, 42)      # #0F172A
    COLOR_TEAL = RGBColor(13, 148, 136)    # #0D9488
    COLOR_SLATE = RGBColor(71, 85, 105)    # #475569

    # -------------------------------------------------------------
    # Title & Metadata
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("PROJECT REPORT")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(13)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_TEAL

    main_title_p = doc.add_paragraph()
    main_title_p.paragraph_format.space_after = Pt(8)
    run_m = main_title_p.add_run("DNA Sequence Similarity Checker")
    run_m.font.name = "Arial"
    run_m.font.size = Pt(24)
    run_m.font.bold = True
    run_m.font.color.rgb = COLOR_NAVY

    sub_title_p = doc.add_paragraph()
    sub_title_p.paragraph_format.space_after = Pt(20)
    run_sub = sub_title_p.add_run("A Modern Bioinformatics Web Application for Positional DNA Comparison & Visual Mutation Analysis")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(13)
    run_sub.font.italic = True
    run_sub.font.color.rgb = COLOR_SLATE

    # Meta Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Technology Stack", "Python 3.10+, Streamlit, Biopython, Matplotlib, Pandas"),
        ("Application Scope", "Bioinformatics, Genomics Education, Sequence Analysis"),
        ("Version & Status", "Version 1.0.0 (Production / Verified)"),
        ("Repository", "https://github.com/ayushtech874-stack/bioPython_project.git")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = COLOR_NAVY

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_SLATE

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # -------------------------------------------------------------
    # 1. Executive Summary
    # -------------------------------------------------------------
    h1 = doc.add_heading(level=1)
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("1. Executive Summary")
    r_h1.font.name = "Arial"
    r_h1.font.color.rgb = COLOR_NAVY

    p_exec = doc.add_paragraph()
    p_exec.paragraph_format.line_spacing = 1.15
    p_exec.paragraph_format.space_after = Pt(10)
    p_exec.add_run(
        "The DNA Sequence Similarity Checker is an educational, production-ready bioinformatics web application "
        "engineered in Python to bridge the gap between abstract molecular genetics concepts and computational implementation. "
        "Designed specifically for college-level students and researchers, the application provides an intuitive platform "
        "to compare DNA sequences position-by-position, validate nucleotide fidelity (A, T, G, C, N), calculate percentage similarity, "
        "and visualize point mutations using a color-coded alignment interface and publication-quality Matplotlib charts."
    )

    # -------------------------------------------------------------
    # 2. Introduction & Biological Relevance
    # -------------------------------------------------------------
    h2 = doc.add_heading(level=1)
    h2.paragraph_format.space_before = Pt(18)
    h2.paragraph_format.space_after = Pt(6)
    r_h2 = h2.add_run("2. Introduction & Biological Significance")
    r_h2.font.name = "Arial"
    r_h2.font.color.rgb = COLOR_NAVY

    p_bio = doc.add_paragraph()
    p_bio.paragraph_format.line_spacing = 1.15
    p_bio.paragraph_format.space_after = Pt(10)
    p_bio.add_run(
        "Deoxyribonucleic acid (DNA) is the hereditary material in humans and nearly all living organisms. "
        "Comparing two homologous or variant DNA sequences is one of the most fundamental operations in computational genomics. "
        "Such comparisons permit biologists to:\n"
    )

    bullet_points = [
        ("Identify Single Nucleotide Polymorphisms (SNPs): ", "Single-base changes that account for genetic diversity and susceptibility to diseases."),
        ("Diagnose Genetic Disorders: ", "For example, identifying point mutations such as the A -> T transversion in the Beta-Globin gene responsible for Sickle Cell Anemia."),
        ("Measure Sequence Divergence: ", "Quantifying the rate of evolutionary drift between closely related strains or alleles."),
        ("Quality Control in Sequencing: ", "Validating read accuracy against reference genomes in Sanger and Next-Generation Sequencing (NGS) workflows.")
    ]
    for b_title, b_desc in bullet_points:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        run_bt = bp.add_run(b_title)
        run_bt.font.bold = True
        run_bt.font.color.rgb = COLOR_NAVY
        bp.add_run(b_desc)

    # -------------------------------------------------------------
    # 3. Project Objectives
    # -------------------------------------------------------------
    h3 = doc.add_heading(level=1)
    h3.paragraph_format.space_before = Pt(18)
    h3.paragraph_format.space_after = Pt(6)
    r_h3 = h3.add_run("3. Project Objectives & Specifications")
    r_h3.font.name = "Arial"
    r_h3.font.color.rgb = COLOR_NAVY

    doc.add_paragraph(
        "The project was designed to meet strict functional, biological, and user experience requirements:"
    )
    reqs = [
        "Interactive Web Interface: Clean, scientific dashboard created using Streamlit without complex JavaScript/Node.js frameworks.",
        "Biopython Integration: Parsing single or multi-line FASTA files directly via Bio.SeqIO with sequence validation.",
        "Strict Nucleotide Validation: Ensuring sequences contain only legitimate DNA bases (A, T, G, C, and optional N), stripping whitespace, and uppercasing characters.",
        "Positional Comparison Algorithm: Formulated as Similarity (%) = (Matches / Maximum Length) * 100, treating missing positions in unequal length sequences as non-matching gaps.",
        "Visual Color-Coded Alignment: Highlighting matching nucleotides in green, mismatching nucleotides in red, and gaps in grey, alongside position rulers.",
        "Multi-Angle Graphical Analytics: Generating Matplotlib composition bar charts, similarity donut charts, and 5' -> 3' sequence track maps.",
        "Data Export Suite: Facilitating one-click downloads of positional comparison tables (CSV) and formatted laboratory text reports (.txt)."
    ]
    for req in reqs:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.add_run(req)

    # -------------------------------------------------------------
    # 4. Mathematical Formulation & Algorithmic Design
    # -------------------------------------------------------------
    h4 = doc.add_heading(level=1)
    h4.paragraph_format.space_before = Pt(18)
    h4.paragraph_format.space_after = Pt(6)
    r_h4 = h4.add_run("4. Mathematical Formulation & Algorithmic Design")
    r_h4.font.name = "Arial"
    r_h4.font.color.rgb = COLOR_NAVY

    doc.add_paragraph(
        "Let Sequence 1 be represented as S1 of length L1, and Sequence 2 as S2 of length L2. "
        "The maximum sequence length is defined as:"
    )
    p_eq1 = doc.add_paragraph()
    p_eq1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq1 = p_eq1.add_run("L_max = max(length(S1), length(S2))")
    r_eq1.font.bold = True
    r_eq1.font.color.rgb = COLOR_NAVY

    doc.add_paragraph(
        "If L1 != L2, the shorter sequence is padded with trailing gap characters ('-') up to length L_max. "
        "At each discrete position i (where 1 <= i <= L_max), the positional status C(i) is evaluated:"
    )

    p_eq2 = doc.add_paragraph()
    p_eq2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq2 = p_eq2.add_run(
        "C(i) = 'Gap'       if S1[i] == '-' or S2[i] == '-'\n"
        "C(i) = 'Match'     if S1[i] == S2[i]\n"
        "C(i) = 'Mismatch'  if S1[i] != S2[i]"
    )
    r_eq2.font.bold = True
    r_eq2.font.color.rgb = COLOR_NAVY

    doc.add_paragraph(
        "The overall Positional Similarity Percentage is subsequently calculated as:"
    )
    p_eq3 = doc.add_paragraph()
    p_eq3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq3 = p_eq3.add_run("Similarity (%) = ( Number of Matches / L_max ) * 100")
    r_eq3.font.bold = True
    r_eq3.font.size = Pt(12)
    r_eq3.font.color.rgb = COLOR_TEAL

    # Table of Interpretation Categories
    cat_table = doc.add_table(rows=5, cols=3)
    cat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Similarity Range", "Interpretation Category", "Description"]
    for j, h in enumerate(headers):
        cell = cat_table.rows[0].cells[j]
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    cat_rows = [
        ("90% – 100%", "Very High Positional Similarity", "Near-identical sequences; high sequence fidelity with few or zero point mutations."),
        ("70% – 89%", "High Positional Similarity", "Substantial sequence identity; exhibits moderate polymorphism or single-codon shifts."),
        ("40% – 69%", "Moderate Positional Similarity", "Partial homology; noticeable divergence or moderate length discrepancies."),
        ("Below 40%", "Low Positional Similarity", "High divergence, random alignment, or completely out-of-frame reading sequences.")
    ]
    for i, (rng, label, desc) in enumerate(cat_rows, start=1):
        row = cat_table.rows[i]
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, txt in enumerate([rng, label, desc]):
            cell = row.cells[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(txt)
            r.font.size = Pt(9.5)
            if j == 1:
                r.font.bold = True
            r.font.color.rgb = COLOR_NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # 5. Software Architecture & Implementation Details
    # -------------------------------------------------------------
    h5 = doc.add_heading(level=1)
    h5.paragraph_format.space_before = Pt(18)
    h5.paragraph_format.space_after = Pt(6)
    r_h5 = h5.add_run("5. Software Architecture & Module Descriptions")
    r_h5.font.name = "Arial"
    r_h5.font.color.rgb = COLOR_NAVY

    doc.add_paragraph(
        "The application follows a strictly modular, decoupled architecture where biological utilities, "
        "visualization routines, and user interface components operate independently:"
    )

    modules = [
        ("app.py (Streamlit Frontend)", 
         "Serves as the user interface orchestrator. Implements session state persistence across multi-page navigation "
         "(Home, Sequence Comparison, Results & Analytics, About the Project), user input management, dynamic metric cards, "
         "error alerts, and download triggers."),
        ("sequence_utils.py (Bioinformatics Engine)", 
         "Contains clean, functional routines for sequence sanitization, validation against {A, T, G, C, N}, Biopython Bio.SeqIO FASTA "
         "parsing, GC-content calculations, and position-by-position comparison calculations."),
        ("visualization.py (Data Visualization Subsystem)", 
         "Constructs publication-ready Matplotlib figures (Bar charts, Donut charts, and Positional tracks) using non-interactive Agg "
         "backends. Also renders responsive HTML/CSS alignment markup with green, red, and grey nucleotide boxes."),
        ("test_checker.py (Automated Test Suite)", 
         "Provides continuous verification with 8 unit tests covering benchmark inputs, unequal lengths, invalid characters, "
         "FASTA parsing, and figure generation.")
    ]
    for mod_title, mod_desc in modules:
        mp = doc.add_paragraph()
        mp.paragraph_format.space_after = Pt(6)
        r_mt = mp.add_run(f"• {mod_title}: ")
        r_mt.font.bold = True
        r_mt.font.color.rgb = COLOR_TEAL
        mp.add_run(mod_desc)

    # -------------------------------------------------------------
    # 6. Experimental Verification & Test Cases
    # -------------------------------------------------------------
    h6 = doc.add_heading(level=1)
    h6.paragraph_format.space_before = Pt(18)
    h6.paragraph_format.space_after = Pt(6)
    r_h6 = h6.add_run("6. Experimental Verification & Test Cases")
    r_h6.font.name = "Arial"
    r_h6.font.color.rgb = COLOR_NAVY

    doc.add_paragraph(
        "To guarantee mathematical fidelity and software robustness, the application was evaluated against multiple biological test cases:"
    )

    # Test Table
    test_table = doc.add_table(rows=4, cols=4)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Test Scenario", "Input Sequences", "Expected vs Observed", "Result"]
    for j, h in enumerate(t_headers):
        cell = test_table.rows[0].cells[j]
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_data = [
        ("Benchmark Test (12 nt)", "S1: ATGCGTACGTAG\nS2: ATGCGTTCGTAG", "Matches: 11, Mismatches: 1\nSimilarity: 91.67%", "PASSED (100% Match)"),
        ("Unequal Length Test", "S1: ATGCGTAGCTAGCTAGCTA (19 nt)\nS2: ATGCGTAGCTAG (12 nt)", "Matches: 12, Gaps: 7\nSimilarity: 63.16%", "PASSED (Trailing Gaps)"),
        ("Sickle Cell Gene Test", "HbA: ACTCCTGAGGAGAAGTCT\nHbS: ACTCCTGTGGAGAAGTCT", "Matches: 17, Mismatch: 1\nSimilarity: 94.44%", "PASSED (SNP Detected)")
    ]
    for i, (scen, inp, obs, res) in enumerate(test_data, start=1):
        row = test_table.rows[i]
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, txt in enumerate([scen, inp, obs, res]):
            cell = row.cells[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(txt)
            r.font.size = Pt(9.5)
            if j == 3:
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)
            else:
                r.font.color.rgb = COLOR_NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # 7. Comparison: Positional Matching vs. Biological Alignment
    # -------------------------------------------------------------
    h7 = doc.add_heading(level=1)
    h7.paragraph_format.space_before = Pt(18)
    h7.paragraph_format.space_after = Pt(6)
    r_h7 = h7.add_run("7. Positional Comparison vs. Advanced Sequence Alignment")
    r_h7.font.name = "Arial"
    r_h7.font.color.rgb = COLOR_NAVY

    doc.add_paragraph(
        "A critical educational objective of this project is clarifying the algorithmic differences between "
        "simple positional comparison and dynamic programming sequence alignment:"
    )

    comp_table = doc.add_table(rows=5, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["Attribute", "Positional Comparison (This Project)", "Dynamic Alignment (Needleman-Wunsch / BLAST)"]
    for j, h in enumerate(c_headers):
        cell = comp_table.rows[0].cells[j]
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    comp_data = [
        ("Alignment Logic", "Strict index-by-index comparison (S1[i] vs S2[i]).", "Inserts gaps dynamically to optimize an alignment score matrix."),
        ("Frameshift Tolerance", "Zero tolerance. A single deletion shifts all downstream bases.", "High tolerance. Optimally places indels to preserve downstream matches."),
        ("Primary Use Case", "Single Nucleotide Polymorphism (SNP) verification and point mutations.", "Homologous gene search, evolutionary phylogenetic distance, remote orthologs."),
        ("Computational Complexity", "O(N) linear time complexity.", "O(N x M) quadratic time complexity (or heuristic O(N)).")
    ]
    for i, (attr, p_col, a_col) in enumerate(comp_data, start=1):
        row = comp_table.rows[i]
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, txt in enumerate([attr, p_col, a_col]):
            cell = row.cells[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(txt)
            r.font.size = Pt(9.5)
            if j == 0:
                r.font.bold = True
            r.font.color.rgb = COLOR_NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # 8. How to Run & User Guide
    # -------------------------------------------------------------
    h8 = doc.add_heading(level=1)
    h8.paragraph_format.space_before = Pt(18)
    h8.paragraph_format.space_after = Pt(6)
    r_h8 = h8.add_run("8. Installation & Execution Guide")
    r_h8.font.name = "Arial"
    r_h8.font.color.rgb = COLOR_NAVY

    doc.add_paragraph(
        "Follow these steps to run the application locally on Windows, macOS, or Linux:"
    )

    run_steps = [
        ("Step 1: Clone the Repository: ", "git clone https://github.com/ayushtech874-stack/bioPython_project.git && cd bioPython_project"),
        ("Step 2: Install Python Dependencies: ", "pip install -r requirements.txt"),
        ("Step 3: Launch Web Application: ", "streamlit run dna_similarity_checker/app.py   (or run: python run_app.py)"),
        ("Step 4: Open in Browser: ", "Navigate to http://localhost:8501 to access the interactive dashboard.")
    ]
    for s_title, s_code in run_steps:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        r_st = p.add_run(s_title)
        r_st.font.bold = True
        r_st.font.color.rgb = COLOR_NAVY
        r_sc = p.add_run(s_code)
        r_sc.font.name = "Courier New"
        r_sc.font.size = Pt(9.5)

    # -------------------------------------------------------------
    # 9. Conclusion & Educational Value
    # -------------------------------------------------------------
    h9 = doc.add_heading(level=1)
    h9.paragraph_format.space_before = Pt(18)
    h9.paragraph_format.space_after = Pt(6)
    r_h9 = h9.add_run("9. Conclusion")
    r_h9.font.name = "Arial"
    r_h9.font.color.rgb = COLOR_NAVY

    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.line_spacing = 1.15
    p_conc.paragraph_format.space_after = Pt(10)
    p_conc.add_run(
        "The DNA Sequence Similarity Checker demonstrates the successful integration of modern Python data science libraries "
        "(Streamlit, Matplotlib, Pandas) with specialized bioinformatics frameworks (Biopython). The application delivers "
        "accurate, lightning-fast positional comparisons, real-time nucleotide error diagnostic alerts, and accessible visual "
        "feedback. It serves as an exemplary educational foundation for aspiring bioinformaticians, geneticists, and computer scientists."
    )

    # Save document
    doc.save(output_path)
    print(f"Report successfully saved to: {output_path}")


if __name__ == "__main__":
    create_report("DNA_Sequence_Similarity_Checker_Project_Report.docx")
