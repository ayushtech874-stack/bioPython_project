"""
app.py
======
Main Streamlit application for the DNA Sequence Similarity Checker.

Optimizations:
- High-contrast, theme-adaptive scientific UI (crystal-clear in both dark & light modes).
- Form-based input submission to completely eliminate typing latency and WebSocket lag.
- Caching for computational similarity and analytical chart generation.
- Real-time DNA validation with Biopython FASTA parsing.
- Color-coded visual sequence alignment matrix and multi-format reporting.
- Architectural insights explaining "Why Streamlit" and performance trade-offs.
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
# High-Contrast Scientific Dashboard Styling (Theme-Adaptive)
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Explicit high-contrast headings */
h1, h2, h3, h4 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px;
}

p, span, label, div {
    color: #E2E8F0;
}

/* Modern Metric Cards */
.metric-card {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    transition: transform 0.15s ease, border-color 0.15s ease;
}
.metric-card:hover {
    border-color: #0D9488;
    transform: translateY(-2px);
}
.metric-title {
    font-size: 11px;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}
.metric-val {
    font-size: 26px;
    font-weight: 800;
    color: #F8FAFC;
    line-height: 1.1;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.metric-sub {
    font-size: 11.5px;
    color: #2DD4BF;
    font-weight: 600;
    margin-top: 4px;
}

/* Hero Section */
.hero-box {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}
.hero-title {
    font-size: 30px;
    font-weight: 800;
    color: #FFFFFF !important;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 15px;
    color: #CBD5E1;
    line-height: 1.6;
    max-width: 950px;
}

/* Custom Alert / Banner */
.status-banner {
    border-radius: 12px;
    padding: 16px 20px;
    margin: 16px 0;
    border-left: 5px solid;
    background-color: #1E293B;
}

/* Disclaimer & Guide Box */
.info-note {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13.5px;
    color: #CBD5E1;
    margin: 14px 0;
    line-height: 1.55;
}

/* Quick buttons styling */
div.stButton > button:first-child {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.15s ease;
}

/* Form container enhancement */
[data-testid="stForm"] {
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
    background-color: rgba(30, 41, 59, 0.4) !important;
    padding: 24px !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Caching Functions for High Performance (Zero Latency)
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_cached_similarity(seq1: str, seq2: str):
    return calculate_positional_similarity(seq1, seq2)

@st.cache_data(show_spinner=False)
def get_cached_barchart(stats: dict):
    return plot_comparison_barchart(stats)

@st.cache_data(show_spinner=False)
def get_cached_donut(stats: dict):
    return plot_similarity_donut(stats)

@st.cache_data(show_spinner=False)
def get_cached_track(comparison_rows: list):
    return plot_position_track(comparison_rows)

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

# Pre-calculate default comparison if not yet set
if st.session_state.last_results is None:
    c1 = clean_sequence(st.session_state.seq1_input)
    c2 = clean_sequence(st.session_state.seq2_input)
    init_res = get_cached_similarity(c1, c2)
    init_res["seq1_name"] = st.session_state.seq1_name
    init_res["seq2_name"] = st.session_state.seq2_name
    st.session_state.last_results = init_res

# -----------------------------------------------------------------------------
# Helper Sample Loaders
# -----------------------------------------------------------------------------
def load_sample_prompt_test():
    st.session_state.seq1_input = "ATGCGTACGTAG"
    st.session_state.seq2_input = "ATGCGTTCGTAG"
    st.session_state.seq1_name = "Benchmark_Ref"
    st.session_state.seq2_name = "Benchmark_Var"
    st.session_state.last_results = None

def load_sample_unequal():
    st.session_state.seq1_input = "ATGCGTAGCTAGCTAGCTA"
    st.session_state.seq2_input = "ATGCGTAGCTAG"
    st.session_state.seq1_name = "Full_Gene_19nt"
    st.session_state.seq2_name = "Truncated_12nt"
    st.session_state.last_results = None

def load_sample_sickle_cell():
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
    st.markdown("### 🧬 BioPython Toolkit")
    menu = st.radio(
        "Navigation Menu:",
        ["🏠 Dashboard Home", "🧬 Sequence Comparison", "📊 Results & Analytics", "🏛️ System Architecture", "ℹ️ About & Why Streamlit?"],
        index=1
    )

    st.markdown("---")
    st.markdown("### ⚙️ Engine Settings")
    allow_n = st.checkbox("Allow 'N' (Ambiguous nucleotide)", value=True,
                          help="Permits 'N' representing an unknown nucleotide base.")

    st.markdown("---")
    st.markdown("### 🧪 Quick Biological Presets")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("Benchmark Pair", on_click=load_sample_prompt_test, use_container_width=True,
                     help="12 nt benchmark with 1 mismatch (91.67%)"):
            pass
    with col_p2:
        if st.button("Unequal Length", on_click=load_sample_unequal, use_container_width=True,
                     help="19 nt vs 12 nt with gap calculation"):
            pass
    if st.button("Sickle Cell Point Mutation", on_click=load_sample_sickle_cell, use_container_width=True,
                 help="Human Beta-Globin (Codon 6 A->T mutation)"):
        pass

    st.markdown("---")
    if st.button("🗑️ Clear Sequence Inputs", on_click=clear_all_inputs, use_container_width=True):
        st.toast("Inputs cleared!", icon="🧹")

    st.markdown("---")
    st.caption("DNA Sequence Similarity Checker v2.0\nHigh-Performance BioPython Suite")

# -----------------------------------------------------------------------------
# PAGE 1: DASHBOARD HOME
# -----------------------------------------------------------------------------
if menu == "🏠 Dashboard Home":
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">🧬 DNA Sequence Similarity Checker</div>
        <div class="hero-sub">
            A high-performance, beginner-friendly bioinformatics engine built with Python and BioPython.
            Perform instant positional nucleotide identity analysis, inspect color-coded single nucleotide variants (SNVs),
            and generate publication-grade analytical reports.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 🔬 How The Algorithm Works")
        st.markdown("""
        Comparing DNA sequences is a fundamental task in genomics, phylogenetics, and molecular medicine.
        This application executes a **deterministic positional alignment model**:

        1. **Input Normalization**: Ingests raw text or standard FASTA records (`>Header\\nSequence`). Automatically normalizes sequences to uppercase and strips all whitespace/newlines.
        2. **Validation Safeguard**: Validates characters against standard IUPAC nucleotide sets (**A, T, G, C**, and optionally **N**).
        3. **Positional Comparison**:
           - **Match (`|`)**: Nucleotides are identical at index $i$.
           - **Mismatch (`•`)**: Nucleotides differ at index $i$ (representing single nucleotide polymorphisms/mutations).
           - **Gap (`—`)**: For unequal length sequences, shorter strands are padded with terminal gaps and counted as non-matches.
        4. **Similarity Metric**:
        """)

        st.latex(r"\text{Similarity (\%)} = \left( \frac{\text{Matching Positions}}{\max(\text{Length}_1, \text{Length}_2)} \right) \times 100")

    with col2:
        st.markdown("### ⚡ Performance & Key Capabilities")
        st.markdown("""
        - 🚀 **Zero-Lag Form Batching**: Typing is batched locally to avoid server-side re-renders.
        - 🛡️ **Robust Error Catching**: Catches invalid characters with detailed diagnostic error messages.
        - 🧬 **Biopython FASTA Ingestion**: Native biological sequence parsing using `Bio.SeqIO`.
        - 🎨 **Visual Matrix Grid**: Color-coded nucleotide alignment matrix.
        - 📈 **Publication Graphics**: Instant bar charts, donut plots, and positional tracks.
        - 📑 **Multi-Format Exports**: One-click download of CSV logs, formatted text summaries, and DOCX reports.
        """)

        st.info("👉 Ready to analyze? Switch to **🧬 Sequence Comparison** in the sidebar!")

# -----------------------------------------------------------------------------
# PAGE 2: SEQUENCE COMPARISON (ZERO-LAG FORM)
# -----------------------------------------------------------------------------
elif menu == "🧬 Sequence Comparison":
    st.title("🧬 DNA Sequence Comparison")
    st.markdown("Enter or upload two DNA sequences below. Click **Run Sequence Comparison** to execute the analysis.")

    # Using st.form isolates user typing from Streamlit reruns, eliminating lag completely
    with st.form(key="dna_comparison_form"):
        col_in1, col_in2 = st.columns(2)

        with col_in1:
            st.subheader("Sequence 1 (Reference)")
            seq1_name_val = st.text_input("Sequence 1 Identifier:", value=st.session_state.seq1_name)
            seq1_raw_val = st.text_area(
                "Enter DNA Sequence 1:",
                value=st.session_state.seq1_input,
                height=130,
                placeholder="e.g. ATGCGTACGTAG",
                help="Enter DNA string or FASTA formatted text"
            )

        with col_in2:
            st.subheader("Sequence 2 (Query / Variant)")
            seq2_name_val = st.text_input("Sequence 2 Identifier:", value=st.session_state.seq2_name)
            seq2_raw_val = st.text_area(
                "Enter DNA Sequence 2:",
                value=st.session_state.seq2_input,
                height=130,
                placeholder="e.g. ATGCGTTCGTAG",
                help="Enter DNA string or FASTA formatted text"
            )

        submit_btn = st.form_submit_button("🚀 Run Sequence Comparison", type="primary", use_container_width=True)

    # File uploader outside form for immediate file ingestion
    with st.expander("📁 Optional: Upload FASTA Files Instead"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f1 = st.file_uploader("Upload FASTA 1:", type=["fasta", "fa", "fna", "txt"], key="up_f1")
            if f1 is not None:
                succ1, id1, s1, err1 = parse_fasta(f1)
                if succ1:
                    st.session_state.seq1_input = s1
                    st.session_state.seq1_name = id1
                    st.success(f"Loaded: `{id1}` ({len(s1)} nt)")
                else:
                    st.error(err1)
        with col_f2:
            f2 = st.file_uploader("Upload FASTA 2:", type=["fasta", "fa", "fna", "txt"], key="up_f2")
            if f2 is not None:
                succ2, id2, s2, err2 = parse_fasta(f2)
                if succ2:
                    st.session_state.seq2_input = s2
                    st.session_state.seq2_name = id2
                    st.success(f"Loaded: `{id2}` ({len(s2)} nt)")
                else:
                    st.error(err2)

    # Process comparison on submit
    if submit_btn:
        st.session_state.seq1_name = seq1_name_val
        st.session_state.seq2_name = seq2_name_val

        # Support FASTA format pasted inside the text area
        if seq1_raw_val.strip().startswith(">"):
            _, parsed_id1, s1_clean, _ = parse_fasta(seq1_raw_val)
            if parsed_id1:
                st.session_state.seq1_name = parsed_id1
            cleaned1 = s1_clean
        else:
            cleaned1 = clean_sequence(seq1_raw_val)

        if seq2_raw_val.strip().startswith(">"):
            _, parsed_id2, s2_clean, _ = parse_fasta(seq2_raw_val)
            if parsed_id2:
                st.session_state.seq2_name = parsed_id2
            cleaned2 = s2_clean
        else:
            cleaned2 = clean_sequence(seq2_raw_val)

        # Validation
        valid1, errors1 = validate_dna_sequence(cleaned1, allow_n=allow_n)
        valid2, errors2 = validate_dna_sequence(cleaned2, allow_n=allow_n)

        if not valid1:
            st.error(f"❌ **Sequence 1 Error:** {errors1[0]}")
            st.session_state.last_results = None
        elif not valid2:
            st.error(f"❌ **Sequence 2 Error:** {errors2[0]}")
            st.session_state.last_results = None
        else:
            results = get_cached_similarity(cleaned1, cleaned2)
            results["seq1_name"] = st.session_state.seq1_name or "Sequence 1"
            results["seq2_name"] = st.session_state.seq2_name or "Sequence 2"
            st.session_state.last_results = results
            st.session_state.seq1_input = cleaned1
            st.session_state.seq2_input = cleaned2
            st.toast("Comparison calculated successfully!", icon="✅")

    # Render results
    res = st.session_state.last_results
    if res is not None:
        st.markdown("---")
        st.markdown("## 📊 Comparison Metrics")

        m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)

        with m_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Seq 1 Length</div>
                <div class="metric-val">{res['len1']} <span style="font-size:13px;color:#94A3B8;">nt</span></div>
                <div class="metric-sub">GC: {res['gc_content1']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Seq 2 Length</div>
                <div class="metric-val">{res['len2']} <span style="font-size:13px;color:#94A3B8;">nt</span></div>
                <div class="metric-sub">GC: {res['gc_content2']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Matching</div>
                <div class="metric-val" style="color:#10B981;">{res['matches']}</div>
                <div class="metric-sub" style="color:#10B981;">{res['match_percentage']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Mismatches</div>
                <div class="metric-val" style="color:#EF4444;">{res['mismatches']}</div>
                <div class="metric-sub" style="color:#EF4444;">{res['mismatch_percentage']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Gaps</div>
                <div class="metric-val" style="color:#94A3B8;">{res['gaps']}</div>
                <div class="metric-sub" style="color:#94A3B8;">{res['gap_percentage']}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col6:
            st.markdown(f"""
            <div class="metric-card" style="border-color:{res['interpretation_color']};">
                <div class="metric-title">Similarity</div>
                <div class="metric-val" style="color:{res['interpretation_color']};">{res['similarity_percentage']}%</div>
                <div class="metric-sub" style="color:{res['interpretation_color']};">Positional</div>
            </div>
            """, unsafe_allow_html=True)

        # Interpretation Banner
        st.markdown(f"""
        <div class="status-banner" style="border-color: {res['interpretation_color']};">
            <h4 style="margin: 0; color: {res['interpretation_color']};">
                🎯 Interpretation: {res['interpretation_label']} ({res['similarity_percentage']}%)
            </h4>
            <p style="margin: 6px 0 0 0; color: #CBD5E1; font-size: 14px;">
                {res['interpretation_desc']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Visual Alignment Section
        st.markdown("### 🎨 Visual Sequence Alignment Matrix")
        chunk_opt = st.select_slider(
            "Display chunk size (bases per line):",
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
        st.components.v1.html(align_html, height=min(600, max(260, (res['max_len'] // chunk_opt + 1) * 175)), scrolling=True)

        # Position Inspection Table
        with st.expander("🔍 Inspect Full Positional Table"):
            df = pd.DataFrame(res["comparison_rows"])
            st.dataframe(df, use_container_width=True, height=280)

# -----------------------------------------------------------------------------
# PAGE 3: RESULTS & ANALYTICS
# -----------------------------------------------------------------------------
elif menu == "📊 Results & Analytics":
    st.title("📊 Analytical Charts & Export Center")

    res = st.session_state.last_results
    if res is None:
        st.warning("⚠️ No comparison data available yet. Please open '🧬 Sequence Comparison' and click 'Run Sequence Comparison' first!")
    else:
        st.markdown(f"Displaying graphical distribution for **{res['seq1_name']}** vs **{res['seq2_name']}**.")

        col_chart1, col_chart2 = st.columns([1, 1])

        with col_chart1:
            st.markdown("#### 1. Positional Composition Breakdown")
            fig_bar = get_cached_barchart(res)
            st.pyplot(fig_bar, use_container_width=True)

        with col_chart2:
            st.markdown("#### 2. Similarity vs. Difference Ratio")
            fig_donut = get_cached_donut(res)
            st.pyplot(fig_donut, use_container_width=True)

        st.markdown("#### 3. Positional Distribution Track Across Sequence")
        fig_track = get_cached_track(res["comparison_rows"])
        st.pyplot(fig_track, use_container_width=True)

        st.markdown("---")
        st.subheader("📥 Export & Download Reports")
        col_d1, col_d2, col_d3 = st.columns(3)

        with col_d1:
            df = pd.DataFrame(res["comparison_rows"])
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📄 Download CSV Data",
                data=csv_data,
                file_name="dna_similarity_positions.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.caption("Complete table with position, bases, status, and symbols.")

        with col_d2:
            text_rep = generate_text_report(res, name1=res["seq1_name"], name2=res["seq2_name"])
            st.download_button(
                label="📝 Download Text Summary",
                data=text_rep.encode("utf-8"),
                file_name="dna_similarity_report.txt",
                mime="text/plain",
                use_container_width=True
            )
            st.caption("Human-readable bioinformatics summary report.")

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
                st.caption("Academic Word report document.")
            else:
                st.button("📘 DOCX Report (Not Found)", disabled=True, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 4: SYSTEM ARCHITECTURE
# -----------------------------------------------------------------------------
elif menu == "🏛️ System Architecture":
    st.title("🏛️ System Architecture & Code Design")
    st.markdown("Comprehensive overview of the application's multi-layered architecture, data pipeline, and modular code hierarchy.")

    st.markdown("""
    ### 1. High-Level Multi-Tier Architecture
    The application follows an asynchronous, decoupled 5-tier architecture designed for low-latency bioinformatics analysis:
    """)

    st.markdown("""
    ```mermaid
    flowchart TD
        subgraph Client ["Client Presentation Tier (Browser)"]
            UI["Streamlit Web UI"]
            AlignGrid["HTML5 Alignment Matrix"]
            Charts["Matplotlib Visualizers"]
        end

        subgraph Controller ["State & Controller Tier"]
            Form["Form Input Batcher (st.form)"]
            Session["Session State Store"]
            Cache["@st.cache_data Memoization"]
        end

        subgraph Ingestion ["Data Ingestion & Normalization Tier"]
            InputRouter["Input Router (Text / FASTA)"]
            BioSeqIO["Biopython Bio.SeqIO Engine"]
            RegexClean["Regex Whitespace Normalizer"]
            Validator["IUPAC DNA Validator"]
        end

        subgraph Domain ["Core Bioinformatics Engine"]
            AlignEngine["Positional Comparison Engine"]
            GCHelper["GC-Content Calculator"]
            InterpEngine["Similarity Classifier"]
        end

        subgraph Export ["Export & Persistence Tier"]
            CSVExp["CSV Table Streamer"]
            TxtExp["Plain-Text Report Builder"]
            DocxExp["Word (.docx) Report Builder"]
        end

        UI --> Form
        Form --> InputRouter
        InputRouter -->|FASTA| BioSeqIO
        InputRouter -->|Raw Text| RegexClean
        BioSeqIO --> RegexClean
        RegexClean --> Validator
        Validator -->|Valid| AlignEngine
        AlignEngine --> GCHelper
        AlignEngine --> InterpEngine
        Domain --> Cache
        Cache --> Session
        Session --> UI
        Session --> AlignGrid
        Session --> Charts
        Session --> Export
    ```
    """)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("#### 🧩 Code Architecture & Module Separation")
        st.markdown("""
        - **`run_app.py`**: Root entry-point launcher that verifies environment and starts the server.
        - **`app.py`**: Presentation layer, session state management, and user interaction controller.
        - **`sequence_utils.py`**: Domain logic containing pure functions for sequence cleaning, validation, Biopython parsing, and positional similarity math.
        - **`visualization.py`**: Rendering engine generating dark-theme Matplotlib figures and HTML alignment grids.
        - **`test_checker.py`**: Automated unit testing suite covering 8 critical edge cases and benchmarks.
        """)

    with col_a2:
        st.markdown("#### ⚡ Performance Optimizations Implemented")
        st.markdown("""
        1. **Form Batching (`st.form`)**: Isolates user typing so that characters are not sent over WebSockets on every keypress.
        2. **Memoization (`@st.cache_data`)**: Caches sequence alignment computations and Matplotlib figure creation in memory.
        3. **Font Lookup Optimization**: Explicitly targets pre-cached sans-serif fonts to eliminate Windows font scanner delays.
        4. **Theme-Adaptive CSS**: Crystal-clear typography and high-contrast card styling in both dark and light modes.
        """)

# -----------------------------------------------------------------------------
# PAGE 5: ABOUT & WHY STREAMLIT?
# -----------------------------------------------------------------------------
elif menu == "ℹ️ About & Why Streamlit?":
    st.title("ℹ️ Technical Evaluation: Why Streamlit?")

    st.markdown("""
    ### ❓ Why Are We Using Streamlit for This Project?
    A common question in bioinformatics tool design is: **Why use Streamlit instead of React, Flask, or pure JavaScript?**

    Here is a candid architectural breakdown of why Streamlit was chosen, where it excels, its inherent constraints, and how we optimized it:
    """)

    st.markdown("""
    | Evaluation Dimension | Streamlit (Our Choice) | Flask / FastAPI + React | Client-Side Vanilla JS / WASM |
    | :--- | :--- | :--- | :--- |
    | **Language Ecosystem** | Pure Python 3 | Python (Backend) + JavaScript/TypeScript (Frontend) | Pure JavaScript / WebAssembly |
    | **Biopython Integration** | **Native & Direct** (`Bio.SeqIO` runs in same process) | Requires building REST API endpoints & JSON serialization | Difficult (Requires Pyodide or JS reimplementation) |
    | **Development Velocity** | ⚡ Extremely Fast (1-2 files) | Slower (2 separate codebases, API contracts, build tools) | Moderate |
    | **Execution Model** | Server-side reactive script execution | Client-side reactive DOM with asynchronous REST calls | Pure client-side browser execution |
    | **Why It Can Feel Laggy** | By default, every widget interaction reruns the entire Python script over WebSockets | Network latency on API round trips | CPU bottleneck on heavy client processing |
    | **Best Suited For** | **Bioinformatics research, academic demos, data science dashboards** | Commercial SaaS, multi-tenant enterprise software | Offline tools, high-framerate client apps |
    """)

    st.markdown("""
    ### 🛠️ Why Was Localhost Initially Laggy & How Did We Fix It?
    1. **The Script-Rerun Paradigm**:
       - *The Issue*: Without isolation, Streamlit re-executes the Python file from line 1 on every single keystroke in a `st.text_area`.
       - *The Solution*: We wrapped the input fields in a **`st.form`**. Now, inputs stay strictly in the browser until the user explicitly hits **"Run Sequence Comparison"**, eliminating typing lag entirely.
    2. **Matplotlib Font Discovery Latency**:
       - *The Issue*: On Windows, requesting non-standard font weights (`semibold`, `medium`) forced Matplotlib to scan the entire `C:\\Windows\\Fonts` directory on each render.
       - *The Solution*: Standardized to pre-registered fonts (`sans-serif`, `bold`, `normal`) and memoized figures using **`@st.cache_data`**.
    3. **UI Invisibility in Dark Mode**:
       - *The Issue*: Hardcoded dark text colors (`#0F172A`) collided with Streamlit's dark background (`#0E1117`), making headings invisible.
       - *The Solution*: Rebuilt the design system with adaptive CSS, high-contrast text (`#F8FAFC`), and modern slate cards (`#1E293B`).
    """)
