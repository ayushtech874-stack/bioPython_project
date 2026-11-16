"""
sequence_utils.py
=================
Bioinformatics utilities for DNA sequence cleaning, validation,
Biopython FASTA parsing, positional similarity calculation,
and report generation.

Designed for college-level beginner bioinformatics projects.
"""

import io
from typing import Tuple, List, Dict, Any
from Bio import SeqIO
from Bio.Seq import Seq


VALID_NUCLEOTIDES = {"A", "T", "G", "C", "N"}


def clean_sequence(raw_sequence: str) -> str:
    """
    Remove all whitespace, newlines, tabs, and convert characters to uppercase.
    
    Parameters:
        raw_sequence (str): Raw string input from user or file.
        
    Returns:
        str: Cleaned, uppercase sequence string.
    """
    if not raw_sequence:
        return ""
    # Filter out whitespace characters and convert to upper case
    return "".join(raw_sequence.split()).upper()


def validate_dna_sequence(sequence: str, allow_n: bool = True) -> Tuple[bool, List[str]]:
    """
    Validate whether a sequence contains only valid DNA nucleotides.
    
    Parameters:
        sequence (str): Cleaned sequence string.
        allow_n (bool): Whether to permit 'N' (unknown nucleotide). Default is True.
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list of human-friendly error messages)
    """
    if not sequence:
        return False, ["Sequence is empty. Please enter at least one nucleotide (A, T, G, C)."]
    
    allowed = VALID_NUCLEOTIDES if allow_n else {"A", "T", "G", "C"}
    invalid_positions = []
    
    for idx, char in enumerate(sequence, start=1):
        if char not in allowed:
            invalid_positions.append((idx, char))
            
    if invalid_positions:
        # Group unique invalid characters
        unique_invalid = sorted(list({char for _, char in invalid_positions}))
        first_few = [f"'{char}' at position {pos}" for pos, char in invalid_positions[:5]]
        more_count = len(invalid_positions) - 5
        
        detail_msg = f"Invalid character(s) detected: {', '.join(unique_invalid)}. Found: " + ", ".join(first_few)
        if more_count > 0:
            detail_msg += f" (and {more_count} more)."
            
        allowed_str = "A, T, G, C, N" if allow_n else "A, T, G, C"
        return False, [
            detail_msg,
            f"DNA sequences must only contain {allowed_str}."
        ]
        
    return True, []


def parse_fasta(file_or_text: Any) -> Tuple[bool, str, str, str]:
    """
    Parse a FASTA file or raw FASTA string using Biopython.
    
    Parameters:
        file_or_text: Uploaded file object, file buffer, or string.
        
    Returns:
        Tuple[bool, str, str, str]: (success, sequence_id, sequence_string, error_message)
    """
    try:
        # If it's a string, wrap in StringIO
        if isinstance(file_or_text, str):
            stream = io.StringIO(file_or_text.strip())
        else:
            # Handle Streamlit UploadedFile or BytesIO
            content = file_or_text.getvalue()
            if isinstance(content, bytes):
                stream = io.StringIO(content.decode("utf-8", errors="replace"))
            else:
                stream = io.StringIO(str(content))
                
        records = list(SeqIO.parse(stream, "fasta"))
        
        if not records:
            return False, "", "", "No valid FASTA records found. Make sure the header begins with '>'."
            
        first_record = records[0]
        seq_id = first_record.id or "FASTA_Sequence"
        cleaned_seq = clean_sequence(str(first_record.seq))
        
        if not cleaned_seq:
            return False, seq_id, "", "FASTA record found, but the sequence content is empty."
            
        return True, seq_id, cleaned_seq, ""
        
    except Exception as e:
        return False, "", "", f"Error reading FASTA data: {str(e)}"


def calculate_gc_content(sequence: str) -> float:
    """
    Calculate the GC content percentage of a DNA sequence.
    
    Parameters:
        sequence (str): DNA nucleotide string.
        
    Returns:
        float: GC content percentage (0.0 to 100.0).
    """
    clean_seq = clean_sequence(sequence).replace("-", "")
    if not clean_seq:
        return 0.0
    gc_count = clean_seq.count("G") + clean_seq.count("C")
    return round((gc_count / len(clean_seq)) * 100.0, 2)


def calculate_positional_similarity(seq1: str, seq2: str) -> Dict[str, Any]:
    """
    Perform a position-by-position comparison between two DNA sequences.
    
    Formula:
        Similarity (%) = (Number of matching positions / Maximum sequence length) * 100
        
    For unequal length sequences, missing positions are represented as gaps ('-')
    and counted as non-matches.
    
    Parameters:
        seq1 (str): Cleaned first DNA sequence.
        seq2 (str): Cleaned second DNA sequence.
        
    Returns:
        Dict[str, Any]: Detailed comparison metrics, position breakdown, and interpretation.
    """
    len1 = len(seq1)
    len2 = len(seq2)
    max_len = max(len1, len2)
    
    if max_len == 0:
        return {
            "len1": 0,
            "len2": 0,
            "max_len": 0,
            "matches": 0,
            "mismatches": 0,
            "gaps": 0,
            "similarity_percentage": 0.0,
            "interpretation_label": "No Data",
            "interpretation_desc": "Sequences are empty.",
            "comparison_rows": [],
            "aligned_seq1": "",
            "aligned_seq2": "",
            "match_string": ""
        }
        
    # Pad shorter sequence with gap character '-'
    padded_seq1 = seq1.ljust(max_len, "-")
    padded_seq2 = seq2.ljust(max_len, "-")
    
    matches = 0
    mismatches = 0
    gaps = 0
    
    comparison_rows = []
    match_symbols = []
    
    for i in range(max_len):
        c1 = padded_seq1[i]
        c2 = padded_seq2[i]
        pos = i + 1
        
        if c1 == "-" or c2 == "-":
            status = "Gap"
            gaps += 1
            symbol = " "
        elif c1 == c2:
            status = "Match"
            matches += 1
            symbol = "|"
        else:
            status = "Mismatch"
            mismatches += 1
            symbol = "."
            
        match_symbols.append(symbol)
        comparison_rows.append({
            "Position": pos,
            "Sequence 1": c1,
            "Sequence 2": c2,
            "Status": status,
            "Symbol": symbol
        })
        
    similarity_percentage = round((matches / max_len) * 100.0, 2)
    match_pct = round((matches / max_len) * 100.0, 2)
    mismatch_pct = round((mismatches / max_len) * 100.0, 2)
    gap_pct = round((gaps / max_len) * 100.0, 2)
    
    # Interpretation based on prompt guidelines
    if similarity_percentage >= 90.0:
        interp_label = "Very High Positional Similarity"
        interp_color = "#10B981"  # Emerald green
        interp_desc = "Sequences share 90% or more identical nucleotides at corresponding positions."
    elif similarity_percentage >= 70.0:
        interp_label = "High Positional Similarity"
        interp_color = "#0D9488"  # Teal
        interp_desc = "Sequences share a substantial degree of positional identity (70%–89%)."
    elif similarity_percentage >= 40.0:
        interp_label = "Moderate Positional Similarity"
        interp_color = "#F59E0B"  # Amber
        interp_desc = "Moderate correspondence (40%–69%). Several mismatches or gaps exist."
    else:
        interp_label = "Low Positional Similarity"
        interp_color = "#EF4444"  # Red
        interp_desc = "Fewer than 40% matching positions. High divergence or unaligned frames."
        
    return {
        "len1": len1,
        "len2": len2,
        "max_len": max_len,
        "matches": matches,
        "mismatches": mismatches,
        "gaps": gaps,
        "similarity_percentage": similarity_percentage,
        "match_percentage": match_pct,
        "mismatch_percentage": mismatch_pct,
        "gap_percentage": gap_pct,
        "gc_content1": calculate_gc_content(seq1),
        "gc_content2": calculate_gc_content(seq2),
        "interpretation_label": interp_label,
        "interpretation_color": interp_color,
        "interpretation_desc": interp_desc,
        "comparison_rows": comparison_rows,
        "aligned_seq1": padded_seq1,
        "aligned_seq2": padded_seq2,
        "match_string": "".join(match_symbols)
    }


def generate_text_report(stats: Dict[str, Any], name1: str = "Sequence 1", name2: str = "Sequence 2") -> str:
    """
    Generate an attractive formatted plain-text report summarizing comparison results.
    """
    report_lines = [
        "=" * 72,
        "          DNA SEQUENCE SIMILARITY CHECKER - ANALYSIS REPORT          ",
        "=" * 72,
        "",
        "PROJECT INFORMATION:",
        "  Algorithm: Simple Position-by-Position Comparison",
        "  Note: This is an unaligned positional comparison, not a full biological",
        "        alignment algorithm (e.g. Needleman-Wunsch or Smith-Waterman).",
        "",
        "-" * 72,
        "SUMMARY METRICS:",
        "-" * 72,
        f"  {name1} Length       : {stats['len1']} nt (GC: {stats['gc_content1']}%)",
        f"  {name2} Length       : {stats['len2']} nt (GC: {stats['gc_content2']}%)",
        f"  Maximum Length            : {stats['max_len']} positions",
        f"  Matching Positions        : {stats['matches']} ({stats['match_percentage']}%)",
        f"  Mismatching Positions     : {stats['mismatches']} ({stats['mismatch_percentage']}%)",
        f"  Gaps (Missing Positions)  : {stats['gaps']} ({stats['gap_percentage']}%)",
        "",
        f"  SIMILARITY PERCENTAGE     : {stats['similarity_percentage']}%",
        f"  INTERPRETATION CATEGORY   : {stats['interpretation_label']}",
        f"  DESCRIPTION               : {stats['interpretation_desc']}",
        "",
        "DISCLAIMER:",
        "  These categories are illustrative and do not establish evolutionary",
        "  or biological relatedness.",
        "",
        "-" * 72,
        "POSITIONAL ALIGNMENT VIEW (Chunks of 50 nt):",
        "-" * 72,
    ]
    
    seq1 = stats["aligned_seq1"]
    seq2 = stats["aligned_seq2"]
    syms = stats["match_string"]
    max_len = stats["max_len"]
    chunk_size = 50
    
    for start in range(0, max_len, chunk_size):
        end = min(start + chunk_size, max_len)
        chunk1 = seq1[start:end]
        chunk2 = seq2[start:end]
        chunk_syms = syms[start:end]
        
        report_lines.append(f"Position: {start + 1:>5} to {end:<5}")
        report_lines.append(f"  Seq 1 : {chunk1}")
        report_lines.append(f"  Match : {chunk_syms}")
        report_lines.append(f"  Seq 2 : {chunk2}")
        report_lines.append("")
        
    report_lines.append("=" * 72)
    report_lines.append("                    END OF REPORT                    ")
    report_lines.append("=" * 72)
    
    return "\n".join(report_lines)
