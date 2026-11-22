"""
visualization.py
================
Matplotlib chart generation and HTML color-coded sequence alignment
visualizations for the DNA Sequence Similarity Checker.

Styled for a clean, modern, high-contrast publication-ready scientific aesthetic.
Compatible with dark and light themes, optimized to eliminate font scanning latency.
"""

import os
import tempfile
from typing import Dict, Any, List

# Ensure a safe, writable matplotlib configuration directory
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "matplotlib"))

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend safe for Streamlit
import matplotlib.pyplot as plt
import numpy as np

# Configure matplotlib font preferences globally to eliminate font scanner delays
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']

# High-contrast scientific palette
COLOR_MATCH = "#10B981"       # Emerald Green
COLOR_MISMATCH = "#EF4444"    # Crimson Red
COLOR_GAP = "#94A3B8"         # Slate Grey
COLOR_TEAL = "#0D9488"        # Vibrant Teal
COLOR_BG = "#1E293B"          # Dark Slate Card
COLOR_TEXT = "#F8FAFC"        # Bright White/Slate
COLOR_MUTED = "#94A3B8"       # Secondary text
COLOR_GRID = "#334155"        # Slate Grid


def plot_comparison_barchart(stats: Dict[str, Any]) -> plt.Figure:
    """
    Generate a clean, modern bar chart comparing Matching, Mismatching,
    and Gap positions with counts and percentage labels.
    """
    categories = ["Matching", "Mismatching", "Gaps"]
    counts = [stats["matches"], stats["mismatches"], stats["gaps"]]
    percentages = [
        stats["match_percentage"],
        stats["mismatch_percentage"],
        stats["gap_percentage"]
    ]
    colors = [COLOR_MATCH, COLOR_MISMATCH, COLOR_GAP]

    fig, ax = plt.subplots(figsize=(6.5, 3.8), dpi=130)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)

    bars = ax.bar(categories, counts, color=colors, width=0.52, edgecolor="none", zorder=3)

    # Style axes and spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_GRID)
    ax.spines["bottom"].set_color(COLOR_GRID)
    ax.spines["bottom"].set_linewidth(1.2)

    ax.yaxis.grid(True, linestyle="--", alpha=0.5, color=COLOR_GRID, zorder=0)
    ax.set_axisbelow(True)

    # Annotate bars with counts and percentages
    max_val = max(counts) if max(counts) > 0 else 1
    y_limit = max_val * 1.25
    ax.set_ylim(0, y_limit)

    for bar, count, pct in zip(bars, counts, percentages):
        height = bar.get_height()
        ax.annotate(
            f"{count} nt\n({pct:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color=COLOR_TEXT
        )

    ax.set_ylabel("Number of Positions", fontsize=10, fontweight="bold", color=COLOR_TEXT, labelpad=8)
    ax.set_title("Positional Breakdown (Matches vs. Mismatches vs. Gaps)",
                 fontsize=11.5, fontweight="bold", color=COLOR_TEXT, pad=12)
    ax.tick_params(axis="x", colors=COLOR_TEXT, labelsize=10)
    ax.tick_params(axis="y", colors=COLOR_MUTED, labelsize=9)

    plt.tight_layout()
    return fig


def plot_similarity_donut(stats: Dict[str, Any]) -> plt.Figure:
    """
    Generate an elegant scientific donut chart displaying the similarity percentage
    with an embedded central metric label.
    """
    sim_pct = stats["similarity_percentage"]
    diff_pct = round(100.0 - sim_pct, 2)

    labels = [f"Similarity ({sim_pct}%)", f"Difference ({diff_pct}%)"]
    sizes = [sim_pct, diff_pct]
    colors = [stats.get("interpretation_color", COLOR_TEAL), "#334155"]

    # If 100% or 0%, adjust to prevent matplotlib warning
    if sim_pct == 100.0:
        sizes = [100.0]
        labels = [f"Similarity (100%)"]
        colors = [COLOR_MATCH]
    elif sim_pct == 0.0:
        sizes = [100.0]
        labels = [f"Difference (100%)"]
        colors = [COLOR_MISMATCH]

    fig, ax = plt.subplots(figsize=(5.2, 3.8), dpi=130)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)

    wedges, _ = ax.pie(
        sizes,
        labels=None,
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.28, edgecolor=COLOR_BG, linewidth=2.5)
    )

    # Central metric text
    ax.text(0, 0.08, f"{sim_pct:.1f}%", ha="center", va="center",
            fontsize=20, fontweight="bold", color=COLOR_TEXT)
    ax.text(0, -0.15, "Positional\nSimilarity", ha="center", va="center",
            fontsize=9.5, fontweight="normal", color=COLOR_MUTED)

    ax.legend(
        wedges, labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=2,
        frameon=False,
        fontsize=9,
        labelcolor=COLOR_TEXT
    )

    ax.set_title("Overall Positional Identity",
                 fontsize=11.5, fontweight="bold", color=COLOR_TEXT, pad=10)

    plt.tight_layout()
    return fig


def plot_position_track(comparison_rows: List[Dict[str, Any]]) -> plt.Figure:
    """
    Generate a linear sequence track diagram showing match and mismatch distribution
    across the entire sequence length.
    """
    total = len(comparison_rows)
    if total == 0:
        fig, ax = plt.subplots(figsize=(8, 1.8), dpi=130)
        fig.patch.set_facecolor(COLOR_BG)
        ax.set_facecolor(COLOR_BG)
        return fig

    # Map statuses to colors
    status_colors = {
        "Match": COLOR_MATCH,
        "Mismatch": COLOR_MISMATCH,
        "Gap": COLOR_GAP
    }
    bar_colors = [status_colors.get(row["Status"], COLOR_GAP) for row in comparison_rows]

    fig, ax = plt.subplots(figsize=(8.5, 1.7), dpi=130)
    fig.patch.set_facecolor(COLOR_BG)
    ax.set_facecolor(COLOR_BG)

    # Plot vertical bars for each position
    x_positions = np.arange(1, total + 1)
    ax.bar(x_positions, 1, color=bar_colors, width=1.0, edgecolor="none")

    ax.set_xlim(0.5, total + 0.5)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(COLOR_GRID)

    ax.set_xlabel("Nucleotide Position (5' → 3')", fontsize=9.5, fontweight="bold", color=COLOR_TEXT, labelpad=6)
    ax.set_title("Sequence Distribution Track", fontsize=11, fontweight="bold", color=COLOR_TEXT, pad=8)
    ax.tick_params(axis="x", colors=COLOR_MUTED, labelsize=8.5)

    plt.tight_layout()
    return fig


def render_html_sequence_alignment(seq1: str, seq2: str, comparison_rows: List[Dict[str, Any]], chunk_size: int = 25) -> str:
    """
    Create an attractive HTML representation of the aligned sequences with
    color-coded nucleotide boxes, position numbers, and alignment symbols.
    
    Colors:
      - Green: Matching nucleotides
      - Red: Mismatching nucleotides
      - Grey: Gaps / missing positions
    """
    if not comparison_rows:
        return "<p style='color: #94A3B8;'>No sequence data to display.</p>"

    html_parts = [
        """
        <style>
        .dna-align-container {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'JetBrains Mono', Consolas, monospace;
            background-color: #0F172A;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 18px 20px;
            margin: 10px 0;
            overflow-x: auto;
            color: #F8FAFC;
        }
        .dna-chunk {
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px dashed #334155;
        }
        .dna-chunk:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        .dna-chunk-header {
            font-size: 11px;
            font-weight: 700;
            color: #38BDF8;
            margin-bottom: 8px;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }
        .dna-grid {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .dna-row {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .dna-label {
            width: 82px;
            font-size: 11px;
            font-weight: 700;
            color: #94A3B8;
            text-align: right;
            padding-right: 10px;
            user-select: none;
            flex-shrink: 0;
        }
        .dna-cell {
            width: 28px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13.5px;
            font-weight: 700;
            border-radius: 6px;
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            flex-shrink: 0;
            transition: transform 0.1s ease;
        }
        .cell-match {
            background-color: rgba(16, 185, 129, 0.22);
            color: #34D399;
            border: 1px solid rgba(52, 211, 153, 0.45);
        }
        .cell-mismatch {
            background-color: rgba(239, 68, 68, 0.22);
            color: #F87171;
            border: 1px solid rgba(248, 113, 113, 0.45);
        }
        .cell-gap {
            background-color: rgba(148, 163, 184, 0.12);
            color: #94A3B8;
            border: 1px solid rgba(148, 163, 184, 0.25);
        }
        .dna-sym {
            font-size: 13px;
            font-weight: 800;
        }
        .sym-match {
            color: #34D399;
        }
        .sym-mismatch {
            color: #F87171;
        }
        .sym-gap {
            color: #64748B;
        }
        .pos-num {
            font-size: 9.5px;
            color: #64748B;
            font-weight: 600;
            background: transparent;
        }
        .dna-legend {
            display: flex;
            gap: 20px;
            margin-top: 14px;
            font-size: 12px;
            font-weight: 600;
            padding-top: 10px;
            border-top: 1px solid #334155;
            color: #CBD5E1;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .legend-badge {
            width: 14px;
            height: 14px;
            border-radius: 4px;
            display: inline-block;
        }
        </style>
        <div class="dna-align-container">
        """
    ]

    total_positions = len(comparison_rows)

    for start in range(0, total_positions, chunk_size):
        end = min(start + chunk_size, total_positions)
        chunk = comparison_rows[start:end]

        html_parts.append(f'<div class="dna-chunk">')
        html_parts.append(f'<div class="dna-chunk-header">Positions {start + 1} — {end}</div>')
        html_parts.append('<div class="dna-grid">')

        # Row 1: Position numbers
        html_parts.append('<div class="dna-row"><div class="dna-label">Position</div>')
        for row in chunk:
            html_parts.append(f'<div class="dna-cell pos-num">{row["Position"]}</div>')
        html_parts.append('</div>')

        # Row 2: Sequence 1 nucleotides
        html_parts.append('<div class="dna-row"><div class="dna-label">Sequence 1</div>')
        for row in chunk:
            c_class = f"cell-{row['Status'].lower()}"
            html_parts.append(f'<div class="dna-cell {c_class}">{row["Sequence 1"]}</div>')
        html_parts.append('</div>')

        # Row 3: Alignment indicator symbols
        html_parts.append('<div class="dna-row"><div class="dna-label">Match</div>')
        for row in chunk:
            sym_char = "|" if row["Status"] == "Match" else ("•" if row["Status"] == "Mismatch" else "—")
            sym_class = f"sym-{row['Status'].lower()}"
            html_parts.append(f'<div class="dna-cell dna-sym {sym_class}">{sym_char}</div>')
        html_parts.append('</div>')

        # Row 4: Sequence 2 nucleotides
        html_parts.append('<div class="dna-row"><div class="dna-label">Sequence 2</div>')
        for row in chunk:
            c_class = f"cell-{row['Status'].lower()}"
            html_parts.append(f'<div class="dna-cell {c_class}">{row["Sequence 2"]}</div>')
        html_parts.append('</div>')

        html_parts.append('</div></div>')  # end dna-grid & dna-chunk

    # Add legend at bottom
    html_parts.append("""
        <div class="dna-legend">
            <div class="legend-item">
                <span class="legend-badge" style="background:rgba(16, 185, 129, 0.22); border:1px solid #34D399;"></span>
                <span style="color:#34D399;">Match (|)</span>
            </div>
            <div class="legend-item">
                <span class="legend-badge" style="background:rgba(239, 68, 68, 0.22); border:1px solid #F87171;"></span>
                <span style="color:#F87171;">Mismatch (•)</span>
            </div>
            <div class="legend-item">
                <span class="legend-badge" style="background:rgba(148, 163, 184, 0.15); border:1px solid #94A3B8;"></span>
                <span style="color:#94A3B8;">Gap (—)</span>
            </div>
        </div>
    </div>
    """)

    return "".join(html_parts)
