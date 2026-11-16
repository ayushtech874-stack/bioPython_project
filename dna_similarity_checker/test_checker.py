"""
test_checker.py
===============
Comprehensive unit test suite for DNA Sequence Similarity Checker.
Verifies all algorithmic requirements, edge cases, FASTA parsing, and visualizations.
"""

import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sequence_utils import (
    clean_sequence,
    validate_dna_sequence,
    parse_fasta,
    calculate_positional_similarity,
    calculate_gc_content,
    generate_text_report
)
from visualization import (
    plot_comparison_barchart,
    plot_similarity_donut,
    plot_position_track,
    render_html_sequence_alignment
)


def test_prompt_benchmark_case():
    print("[RUNNING] Test 1: Prompt Benchmark Case (12 nt, 1 mismatch)")
    s1 = "ATGCGTACGTAG"
    s2 = "ATGCGTTCGTAG"
    
    clean1 = clean_sequence(s1)
    clean2 = clean_sequence(s2)
    
    val1, err1 = validate_dna_sequence(clean1)
    val2, err2 = validate_dna_sequence(clean2)
    assert val1 and val2, "Sequences should be valid"
    
    res = calculate_positional_similarity(clean1, clean2)
    assert res["len1"] == 12, f"Expected len1 12, got {res['len1']}"
    assert res["len2"] == 12, f"Expected len2 12, got {res['len2']}"
    assert res["matches"] == 11, f"Expected 11 matches, got {res['matches']}"
    assert res["mismatches"] == 1, f"Expected 1 mismatch, got {res['mismatches']}"
    assert res["gaps"] == 0, f"Expected 0 gaps, got {res['gaps']}"
    assert res["similarity_percentage"] == 91.67, f"Expected 91.67%, got {res['similarity_percentage']}"
    assert "Very High" in res["interpretation_label"]
    print("  -> Passed: 11 matches, 1 mismatch, 91.67% similarity.")


def test_unequal_length():
    print("[RUNNING] Test 2: Unequal Sequence Lengths (Gaps counted as non-matches)")
    s1 = "ATGCGTAGCTAGCTAGCTA"  # 19 nt
    s2 = "ATGCGTAGCTAG"         # 12 nt
    
    res = calculate_positional_similarity(s1, s2)
    assert res["len1"] == 19
    assert res["len2"] == 12
    assert res["max_len"] == 19
    assert res["matches"] == 12
    assert res["gaps"] == 7
    assert res["mismatches"] == 0
    # 12 / 19 * 100 = 63.16%
    assert res["similarity_percentage"] == 63.16
    print("  -> Passed: 12 matches, 7 gaps, 63.16% similarity.")


def test_case_and_whitespace_cleaning():
    print("[RUNNING] Test 3: Lowercase and Whitespace Cleaning")
    raw = "  atg cgt\n acg\t tag \r"
    cleaned = clean_sequence(raw)
    assert cleaned == "ATGCGTACGTAG", f"Unexpected cleaned string: {cleaned}"
    print("  -> Passed: Correctly uppercased and stripped whitespace.")


def test_invalid_characters():
    print("[RUNNING] Test 4: Invalid Characters Detection")
    val, errs = validate_dna_sequence("ATGCXYZ123")
    assert not val, "Expected validation failure for invalid chars"
    assert len(errs) > 0
    print("  -> Passed: Caught invalid chars correctly.")


def test_empty_sequence():
    print("[RUNNING] Test 5: Empty Sequence Validation")
    val, errs = validate_dna_sequence("")
    assert not val
    assert "empty" in errs[0].lower()
    print("  -> Passed: Caught empty sequence correctly.")


def test_fasta_parsing():
    print("[RUNNING] Test 6: Biopython FASTA Parsing")
    fasta_str = ">TestGene Description of gene\nATGCTAGCTA\n"
    success, seq_id, seq, err = parse_fasta(fasta_str)
    assert success, f"FASTA parsing failed: {err}"
    assert seq_id == "TestGene"
    assert seq == "ATGCTAGCTA"
    print("  -> Passed: Biopython successfully parsed FASTA record.")


def test_visualizations():
    print("[RUNNING] Test 7: Matplotlib Chart and HTML Generation")
    res = calculate_positional_similarity("ATGCGTACGTAG", "ATGCGTTCGTAG")
    fig1 = plot_comparison_barchart(res)
    fig2 = plot_similarity_donut(res)
    fig3 = plot_position_track(res["comparison_rows"])
    html = render_html_sequence_alignment(res["aligned_seq1"], res["aligned_seq2"], res["comparison_rows"])
    
    assert fig1 is not None
    assert fig2 is not None
    assert fig3 is not None
    assert "dna-align-container" in html
    assert "cell-match" in html
    assert "cell-mismatch" in html
    print("  -> Passed: All figures and HTML generated without error.")


def test_text_report():
    print("[RUNNING] Test 8: Plain-Text Report Generation")
    res = calculate_positional_similarity("ATGCGTACGTAG", "ATGCGTTCGTAG")
    rep = generate_text_report(res, "SeqA", "SeqB")
    assert "DNA SEQUENCE SIMILARITY CHECKER" in rep
    assert "91.67%" in rep
    assert "SeqA" in rep
    print("  -> Passed: Text report generated successfully.")


if __name__ == "__main__":
    print("=" * 60)
    print("Starting DNA Sequence Similarity Checker Test Suite")
    print("=" * 60)
    test_prompt_benchmark_case()
    test_unequal_length()
    test_case_and_whitespace_cleaning()
    test_invalid_characters()
    test_empty_sequence()
    test_fasta_parsing()
    test_visualizations()
    test_text_report()
    print("=" * 60)
    print("ALL 8 TESTS PASSED SUCCESSFULLY! ✅")
    print("=" * 60)
