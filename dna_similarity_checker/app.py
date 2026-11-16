"""
app.py
======
Main Streamlit application for the DNA Sequence Similarity Checker.

Features:
- Manual DNA sequence entry & FASTA file upload via Biopython
- Real-time DNA validation (A, T, G, C, and optional N)
- Position-by-position similarity calculation
- Interactive metric cards and interpretation guidelines
- Color-coded visual sequence alignment (Green=Match, Red=Mismatch, Grey=Gap)
- Matplotlib analytical charts (Bar chart, Donut chart, Positional track)
- CSV and Text report downloads
- Educational scientific dashboard design
"""

import os
import sys
import tempfile
import pandas as pd
import streamlit as st

# Ensure safe matplotlib config dir
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "matplotlib"))

# Local imports
from sequence_utils import (
    clean_sequence,
    validate_dna_sequence,
    parse_fasta,
    calculate_positional_similarity,
    generate_text_report
)
from visualization import (
    plot_comparison_barchart,
    plot_similarity_donut,
    plot_position_track,
    render_html_sequence_alignment
)

# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="DNA Sequence Similarity Checker",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom Scientific Dashboard CSS
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Main typography and background styling */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Header colors */
h1, h2, h3 {
    color: #0F172A !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

/* Metric card styling */
.metric-container {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04);
    margin-bottom: 12px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.metric-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
}
.metric-title {
    font-size: 12px;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 26px;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.1;
}
.metric-subtitle {
    font-size: 12px;
    color: #0D9488;
    font-weight: 600;
    margin-top: 4px;
}

/* Interpretation banner */
.interpretation-banner {
    border-radius: 12px;
    padding: 18px 22px;
    margin: 18px 0;
    border-left: 6px solid;
}

/* Disclaimer box */
.disclaimer-box {
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13px;
    color: #475569;
    margin: 15px 0;
}

/* Hero card on Home */
.hero-card {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: #FFFFFF;
    border-radius: 16px;
    padding: 30px 36px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
}
.hero-title {
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF !important;
    margin-bottom: 10px;
}
.hero-desc {
    font-size: 15px;
    color: #E2E8F0;
    line-height: 1.6;
    max-width: 900px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "seq1_input" not in st.session_state:
    st.session_state.seq1_input = "ATGCGTACGTAG"
if "seq2_input" not in st.session_state:
    st.session_state.seq2_input = "ATGCGTTCGTAG"
if "seq1_name" not in st.session_state:
    st.session_state.seq1_name = "Sequence 1"
if "seq2_name" not in st.session_state:
    st.session_state.seq2_name = "Sequence 2"
if "last_results" not in st.session_state:
    st.session_state.last_results = None

# -----------------------------------------------------------------------------
# Helper Sample Loaders
# -----------------------------------------------------------------------------
def load_sample_prompt_test():
    st.session_state.seq1_input = "ATGCGTACGTAG"
    st.session_state.seq2_input = "ATGCGTTCGTAG"
    st.session_state.seq1_name = "Reference_Seq1"
    st.session_state.seq2_name = "Variant_Seq2"
    st.session_state.last_results = None

def load_sample_unequal():
    st.session_state.seq1_input = "ATGCGTAGCTAGCTAGCTA"
    st.session_state.seq2_input = "ATGCGTAGCTAG"
    st.session_state.seq1_name = "Full_Gene"
    st.session_state.seq2_name = "Truncated_Gene"
    st.session_state.last_results = None

def load_sample_sickle_cell():
    # Real-world biological snippet: Human Beta-Globin (HBB) codon 6 (Normal A vs Sickle T)
    st.session_state.seq1_input = "ACTCCTGAGGAGAAGTCT"
    st.session_state.seq2_input = "ACTCCTGTGGAGAAGTCT"
    st.session_state.seq1_name = "HbA_Normal_Allele"
    st.session_state.seq2_name = "HbS_Sickle_Allele"
    st.session_state.last_results = None

def clear_all_inputs():
    st.session_state.seq1_input = ""
    st.session_state.seq2_input = ""
    st.session_state.seq1_name = "Sequence 1"
    st.session_state.seq2_name = "Sequence 2"
    st.session_state.last_results = None

# -----------------------------------------------------------------------------
# Sidebar Navigation & Settings
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧬 Navigation")
    menu = st.radio(
        "Go to page:",
        ["🏠 Home", "🧬 Sequence Comparison", "📊 Results & Analytics", "ℹ️ About the Project"],
        index=1  # Default directly to Comparison for quick use
    )

    st.markdown("---")
    st.markdown("### ⚙️ Validation Settings")
    allow_n = st.checkbox("Allow 'N' (Unknown nucleotide)", value=True,
                          help="Permits 'N' representing an ambiguous or unknown nucleotide.")

    st.markdown("---")
    st.markdown("### 🧪 Quick Presets")
    st.caption("Load verified test pairs:")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("Standard Test", on_click=load_sample_prompt_test, use_container_width=True,
                     help="12 nt test case with 1 mismatch (91.67%)"):
            pass
    with col_p2:
        if st.button("Unequal Length", on_click=load_sample_unequal, use_container_width=True,
                     help="19 nt vs 12 nt with gap handling"):
            pass
    if st.button("Sickle Cell Gene Mutation", on_click=load_sample_sickle_cell, use_container_width=True,
                 help="Human Beta-Globin HbA vs HbS point mutation"):
        pass

    st.markdown("---")
    if st.button("🗑️ Clear Inputs", on_click=clear_all_inputs, use_container_width=True):
        st.toast("Inputs cleared!", icon="🧹")

    st.markdown("---")
    st.caption("DNA Sequence Similarity Checker v1.0\nDesigned for beginner bioinformatics.")

# -----------------------------------------------------------------------------
# PAGE 1: HOME
# -----------------------------------------------------------------------------
if menu == "🏠 Home":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">🧬 DNA Sequence Similarity Checker</div>
        <div class="hero-desc">
            A beginner-friendly bioinformatics tool for calculating positional nucleotide identity,
            visualizing sequence matches and mismatches in color, and generating graphical comparison analytics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 🔬 How It Works")
        st.markdown("""
        Comparing DNA sequences is a fundamental task in molecular biology, genomics, and computational bioinformatics.
        This application performs an **unaligned, position-by-position comparison** between two DNA sequences:

        1. **Input & Cleaning**: Paste DNA sequences directly or upload standard FASTA files. Lowercase nucleotides are automatically converted to uppercase, and whitespace is removed.
        2. **Validation**: The tool validates that only legitimate DNA characters (**A, T, G, C**, and optionally **N**) are present.
        3. **Positional Comparison**: At each nucleotide index $i$, the nucleotides are compared:
           - **Match**: Both sequences share the exact same nucleotide (`A==A`, `T==T`, etc.).
           - **Mismatch**: The nucleotides differ (`A != G`).
           - **Gap**: If sequences are unequal in length, the trailing positions in the shorter sequence are padded with gaps (`-`) and counted as non-matches.
        4. **Similarity Metric**:
        """)

        st.latex(r"\text{Similarity (\%)} = \left( \frac{\text{Matching Positions}}{\max(\text{Length}_1, \text{Length}_2)} \right) \times 100")

        st.markdown("""
        5. **Visual & Graphical Feedback**: See color-coded alignment maps, interactive tables, and publication-ready Matplotlib charts.
        """)

    with col2:
        st.markdown("### 💡 Key Features")
        st.markdown("""
        - ✍️ **Dual Input Modes**: Manual pasting or FASTA file upload with Biopython.
        - 🛡️ **Strict DNA Validation**: Instant diagnostic feedback on invalid characters.
        - 🎨 **Visual Alignment**: Color-coded nucleotide badges (Green = Match, Red = Mismatch, Grey = Gap).
        - 📊 **Matplotlib Visualizations**: High-resolution bar charts, similarity donuts, and positional track plots.
        - 📥 **Export Reports**: Instant download of CSV position logs and formatted text reports.
        """)

        st.info("👉 Ready to test? Head over to **🧬 Sequence Comparison** in the sidebar!")

# -----------------------------------------------------------------------------
# PAGE 2: SEQUENCE COMPARISON
# -----------------------------------------------------------------------------
elif menu == "🧬 Sequence Comparison":
    st.title("🧬 DNA Sequence Comparison")
    st.markdown("Enter or upload two DNA sequences below to calculate their similarity and inspect their positional alignment.")

    # Two columns for inputs
    col_input1, col_input2 = st.columns(2)

    with col_input1:
        st.subheader("Sequence 1 (Reference)")
        input_mode1 = st.radio("Input method for Sequence 1:", ["Manual Input", "Upload FASTA"], key="mode1", horizontal=True)

        if input_mode1 == "Manual Input":
            seq1_raw = st.text_area(
                "Enter DNA Sequence 1:",
                value=st.session_state.seq1_input,
                height=130,
                placeholder="e.g. ATGCGTACGTAG",
                key="seq1_text_widget"
            )
            seq1_name = st.text_input("Sequence 1 Label / ID:", value=st.session_state.seq1_name, key="seq1_name_widget")
        else:
            uploaded_file1 = st.file_uploader("Upload FASTA file for Sequence 1:", type=["fasta", "fa", "fna", "txt"], key="fasta1")
            seq1_name = "Sequence 1"
            seq1_raw = ""
            if uploaded_file1 is not None:
                success, f_id, f_seq, err = parse_fasta(uploaded_file1)
                if success:
                    seq1_raw = f_seq
                    seq1_name = f_id
                    st.success(f"Loaded record: `{seq1_name}` ({len(seq1_raw)} nt)")
                else:
                    st.error(err)

    with col_input2:
        st.subheader("Sequence 2 (Query / Variant)")
        input_mode2 = st.radio("Input method for Sequence 2:", ["Manual Input", "Upload FASTA"], key="mode2", horizontal=True)

        if input_mode2 == "Manual Input":
            seq2_raw = st.text_area(
                "Enter DNA Sequence 2:",
                value=st.session_state.seq2_input,
                height=130,
                placeholder="e.g. ATGCGTTCGTAG",
                key="seq2_text_widget"
            )
            seq2_name = st.text_input("Sequence 2 Label / ID:", value=st.session_state.seq2_name, key="seq2_name_widget")
        else:
            uploaded_file2 = st.file_uploader("Upload FASTA file for Sequence 2:", type=["fasta", "fa", "fna", "txt"], key="fasta2")
            seq2_name = "Sequence 2"
            seq2_raw = ""
            if uploaded_file2 is not None:
                success, f_id, f_seq, err = parse_fasta(uploaded_file2)
                if success:
                    seq2_raw = f_seq
                    seq2_name = f_id
                    st.success(f"Loaded record: `{seq2_name}` ({len(seq2_raw)} nt)")
                else:
                    st.error(err)

    st.markdown("---")

    # Action Button
    run_col1, run_col2 = st.columns([1, 4])
    with run_col1:
        run_btn = st.button("🚀 Compare Sequences", type="primary", use_container_width=True)

    # Clean inputs
    cleaned_seq1 = clean_sequence(seq1_raw)
    cleaned_seq2 = clean_sequence(seq2_raw)

    # Trigger calculation when button clicked or if inputs changed
    if run_btn or st.session_state.last_results is None:
        # Perform validation
        valid1, errors1 = validate_dna_sequence(cleaned_seq1, allow_n=allow_n)
        valid2, errors2 = validate_dna_sequence(cleaned_seq2, allow_n=allow_n)

        if not valid1:
            st.error(f"❌ **Sequence 1 Error:** {errors1[0]}")
            if len(errors1) > 1:
                st.caption(errors1[1])
            st.session_state.last_results = None
        elif not valid2:
            st.error(f"❌ **Sequence 2 Error:** {errors2[0]}")
            if len(errors2) > 1:
                st.caption(errors2[1])
            st.session_state.last_results = None
        else:
            # Perform similarity calculation
            results = calculate_positional_similarity(cleaned_seq1, cleaned_seq2)
            results["seq1_name"] = seq1_name or "Sequence 1"
            results["seq2_name"] = seq2_name or "Sequence 2"
            st.session_state.last_results = results
            st.session_state.seq1_input = cleaned_seq1
            st.session_state.seq2_input = cleaned_seq2
            st.session_state.seq1_name = seq1_name
            st.session_state.seq2_name = seq2_name

    # Display results if available
    res = st.session_state.last_results
    if res is not None:
        st.markdown("## 📊 Comparison Summary")

        # Metric Cards Row
        m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)

        with m_col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Seq 1 Length</div>
                <div class="metric-value">{res['len1']} <span style="font-size:14px;color:#64748B;">nt</span></div>
                <div class="metric-subtitle">GC: {res['gc_content1']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Seq 2 Length</div>
                <div class="metric-value">{res['len2']} <span style="font-size:14px;color:#64748B;">nt</span></div>
                <div class="metric-subtitle">GC: {res['gc_content2']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Matching</div>
                <div class="metric-value" style="color:#10B981;">{res['matches']}</div>
                <div class="metric-subtitle" style="color:#10B981;">{res['match_percentage']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Mismatching</div>
                <div class="metric-value" style="color:#EF4444;">{res['mismatches']}</div>
                <div class="metric-subtitle" style="color:#EF4444;">{res['mismatch_percentage']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col5:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">Gaps</div>
                <div class="metric-value" style="color:#64748B;">{res['gaps']}</div>
                <div class="metric-subtitle" style="color:#64748B;">{res['gap_percentage']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col6:
            st.markdown(f"""
            <div class="metric-container" style="border-color:{res['interpretation_color']};">
                <div class="metric-title">Similarity</div>
                <div class="metric-value" style="color:{res['interpretation_color']};">{res['similarity_percentage']}%</div>
                <div class="metric-subtitle" style="color:{res['interpretation_color']};">Positional</div>
            </div>
            """, unsafe_allow_html=True)

        # Interpretation banner
        st.markdown(f"""
        <div class="interpretation-banner" style="background-color: {res['interpretation_color']}15; border-color: {res['interpretation_color']};">
            <h4 style="margin: 0; color: {res['interpretation_color']}; font-weight: 700;">
                🎯 Result: {res['interpretation_label']} ({res['similarity_percentage']}%)
            </h4>
            <p style="margin: 6px 0 0 0; color: #1E293B; font-size: 14px;">
                {res['interpretation_desc']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Educational disclaimer
        st.markdown("""
        <div class="disclaimer-box">
            ℹ️ <strong>Educational Note:</strong> This application implements a strict <em>position-by-position comparison</em>.
            For unequal-length sequences, missing positions are treated as non-matching gaps.
            These categories are illustrative and do not establish evolutionary or biological relatedness (which require dynamic programming algorithms like Needleman-Wunsch or BLAST).
        </div>
        """, unsafe_allow_html=True)

        # Visual Alignment Section
        st.markdown("### 🎨 Visual Sequence Alignment")
        chunk_opt = st.select_slider(
            "Display chunk size (nucleotides per line):",
            options=[15, 20, 25, 30, 50],
            value=25,
            key="chunk_slider"
        )

        align_html = render_html_sequence_alignment(
            res["aligned_seq1"],
            res["aligned_seq2"],
            res["comparison_rows"],
            chunk_size=chunk_opt
        )
        st.components.v1.html(align_html, height=min(550, max(260, (res['max_len'] // chunk_opt + 1) * 165)), scrolling=True)

        # Dataframe inspection
        with st.expander("🔍 View Detailed Position-by-Position Table"):
            df = pd.DataFrame(res["comparison_rows"])
            st.dataframe(df, use_container_width=True, height=280)

# -----------------------------------------------------------------------------
# PAGE 3: RESULTS & ANALYTICS
# -----------------------------------------------------------------------------
elif menu == "📊 Results & Analytics":
    st.title("📊 Analytical Charts & Export Center")

    res = st.session_state.last_results
    if res is None:
        st.warning("⚠️ No comparison data available yet. Please navigate to '🧬 Sequence Comparison' and click 'Compare Sequences' first!")
    else:
        st.markdown(f"Displaying graphical analysis for **{res['seq1_name']}** vs **{res['seq2_name']}**.")

        # Matplotlib Charts Row
        col_chart1, col_chart2 = st.columns([1, 1])

        with col_chart1:
            st.markdown("#### 1. Positional Composition")
            fig_bar = plot_comparison_barchart(res)
            st.pyplot(fig_bar, use_container_width=True)

        with col_chart2:
            st.markdown("#### 2. Similarity Percentage")
            fig_donut = plot_similarity_donut(res)
            st.pyplot(fig_donut, use_container_width=True)

        # Sequence Track
        st.markdown("#### 3. Positional Distribution Track")
        fig_track = plot_position_track(res["comparison_rows"])
        st.pyplot(fig_track, use_container_width=True)

        st.markdown("---")
        st.subheader("📥 Export & Download Results")
        col_d1, col_d2, col_d3 = st.columns(3)

        # CSV Download
        with col_d1:
            df = pd.DataFrame(res["comparison_rows"])
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📄 Download Results (CSV)",
                data=csv_data,
                file_name="dna_similarity_positions.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.caption("Position, Sequence 1, Sequence 2, Status, and Symbol.")

        # Text Report Download
        with col_d2:
            text_rep = generate_text_report(res, name1=res["seq1_name"], name2=res["seq2_name"])
            st.download_button(
                label="📝 Download Summary (.TXT)",
                data=text_rep.encode("utf-8"),
                file_name="dna_similarity_report.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.caption("Formatted analysis report with alignment chunks.")

        # DOCX Project Report Download
        with col_d3:
            docx_path = os.path.join(os.path.dirname(__file__), "DNA_Sequence_Similarity_Checker_Project_Report.docx")
            if not os.path.exists(docx_path):
                docx_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "DNA_Sequence_Similarity_Checker_Project_Report.docx")

            if os.path.exists(docx_path):
                with open(docx_path, "rb") as f:
                    docx_bytes = f.read()
                st.download_button(
                    label="📘 Project Report (.DOCX)",
                    data=docx_bytes,
                    file_name="DNA_Sequence_Similarity_Checker_Project_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                st.caption("Full editable project documentation in Word (.docx).")
            else:
                st.button("📘 DOCX Report (Not Found)", disabled=True, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 4: ABOUT THE PROJECT
# -----------------------------------------------------------------------------
elif menu == "ℹ️ About the Project":
    st.title("ℹ️ About DNA Sequence Similarity Checker")

    st.markdown("""
    ### 🎯 Project Overview
    The **DNA Sequence Similarity Checker** is a beginner-friendly bioinformatics web application built to introduce college students
    and aspiring bioinformaticians to biological sequence comparison, data validation, and computational analytics using Python.

    ### 🛠️ Technology Stack
    - **Python 3**: Core programming language.
    - **Streamlit**: Modern interactive web framework for data science and bioinformatics.
    - **Biopython**: Industry-standard bioinformatics library for reading FASTA records (`Bio.SeqIO`) and sequence handling (`Bio.Seq`).
    - **Matplotlib**: Generation of scientific charts (bar charts, donut charts, and positional tracks).
    - **Pandas**: Structured tabular representation and CSV data generation.

    ### 📐 Algorithmic Design
    This application utilizes a **position-by-position comparison** model:
    - It aligns sequences directly at index 0 without inserting internal indels to optimize matches.
    - If Sequence 1 and Sequence 2 have different lengths, the shorter sequence is padded with gap characters (`-`) at the end.
    - Similarity percentage is calculated as:
    """)

    st.latex(r"\text{Similarity} = \frac{\text{Matches}}{\max(\text{Length}_1, \text{Length}_2)} \times 100")

    st.markdown("""
    ### 🔬 Positional Comparison vs. Full Alignment
    It is vital for students to understand the distinction between this simple positional method and real-world biological sequence alignment:
    | Feature | Positional Comparison (This App) | Global Alignment (Needleman-Wunsch) | Local Alignment (Smith-Waterman / BLAST) |
    | :--- | :--- | :--- | :--- |
    | **Approach** | Strict 1-to-1 index matching | Dynamic programming with gap penalties | Identifies high-scoring local matches |
    | **Frameshift tolerance** | None (a 1 nt shift ruins alignment) | High (inserts optimal gaps) | High (finds matching conserved motifs) |
    | **Ideal Use Case** | Point mutation checks, SNP analysis | Full homologous gene alignment | Database searching and remote homology |
    | **Complexity** | $O(N)$ linear time | $O(N \times M)$ quadratic time | $O(N \times M)$ or heuristic $O(N)$ |

    ### 👥 Project Information
    - **Project Name**: DNA Sequence Similarity Checker
    - **Target Audience**: College-level beginner bioinformatics students & researchers.
    - **License**: Educational Open Source.
    """)
