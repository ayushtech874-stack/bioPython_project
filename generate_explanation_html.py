"""
generate_explanation_html.py
=============================
Generates a comprehensive, interactive, publication-quality HTML document:
'ProjectExplanation.html' containing full project documentation, code walkthroughs,
methodology, system architecture, dependencies, and 25+ Viva Voce questions & answers.
"""

import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DNA Sequence Similarity Checker - Complete Project Masterclass & Viva Guide</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0F172A;
            --primary-light: #1E293B;
            --accent: #0D9488;
            --accent-light: #14B8A6;
            --accent-bg: #CCFBF1;
            --success: #10B981;
            --success-bg: #DCFCE7;
            --danger: #EF4444;
            --danger-bg: #FEE2E2;
            --warning: #F59E0B;
            --warning-bg: #FEF3C7;
            --text-main: #334155;
            --text-muted: #64748B;
            --border: #E2E8F0;
            --bg-light: #F8FAFC;
            --bg-card: #FFFFFF;
            --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-sans);
            color: var(--text-main);
            background-color: var(--bg-light);
            line-height: 1.65;
            -webkit-font-smoothing: antialiased;
        }

        /* Layout Container */
        .page-wrapper {
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: 280px;
            background-color: var(--primary);
            color: #FFFFFF;
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            padding: 30px 20px;
            flex-shrink: 0;
            border-right: 1px solid #334155;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 18px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .sidebar-menu {
            list-style: none;
        }

        .sidebar-menu li {
            margin-bottom: 8px;
        }

        .sidebar-menu a {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #94A3B8;
            text-decoration: none;
            font-size: 13.5px;
            font-weight: 600;
            padding: 8px 12px;
            border-radius: 8px;
            transition: all 0.2s ease;
        }

        .sidebar-menu a:hover {
            color: #FFFFFF;
            background-color: rgba(255,255,255,0.08);
        }

        /* Main Content */
        .main-content {
            flex: 1;
            padding: 40px 60px;
            max-width: 1200px;
        }

        /* Header Card */
        .hero-banner {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-radius: 20px;
            padding: 40px;
            color: #FFFFFF;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.2);
            position: relative;
            overflow: hidden;
        }

        .hero-banner::after {
            content: '🧬';
            position: absolute;
            right: 40px;
            top: 30px;
            font-size: 120px;
            opacity: 0.12;
            pointer-events: none;
        }

        .badge-tag {
            display: inline-block;
            background: rgba(13, 148, 136, 0.25);
            color: #2DD4BF;
            border: 1px solid rgba(45, 212, 191, 0.4);
            font-size: 12px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 15px;
        }

        .hero-title {
            font-size: 34px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }

        .hero-subtitle {
            font-size: 16px;
            color: #CBD5E1;
            max-width: 800px;
            line-height: 1.6;
        }

        .meta-badges {
            display: flex;
            gap: 12px;
            margin-top: 25px;
            flex-wrap: wrap;
        }

        .meta-chip {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 13px;
            color: #E2E8F0;
            font-weight: 600;
        }

        /* Typography */
        h2.section-heading {
            font-size: 24px;
            font-weight: 800;
            color: var(--primary);
            margin: 50px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--border);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        h3.sub-heading {
            font-size: 18px;
            font-weight: 700;
            color: var(--primary);
            margin: 30px 0 12px 0;
        }

        p {
            margin-bottom: 16px;
            font-size: 15px;
            color: #334155;
        }

        /* Card Container */
        .doc-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -2px rgba(0, 0, 0, 0.02);
        }

        /* Tables */
        .styled-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 20px 0;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid var(--border);
            background-color: #FFFFFF;
        }

        .styled-table th {
            background-color: var(--primary);
            color: #FFFFFF;
            font-weight: 700;
            text-align: left;
            padding: 12px 16px;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .styled-table td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
            color: #334155;
        }

        .styled-table tr:last-child td {
            border-bottom: none;
        }

        .styled-table tr:nth-child(even) td {
            background-color: #F8FAFC;
        }

        /* Code Blocks */
        pre code {
            display: block;
            background: #0F172A;
            color: #F8FAFC;
            padding: 18px 22px;
            border-radius: 12px;
            font-family: var(--font-mono);
            font-size: 13.5px;
            line-height: 1.5;
            overflow-x: auto;
            margin: 15px 0;
            box-shadow: 0 4px 10px rgba(15, 23, 42, 0.15);
        }

        code.inline-code {
            font-family: var(--font-mono);
            background: #F1F5F9;
            color: #0F172A;
            padding: 2px 6px;
            border-radius: 5px;
            font-size: 13.5px;
            border: 1px solid #E2E8F0;
        }

        /* Formula Box */
        .formula-box {
            background: linear-gradient(to right, #F0FDFA, #F8FAFC);
            border-left: 5px solid var(--accent);
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 16px;
            font-weight: 600;
            color: var(--primary);
        }

        /* Method Cards */
        .method-block {
            border: 1px solid var(--border);
            border-radius: 12px;
            margin-bottom: 20px;
            background: #FFFFFF;
            overflow: hidden;
        }

        .method-header {
            background: #F8FAFC;
            padding: 14px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .method-name {
            font-family: var(--font-mono);
            font-weight: 700;
            color: var(--accent);
            font-size: 15px;
        }

        .method-file {
            font-size: 12px;
            background: #E2E8F0;
            color: var(--primary);
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 600;
        }

        .method-body {
            padding: 18px 20px;
        }

        /* Accordion for Viva Questions */
        .accordion-item {
            border: 1px solid var(--border);
            border-radius: 10px;
            margin-bottom: 12px;
            background: #FFFFFF;
            transition: all 0.2s ease;
        }

        .accordion-item:hover {
            border-color: #CBD5E1;
        }

        .accordion-header {
            padding: 16px 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-weight: 700;
            color: var(--primary);
            font-size: 15px;
            user-select: none;
        }

        .accordion-header:hover {
            color: var(--accent);
        }

        .accordion-icon {
            font-size: 18px;
            color: var(--accent);
            transition: transform 0.25s ease;
        }

        .accordion-body {
            display: none;
            padding: 0 20px 18px 20px;
            border-top: 1px solid #F1F5F9;
            color: #475569;
            font-size: 14.5px;
            line-height: 1.6;
        }

        .accordion-item.active .accordion-body {
            display: block;
            padding-top: 14px;
        }

        .accordion-item.active .accordion-icon {
            transform: rotate(45deg);
        }

        .viva-badge {
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 4px;
            margin-right: 8px;
            text-transform: uppercase;
        }

        .badge-concept { background: #E0E7FF; color: #4338CA; }
        .badge-code { background: #FEF3C7; color: #92400E; }
        .badge-bio { background: #DCFCE7; color: #166534; }
        .badge-algo { background: #FCE7F3; color: #9D174D; }

        /* Responsive Design */
        @media (max-width: 900px) {
            .page-wrapper { flex-direction: column; }
            .sidebar { width: 100%; height: auto; position: relative; }
            .main-content { padding: 25px 20px; }
        }
    </style>
</head>
<body>

<div class="page-wrapper">
    <!-- Sidebar Navigation -->
    <nav class="sidebar">
        <div class="sidebar-brand">
            <span>🧬</span> DNA Project Docs
        </div>
        <ul class="sidebar-menu">
            <li><a href="#overview">📌 1. Project Overview & PS</a></li>
            <li><a href="#biology">🔬 2. Biological Background</a></li>
            <li><a href="#algorithm">📐 3. Algorithm & Math</a></li>
            <li><a href="#architecture">📁 4. Project Architecture</a></li>
            <li><a href="#dependencies">📦 5. Code Dependencies</a></li>
            <li><a href="#methods">⚙️ 6. Methods & Functionality</a></li>
            <li><a href="#viva">🎓 7. Comprehensive Viva Voce</a></li>
            <li><a href="#run-guide">🚀 8. Execution & Testing</a></li>
        </ul>
    </nav>

    <!-- Main Content Area -->
    <main class="main-content">
        <!-- Hero Header -->
        <header class="hero-banner" id="overview">
            <span class="badge-tag">Comprehensive Masterclass Documentation</span>
            <h1 class="hero-title">DNA Sequence Similarity Checker</h1>
            <p class="hero-subtitle">
                A production-ready computational bioinformatics web application built with Python 3, Streamlit,
                Biopython, Matplotlib, and Pandas. Explaining sequence alignment, mutation identification, FASTA processing,
                and viva voce questions.
            </p>
            <div class="meta-badges">
                <span class="meta-chip">🐍 Python 3.10+</span>
                <span class="meta-chip">🧬 Biopython 1.80+</span>
                <span class="meta-chip">📊 Streamlit & Matplotlib</span>
                <span class="meta-chip">📘 College & Lab Grade</span>
            </div>
        </header>

        <!-- SECTION 1: Problem Statement & Objectives -->
        <section>
            <h2 class="section-heading">📌 1. Problem Statement & Scope</h2>
            <div class="doc-card">
                <h3 class="sub-heading">The Problem (Why this project exists)</h3>
                <p>
                    Deoxyribonucleic acid (DNA) stores the complete biological blueprint of life. In modern molecular genetics,
                    a single change in the nucleotide sequence (an <em>Adenine (A), Thymine (T), Guanine (G), or Cytosine (C)</em>)
                    can determine whether an organism is healthy or develops a pathological genetic disorder.
                </p>
                <p>
                    Bioinformatics students frequently struggle to connect abstract molecular biology theory with tangible computational algorithms.
                    Many commercial tools (like NCBI BLAST) operate as black boxes with complex web services. This project was engineered to solve that
                    educational problem by providing a <strong>transparent, position-by-position comparison engine</strong> where every single nucleotide
                    is validated, indexed, color-coded, and graphed in real-time.
                </p>

                <h3 class="sub-heading">Core Objectives</h3>
                <ul style="margin-left: 20px; line-height: 1.8;">
                    <li>Provide dual sequence input via <strong>manual typing</strong> or <strong>FASTA file upload</strong>.</li>
                    <li>Validate input integrity against legal DNA bases (<code>A, T, G, C</code> and optional ambiguous base <code>N</code>).</li>
                    <li>Compute rigorous positional similarity percentage while handling unequal lengths with gap-padding.</li>
                    <li>Render color-coded alignment views (Green = Match, Red = Mismatch, Grey = Gap).</li>
                    <li>Generate publication-quality charts (Bar chart, Donut chart, and Sequence Track plot).</li>
                    <li>Export results as structured <strong>CSV</strong>, lab summary <strong>TXT</strong>, and editable Word <strong>DOCX</strong> reports.</li>
                </ul>
            </div>
        </section>

        <!-- SECTION 2: Biological Background -->
        <section id="biology">
            <h2 class="section-heading">🔬 2. Biological Background & Context</h2>
            <div class="doc-card">
                <p>
                    DNA is composed of two polynucleotide chains coiled around each other in a double helix. The four nitrogenous bases are:
                </p>
                <ul style="margin-left: 20px; line-height: 1.8;">
                    <li><strong>Purines (Double-ring):</strong> Adenine (A) and Guanine (G)</li>
                    <li><strong>Pyrimidines (Single-ring):</strong> Thymine (T) and Cytosine (C)</li>
                </ul>

                <h3 class="sub-heading">Real-World Case Study: Sickle Cell Anemia</h3>
                <p>
                    To demonstrate the clinical power of DNA similarity checking, our application includes a verified preset for human Beta-Globin (<em>HBB</em>):
                </p>
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Allele</th>
                            <th>DNA Sequence (Codons 4 to 9)</th>
                            <th>Codon 6</th>
                            <th>Translated Amino Acid</th>
                            <th>Clinical Phenotype</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>HbA (Normal)</strong></td>
                            <td><code>ACT CCT <strong>GAG</strong> GAG AAG TCT</code></td>
                            <td><code>GAG</code></td>
                            <td>Glutamic Acid (Hydrophilic)</td>
                            <td>Normal Biconcave Erythrocytes</td>
                        </tr>
                        <tr>
                            <td><strong>HbS (Sickle)</strong></td>
                            <td><code>ACT CCT <strong>GTG</strong> GAG AAG TCT</code></td>
                            <td><code>GTG</code></td>
                            <td>Valine (Hydrophobic)</td>
                            <td>Sickle Cell Hemoglobin Polymerization</td>
                        </tr>
                    </tbody>
                </table>
                <p>
                    A single transversion mutation at position 8 (<code>A &rarr; T</code>) alters protein folding, demonstrating why positional nucleotide comparison is critical.
                </p>
            </div>
        </section>

        <!-- SECTION 3: Algorithm & Math -->
        <section id="algorithm">
            <h2 class="section-heading">📐 3. Mathematical Formulation & Algorithm</h2>
            <div class="doc-card">
                <p>
                    Let Sequence 1 be $S_1$ of length $L_1$, and Sequence 2 be $S_2$ of length $L_2$.
                    The maximum sequence length is:
                </p>
                <div class="formula-box">
                    $$L_{max} = \\max(L_1, L_2)$$
                </div>
                <p>
                    If $L_1 \neq L_2$, the shorter sequence is padded with gap characters (<code>-</code>) up to length $L_{max}$.
                    At each index $i$ ($1 \le i \le L_{max}$), the status is:
                </p>
                <pre><code>if S1[i] == '-' or S2[i] == '-':
    Status = "Gap" (Non-match)
elif S1[i] == S2[i]:
    Status = "Match"
else:
    Status = "Mismatch"</code></pre>

                <p>The overall <strong>Positional Similarity Percentage</strong> is:</p>
                <div class="formula-box">
                    $$\text{Similarity (\%)} = \left( \frac{\text{Total Matches}}{L_{max}} \right) \times 100$$
                </div>

                <h3 class="sub-heading">Positional Comparison vs. Dynamic Programming Alignment</h3>
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Dimension</th>
                            <th>Positional Comparison (This Project)</th>
                            <th>Global Alignment (Needleman-Wunsch)</th>
                            <th>Local Alignment (Smith-Waterman / BLAST)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Method</strong></td>
                            <td>Strict 1-to-1 index matching ($S_1[i]$ vs $S_2[i]$)</td>
                            <td>Dynamic Programming with Gap Penalties</td>
                            <td>Dynamic Programming / Heuristic Word Seeds</td>
                        </tr>
                        <tr>
                            <td><strong>Frameshift Sensitivity</strong></td>
                            <td>High: 1 insertion ruins all downstream matches</td>
                            <td>Tolerant: Places gaps to realign homologous regions</td>
                            <td>Tolerant: Discovers matching blocks anywhere</td>
                        </tr>
                        <tr>
                            <td><strong>Time Complexity</strong></td>
                            <td>$O(N)$ Linear time</td>
                            <td>$O(N \times M)$ Quadratic time</td>
                            <td>$O(N \times M)$ Quadratic time</td>
                        </tr>
                        <tr>
                            <td><strong>Best Used For</strong></td>
                            <td>Pre-aligned genes, SNPs, point mutations</td>
                            <td>Full-length evolutionary gene alignment</td>
                            <td>Database searches & motif discovery</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

                <!-- SECTION 4: System & Code Architecture Masterclass -->
        <section id="architecture">
            <h2 class="section-heading">📁 4. System & Code Architecture Masterclass</h2>
            
            <div class="doc-card">
                <h3 style="color: var(--accent); margin-bottom: 12px;">4.1 High-Level System Architecture & End-to-End Pipeline</h3>
                <p>
                    The DNA Sequence Similarity Checker is engineered with a decoupled, asynchronous 5-tier architecture.
                    It strictly isolates the client presentation layer from biological sequence computation and serialization services.
                </p>

                <!-- High-Level System Architecture SVG Diagram -->
                <div style="background: #0F172A; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin: 20px 0; overflow-x: auto;">
                    <svg viewBox="0 0 960 490" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Plus Jakarta Sans', sans-serif;">
                        <defs>
                            <linearGradient id="gradClient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#0F766E"/>
                                <stop offset="100%" stop-color="#14B8A6"/>
                            </linearGradient>
                            <linearGradient id="gradController" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#1E3A8A"/>
                                <stop offset="100%" stop-color="#3B82F6"/>
                            </linearGradient>
                            <linearGradient id="gradBio" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#065F46"/>
                                <stop offset="100%" stop-color="#10B981"/>
                            </linearGradient>
                            <linearGradient id="gradVis" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#581C87"/>
                                <stop offset="100%" stop-color="#8B5CF6"/>
                            </linearGradient>
                            <linearGradient id="gradExport" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#92400E"/>
                                <stop offset="100%" stop-color="#F59E0B"/>
                            </linearGradient>
                            <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                                <path d="M 0 1 L 8 5 L 0 9 z" fill="#38BDF8"/>
                            </marker>
                        </defs>

                        <!-- Background Grid Lines -->
                        <g stroke="#1E293B" stroke-width="1">
                            <line x1="40" y1="90" x2="920" y2="90"/>
                            <line x1="40" y1="180" x2="920" y2="180"/>
                            <line x1="40" y1="270" x2="920" y2="270"/>
                            <line x1="40" y1="360" x2="920" y2="360"/>
                        </g>

                        <!-- Tier 1: Client Presentation -->
                        <rect x="50" y="30" width="860" height="65" rx="10" fill="#1E293B" stroke="#0D9488" stroke-width="1.8"/>
                        <rect x="65" y="42" width="160" height="40" rx="6" fill="url(#gradClient)"/>
                        <text x="145" y="66" fill="#FFFFFF" font-size="12" font-weight="bold" text-anchor="middle">1. Client / Browser</text>
                        <text x="245" y="58" fill="#F8FAFC" font-size="13" font-weight="bold">Streamlit Web Dashboard (Port 8501)</text>
                        <text x="245" y="76" fill="#94A3B8" font-size="11">Form Isolation (Zero-Lag Typing) | Reactive View Engine | HTML5 Alignment Matrix</text>

                        <!-- Tier 2: Controller & State -->
                        <rect x="50" y="115" width="860" height="65" rx="10" fill="#1E293B" stroke="#3B82F6" stroke-width="1.8"/>
                        <rect x="65" y="127" width="160" height="40" rx="6" fill="url(#gradController)"/>
                        <text x="145" y="151" fill="#FFFFFF" font-size="12" font-weight="bold" text-anchor="middle">2. Controller & State</text>
                        <text x="245" y="143" fill="#F8FAFC" font-size="13" font-weight="bold">Streamlit SessionState &amp; Cache Tier</text>
                        <text x="245" y="161" fill="#94A3B8" font-size="11">`st.session_state` Cache | `@st.cache_data` Memoization | Event Listeners &amp; Preset Dispatchers</text>

                        <!-- Tier 3: Ingestion & Validation -->
                        <rect x="50" y="200" width="860" height="65" rx="10" fill="#1E293B" stroke="#10B981" stroke-width="1.8"/>
                        <rect x="65" y="212" width="160" height="40" rx="6" fill="url(#gradBio)"/>
                        <text x="145" y="236" fill="#FFFFFF" font-size="12" font-weight="bold" text-anchor="middle">3. Ingestion &amp; Validation</text>
                        <text x="245" y="228" fill="#F8FAFC" font-size="13" font-weight="bold">Biopython Parsing &amp; Normalization Service</text>
                        <text x="245" y="246" fill="#94A3B8" font-size="11">`Bio.SeqIO` FASTA Parser | Regex Whitespace Stripper | Case Normalizer | IUPAC Nucleotide Validator</text>

                        <!-- Tier 4: Core Domain Logic -->
                        <rect x="50" y="285" width="860" height="65" rx="10" fill="#1E293B" stroke="#8B5CF6" stroke-width="1.8"/>
                        <rect x="65" y="297" width="160" height="40" rx="6" fill="url(#gradVis)"/>
                        <text x="145" y="321" fill="#FFFFFF" font-size="12" font-weight="bold" text-anchor="middle">4. Computational Core</text>
                        <text x="245" y="313" fill="#F8FAFC" font-size="13" font-weight="bold">Positional Alignment &amp; Metric Engine</text>
                        <text x="245" y="331" fill="#94A3B8" font-size="11">Index Matching Matrix | Gap Trailing Padding | GC-Content Calculator | Similarity Categorizer</text>

                        <!-- Tier 5: Output & Serialization -->
                        <rect x="50" y="370" width="860" height="65" rx="10" fill="#1E293B" stroke="#F59E0B" stroke-width="1.8"/>
                        <rect x="65" y="382" width="160" height="40" rx="6" fill="url(#gradExport)"/>
                        <text x="145" y="406" fill="#FFFFFF" font-size="12" font-weight="bold" text-anchor="middle">5. Export &amp; Graphics</text>
                        <text x="245" y="398" fill="#F8FAFC" font-size="13" font-weight="bold">Matplotlib Agg Vectorizer &amp; Multi-Format Exporters</text>
                        <text x="245" y="416" fill="#94A3B8" font-size="11">Bar/Donut/Track Renderers | CSV Positional Streamer | Text Summary Builder | DOCX Word Compiler</text>

                        <!-- Connector Arrows -->
                        <path d="M 480 95 L 480 115" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)"/>
                        <path d="M 480 180 L 480 200" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)"/>
                        <path d="M 480 265 L 480 285" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)"/>
                        <path d="M 480 350 L 480 370" stroke="#38BDF8" stroke-width="2.5" marker-end="url(#arrow)"/>

                        <!-- Footer Meta -->
                        <text x="480" y="465" fill="#64748B" font-size="11" text-anchor="middle">End-to-End Reactive Data Flow: Client Request → Normalization → Algorithmic Scoring → Visualization &amp; Export</text>
                    </svg>
                </div>

                <p>
                    <strong>Execution Flow Walkthrough:</strong>
                </p>
                <ol style="margin-left: 20px; margin-bottom: 20px; color: var(--text-main);">
                    <li><strong>Form Isolation &amp; Dispatch:</strong> The user enters DNA sequences into a decoupled <code>st.form</code>. Unlike raw input widgets that fire a rerun on every keystroke, the form batches interactions entirely in the browser DOM, executing a single WebSocket message only when submitted.</li>
                    <li><strong>Data Ingestion &amp; Routing:</strong> Inputs are routed to <code>parse_fasta()</code> if starting with a FASTA header <code>&gt;</code>, invoking Biopython's <code>Bio.SeqIO.read()</code>. Raw sequences are cleansed of whitespace and uppercase-normalized.</li>
                    <li><strong>Guard-Clause Validation:</strong> Sequence strings are evaluated against IUPAC nucleotide regexes. If illegal characters are discovered, execution halts cleanly with an error notification.</li>
                    <li><strong>Algorithmic Execution:</strong> Valid sequences enter <code>calculate_positional_similarity()</code>. The algorithm computes 1-to-1 index identity, trailing gap counts, GC content ratios, and qualitative interpretation thresholds.</li>
                    <li><strong>Memoized Output Dispatch:</strong> Result payloads are cached with <code>@st.cache_data</code> to enable zero-latency page transitions, dynamic HTML alignment generation, and export generation (CSV, TXT, DOCX).</li>
                </ol>

                <hr style="border: 0; border-top: 1px solid var(--border); margin: 25px 0;">

                <h3 style="color: var(--accent); margin-bottom: 12px;">4.2 Code Architecture &amp; Modular Decomposition</h3>
                <p>
                    The codebase strictly adheres to the <strong>Single Responsibility Principle (SRP)</strong> and <strong>Separation of Concerns (SoC)</strong>.
                    Domain logic and mathematical calculations are strictly decoupled from Streamlit presentation code, ensuring 100% automated testability.
                </p>

                <!-- Code Architecture SVG Diagram -->
                <div style="background: #0F172A; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin: 20px 0; overflow-x: auto;">
                    <svg viewBox="0 0 960 460" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Plus Jakarta Sans', sans-serif;">
                        <!-- Modules Boxes -->
                        <!-- run_app.py -->
                        <g>
                            <rect x="50" y="30" width="220" height="70" rx="8" fill="#1E293B" stroke="#0D9488" stroke-width="2"/>
                            <text x="160" y="58" fill="#2DD4BF" font-size="13" font-weight="bold" text-anchor="middle">🚀 run_app.py</text>
                            <text x="160" y="78" fill="#94A3B8" font-size="10.5" text-anchor="middle">Root Launcher &amp; Subprocess</text>
                        </g>

                        <!-- app.py -->
                        <g>
                            <rect x="360" y="30" width="250" height="95" rx="8" fill="#1E293B" stroke="#38BDF8" stroke-width="2"/>
                            <text x="485" y="58" fill="#38BDF8" font-size="14" font-weight="bold" text-anchor="middle">💻 dna_similarity_checker/app.py</text>
                            <text x="485" y="78" fill="#F8FAFC" font-size="11" text-anchor="middle">Streamlit Reactive UI &amp; Router</text>
                            <text x="485" y="98" fill="#94A3B8" font-size="10" text-anchor="middle">Form Batching | Session State | Caching</text>
                        </g>

                        <!-- test_checker.py -->
                        <g>
                            <rect x="690" y="30" width="220" height="70" rx="8" fill="#1E293B" stroke="#10B981" stroke-width="2"/>
                            <text x="800" y="58" fill="#34D399" font-size="13" font-weight="bold" text-anchor="middle">🧪 test_checker.py</text>
                            <text x="800" y="78" fill="#94A3B8" font-size="10.5" text-anchor="middle">Automated 8-Test Suite</text>
                        </g>

                        <!-- sequence_utils.py -->
                        <g>
                            <rect x="180" y="190" width="280" height="130" rx="8" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
                            <text x="320" y="218" fill="#FBBF24" font-size="13.5" font-weight="bold" text-anchor="middle">⚙️ sequence_utils.py</text>
                            <text x="320" y="238" fill="#F8FAFC" font-size="11" text-anchor="middle">Pure Biological Computational Core</text>
                            <line x1="195" y1="248" x2="445" y2="248" stroke="#334155" stroke-width="1"/>
                            <text x="200" y="266" fill="#94A3B8" font-size="10">• clean_sequence()</text>
                            <text x="200" y="282" fill="#94A3B8" font-size="10">• validate_dna_sequence()</text>
                            <text x="200" y="298" fill="#94A3B8" font-size="10">• parse_fasta() (BioPython)</text>
                            <text x="330" y="266" fill="#94A3B8" font-size="10">• calculate_positional_similarity()</text>
                            <text x="330" y="282" fill="#94A3B8" font-size="10">• calculate_gc_content()</text>
                            <text x="330" y="298" fill="#94A3B8" font-size="10">• generate_text_report()</text>
                        </g>

                        <!-- visualization.py -->
                        <g>
                            <rect x="520" y="190" width="280" height="130" rx="8" fill="#1E293B" stroke="#EC4899" stroke-width="2"/>
                            <text x="660" y="218" fill="#F472B6" font-size="13.5" font-weight="bold" text-anchor="middle">🎨 visualization.py</text>
                            <text x="660" y="238" fill="#F8FAFC" font-size="11" text-anchor="middle">Rendering &amp; Graphics Engine</text>
                            <line x1="535" y1="248" x2="785" y2="248" stroke="#334155" stroke-width="1"/>
                            <text x="540" y="266" fill="#94A3B8" font-size="10">• plot_comparison_barchart()</text>
                            <text x="540" y="282" fill="#94A3B8" font-size="10">• plot_similarity_donut()</text>
                            <text x="540" y="298" fill="#94A3B8" font-size="10">• plot_position_track()</text>
                            <text x="670" y="266" fill="#94A3B8" font-size="10">• render_html_sequence_alignment()</text>
                            <text x="670" y="282" fill="#94A3B8" font-size="10">• Matplotlib Agg Non-Interactive</text>
                            <text x="670" y="298" fill="#94A3B8" font-size="10">• Theme-Adaptive Contrast CSS</text>
                        </g>

                        <!-- Supporting Generators -->
                        <g>
                            <rect x="250" y="370" width="220" height="60" rx="6" fill="#1E293B" stroke="#64748B" stroke-width="1.5"/>
                            <text x="360" y="394" fill="#CBD5E1" font-size="11.5" font-weight="bold" text-anchor="middle">📄 generate_docx_report.py</text>
                            <text x="360" y="412" fill="#94A3B8" font-size="9.5" text-anchor="middle">Academic Word (.docx) Builder</text>
                        </g>
                        <g>
                            <rect x="510" y="370" width="230" height="60" rx="6" fill="#1E293B" stroke="#64748B" stroke-width="1.5"/>
                            <text x="625" y="394" fill="#CBD5E1" font-size="11.5" font-weight="bold" text-anchor="middle">🌐 generate_explanation_html.py</text>
                            <text x="625" y="412" fill="#94A3B8" font-size="9.5" text-anchor="middle">Interactive HTML Docs Generator</text>
                        </g>

                        <!-- Dependency Flow Lines -->
                        <path d="M 270 65 L 360 65" stroke="#38BDF8" stroke-width="2" marker-end="url(#arrow)"/>
                        <path d="M 430 125 L 340 190" stroke="#F59E0B" stroke-width="2" marker-end="url(#arrow)"/>
                        <path d="M 540 125 L 630 190" stroke="#EC4899" stroke-width="2" marker-end="url(#arrow)"/>
                        <path d="M 750 100 L 440 190" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#arrow)"/>
                        <path d="M 780 100 L 680 190" stroke="#EC4899" stroke-width="1.5" stroke-dasharray="4,4" marker-end="url(#arrow)"/>
                    </svg>
                </div>

                <h4 style="margin: 18px 0 10px 0; color: var(--primary);">Modular Responsibility Matrix</h4>
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>File / Module</th>
                            <th>Layer</th>
                            <th>Key Responsibilities</th>
                            <th>Design Pattern Employed</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>run_app.py</code></td>
                            <td>Entry Point</td>
                            <td>Resolves virtual environment path, sets headless configuration, launches Streamlit subprocess.</td>
                            <td><strong>Facade Pattern</strong> (simplified launch CLI)</td>
                        </tr>
                        <tr>
                            <td><code>dna_similarity_checker/app.py</code></td>
                            <td>Presentation &amp; Controller</td>
                            <td>Manages Streamlit session state, renders forms, binds sample presets, dispatches cached calculations.</td>
                            <td><strong>MVC Controller / Reactive View</strong></td>
                        </tr>
                        <tr>
                            <td><code>dna_similarity_checker/sequence_utils.py</code></td>
                            <td>Domain Logic</td>
                            <td>Pure computational functions for FASTA ingestion, string cleaning, DNA validation, and positional identity math.</td>
                            <td><strong>Pipeline Pattern &amp; Pure Functions</strong></td>
                        </tr>
                        <tr>
                            <td><code>dna_similarity_checker/visualization.py</code></td>
                            <td>Graphics Engine</td>
                            <td>Constructs publication-grade Matplotlib figures and HTML color-coded alignment chunk matrices.</td>
                            <td><strong>Renderer Pattern / Strategy Pattern</strong></td>
                        </tr>
                        <tr>
                            <td><code>dna_similarity_checker/test_checker.py</code></td>
                            <td>Quality Assurance</td>
                            <td>Executes 8 automated unit tests verifying benchmark cases, unequal lengths, error bounds, and FASTA records.</td>
                            <td><strong>Automated Unit Test Suite</strong></td>
                        </tr>
                    </tbody>
                </table>

                <h4 style="margin: 22px 0 10px 0; color: var(--primary);">Data Contract: Positional Similarity Output Schema</h4>
                <p>
                    When <code>calculate_positional_similarity(s1, s2)</code> completes, it yields a standardized, strongly-typed dictionary:
                </p>
                <pre><code>{
    "len1": 18,                                 # int: Length of Sequence 1
    "len2": 18,                                 # int: Length of Sequence 2
    "max_len": 18,                              # int: Maximum alignment length (denominator)
    "matches": 17,                              # int: Number of identical nucleotides at same index
    "mismatches": 1,                            # int: Number of differing nucleotides
    "gaps": 0,                                  # int: Trailing unaligned gap positions
    "similarity_percentage": 94.44,             # float: (matches / max_len) * 100
    "match_percentage": 94.44,                  # float: Percentage of matches
    "mismatch_percentage": 5.56,                # float: Percentage of mismatches
    "gap_percentage": 0.0,                      # float: Percentage of gaps
    "gc_content1": 50.0,                        # float: (G+C)/len1 * 100 for Seq 1
    "gc_content2": 50.0,                        # float: (G+C)/len2 * 100 for Seq 2
    "interpretation_label": "Very High Positional Similarity",
    "interpretation_color": "#10B981",          # Hex code for UI status badge
    "interpretation_desc": "Sequences share 90% or more identical nucleotides...",
    "aligned_seq1": "ACTCCTGAGGAGAAGTCT",       # str: Padded Sequence 1
    "aligned_seq2": "ACTCCTGTGGAGAAGTCT",       # str: Padded Sequence 2
    "match_string": "|||||||.||||||||||",       # str: Alignment representation (| = match, . = mismatch, - = gap)
    "comparison_rows": [                        # List[Dict]: Position-by-position row breakdown
        {"Position": 1, "Sequence 1": "A", "Sequence 2": "A", "Status": "Match", "Symbol": "|"},
        {"Position": 8, "Sequence 1": "A", "Sequence 2": "T", "Status": "Mismatch", "Symbol": "."}
    ]
}</code></pre>

                <hr style="border: 0; border-top: 1px solid var(--border); margin: 25px 0;">

                <h3 style="color: var(--accent); margin-bottom: 12px;">4.3 Architectural Evaluation: "Why Streamlit?" &amp; Performance Engineering</h3>
                <p>
                    Bioinformatics software architects frequently evaluate whether to build applications in <strong>Streamlit</strong>, 
                    <strong>Flask/FastAPI + React</strong>, or <strong>pure Client-Side JavaScript/WebAssembly</strong>.
                    Here is the definitive architectural comparison:
                </p>

                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Evaluation Criterion</th>
                            <th>Streamlit (This Project)</th>
                            <th>FastAPI / Flask + React</th>
                            <th>Client-Side JS / WebAssembly</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Language Ecosystem</strong></td>
                            <td><span style="color:#10B981; font-weight:bold;">100% Pure Python</span></td>
                            <td>Python (Backend) + TypeScript/React (Frontend)</td>
                            <td>JavaScript / TypeScript / Rust (WASM)</td>
                        </tr>
                        <tr>
                            <td><strong>Biopython Compatibility</strong></td>
                            <td><span style="color:#10B981; font-weight:bold;">Direct in-process</span> (<code>Bio.SeqIO</code>, <code>Bio.Seq</code>)</td>
                            <td>Requires JSON REST API serialization bridge</td>
                            <td>Difficult; requires Pyodide or JS reimplementation</td>
                        </tr>
                        <tr>
                            <td><strong>State &amp; Execution Model</strong></td>
                            <td>Server-driven reactive loop over WebSockets</td>
                            <td>Client-side virtual DOM with async REST fetches</td>
                            <td>Pure client-side event-driven rendering</td>
                        </tr>
                        <tr>
                            <td><strong>Development Overhead</strong></td>
                            <td><span style="color:#10B981; font-weight:bold;">Minimal (Single codebase, zero build step)</span></td>
                            <td>High (2 codebases, CORS, npm/vite packaging)</td>
                            <td>Moderate to High</td>
                        </tr>
                        <tr>
                            <td><strong>Why It Can Feel Laggy</strong></td>
                            <td>Reruns entire script on unbatched input events</td>
                            <td>Network latency on unoptimized API endpoints</td>
                            <td>Client device CPU bottlenecks on large datasets</td>
                        </tr>
                        <tr>
                            <td><strong>Best Architectural Fit</strong></td>
                            <td><strong>Bioinformatics research, clinical prototypes, data science dashboards</strong></td>
                            <td>Commercial multi-tenant SaaS platforms</td>
                            <td>Offline standalone browser tools</td>
                        </tr>
                    </tbody>
                </table>

                <h4 style="margin: 18px 0 10px 0; color: var(--primary);">Root Causes of Localhost Latency &amp; How We Solved Them:</h4>
                <div class="callout callout-info">
                    <p><strong>1. Input Typing Lag Eliminated via Form Batching:</strong></p>
                    <p>
                        In standard Streamlit implementations, placing <code>st.text_area</code> in the open script body causes a full server re-execution on every key stroke or debounced pause.
                        By wrapping input widgets inside <code>with st.form("dna_comparison_form"):</code>, input state changes are retained entirely within the client's browser memory until the user clicks <em>"Run Sequence Comparison"</em>. Typing operates at 60 FPS without WebSocket round-trips.
                    </p>
                </div>
                <div class="callout callout-info">
                    <p><strong>2. Matplotlib Font Scanner Bottleneck Removed:</strong></p>
                    <p>
                        On Windows systems, Matplotlib's default font manager scans the entire <code>C:\Windows\Fonts</code> directory when requested to resolve non-standard weights (such as <code>semibold</code> or <code>medium</code>). This caused a 3-5 second delay during plot rasterization.
                        We resolved this by setting global font preferences to pre-cached <code>DejaVu Sans</code> and standard weights (<code>bold</code>, <code>normal</code>), and caching figure generators with <code>@st.cache_data</code>.
                    </p>
                </div>
                <div class="callout callout-info">
                    <p><strong>3. Contrast &amp; Invisibility Fixed with Adaptive Dark-Theming:</strong></p>
                    <p>
                        Hardcoded deep navy colors (<code>#0F172A</code>) previously resulted in near-zero contrast when rendered against Streamlit's dark mode background (<code>#0E1117</code>).
                        We re-engineered the styling system with explicit high-contrast text (<code>#F8FAFC</code>), slate card backdrops (<code>#1E293B</code>), and vibrant color-coded status badges.
                    </p>
                </div>

                <h4 style="margin: 18px 0 10px 0; color: var(--primary);">4.4 Complete Project Directory Tree</h4>
                <pre><code>bioPython_project/
│
├── .streamlit/
│   └── config.toml                                    # High-performance server &amp; theme settings
│
├── README.md                                          # GitHub project landing documentation
├── requirements.txt                                   # Python dependencies
├── run_app.py                                         # Root launcher convenience script
├── generate_docx_report.py                            # Academic Word report builder
├── DNA_Sequence_Similarity_Checker_Project_Report.docx # Editable Word report file
├── ProjectExplanation.html                            # Complete masterclass documentation &amp; Viva guide
├── generate_explanation_html.py                       # Master documentation generator script
│
├── docs/
│   ├── DNA_Sequence_Similarity_Checker_Project_Report.docx
│   └── ProjectExplanation.html
│
└── dna_similarity_checker/                            # Primary application package
    ├── .streamlit/
    │   └── config.toml                                # Package-level Streamlit settings
    ├── app.py                                         # Streamlit user interface &amp; dashboard
    ├── sequence_utils.py                              # Biopython FASTA parser &amp; computational logic
    ├── visualization.py                               # Matplotlib charts &amp; HTML alignment view
    ├── test_checker.py                                # Automated unit test suite (8 tests)
    ├── requirements.txt                               # Package dependencies
    ├── README.md                                      # Sub-package readme
    ├── ProjectExplanation.html                        # Local copy of masterclass docs
    │
    └── sample_data/                                   # Pre-loaded FASTA test cases
        ├── seq1.fasta                                 # 12 nt reference sequence
        ├── seq2.fasta                                 # 12 nt variant sequence
        ├── hba_normal.fasta                           # Human Normal Beta-Globin (Codons 4-9)
        └── hbs_sickle.fasta                           # Human Sickle Beta-Globin (Codon 6 Mutation)</code></pre>
            </div>
        </section>

        <!-- SECTION 5: Code Dependencies -->
        <section id="dependencies">
            <h2 class="section-heading">📦 5. Code Dependencies & Library Ecosystem</h2>
            <div class="doc-card">
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Package</th>
                            <th>Role in Project</th>
                            <th>Why This Library Was Selected</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>streamlit &gt;= 1.30.0</code></td>
                            <td>Interactive Web Interface</td>
                            <td>Provides reactive state, native metric cards, multi-page layout, and file downloaders without frontend framework complexity.</td>
                        </tr>
                        <tr>
                            <td><code>biopython &gt;= 1.80</code></td>
                            <td>Bioinformatics Sequence Ingestion</td>
                            <td>Industry standard for biological formats. Provides <code>Bio.SeqIO</code> for safe FASTA parsing and sequence handling.</td>
                        </tr>
                        <tr>
                            <td><code>matplotlib &gt;= 3.7.0</code></td>
                            <td>Data Visualization</td>
                            <td>Generates publication-quality charts (Bar charts, Donut charts, and Positional tracks) using non-interactive Agg backends.</td>
                        </tr>
                        <tr>
                            <td><code>pandas &gt;= 2.0.0</code></td>
                            <td>Tabular Data Manipulation</td>
                            <td>Powers structured position-by-position inspection tables and rapid CSV generation.</td>
                        </tr>
                        <tr>
                            <td><code>python-docx &gt;= 1.2.0</code></td>
                            <td>Academic Report Generation</td>
                            <td>Enables programmatic creation of stylized Microsoft Word (.docx) project reports with tables, colors, and margins.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- SECTION 6: Methods & Functionality -->
        <section id="methods">
            <h2 class="section-heading">⚙️ 6. Code Walkthrough: Methods & Functionality</h2>

            <!-- sequence_utils.py -->
            <h3 class="sub-heading">Module: sequence_utils.py</h3>

            <div class="method-block">
                <div class="method-header">
                    <span class="method-name">clean_sequence(raw_sequence: str) -&gt; str</span>
                    <span class="method-file">sequence_utils.py</span>
                </div>
                <div class="method-body">
                    <p><strong>Purpose:</strong> Prepares user input by removing all whitespace, tabs, carriage returns, and newlines, and converting characters to uppercase.</p>
                    <pre><code>def clean_sequence(raw_sequence: str) -> str:
    if not raw_sequence:
        return ""
    return "".join(raw_sequence.split()).upper()</code></pre>
                </div>
            </div>

            <div class="method-block">
                <div class="method-header">
                    <span class="method-name">validate_dna_sequence(sequence: str, allow_n: bool = True) -&gt; Tuple[bool, List[str]]</span>
                    <span class="method-file">sequence_utils.py</span>
                </div>
                <div class="method-body">
                    <p><strong>Purpose:</strong> Validates that the input strictly contains allowed DNA nucleotides. Identifies invalid symbols and their exact 1-based positions.</p>
                    <pre><code>def validate_dna_sequence(sequence: str, allow_n: bool = True) -> Tuple[bool, List[str]]:
    if not sequence:
        return False, ["Sequence is empty. Please enter at least one nucleotide (A, T, G, C)."]
    allowed = {"A", "T", "G", "C", "N"} if allow_n else {"A", "T", "G", "C"}
    invalid_positions = [(idx, char) for idx, char in enumerate(sequence, start=1) if char not in allowed]
    if invalid_positions:
        # Returns diagnostic message specifying invalid character & position
        return False, [f"Invalid character(s) detected: ..."]
    return True, []</code></pre>
                </div>
            </div>

            <div class="method-block">
                <div class="method-header">
                    <span class="method-name">parse_fasta(file_or_text: Any) -&gt; Tuple[bool, str, str, str]</span>
                    <span class="method-file">sequence_utils.py</span>
                </div>
                <div class="method-body">
                    <p><strong>Purpose:</strong> Ingests uploaded FASTA files using Biopython's <code>SeqIO.parse</code>. Safely handles strings or byte streams, extracting sequence IDs and clean sequences.</p>
                    <pre><code>def parse_fasta(file_or_text: Any) -> Tuple[bool, str, str, str]:
    # Wraps input in io.StringIO and delegates parsing to Bio.SeqIO
    records = list(SeqIO.parse(stream, "fasta"))
    if not records:
        return False, "", "", "No valid FASTA records found."
    return True, records[0].id, clean_sequence(str(records[0].seq)), ""</code></pre>
                </div>
            </div>

            <div class="method-block">
                <div class="method-header">
                    <span class="method-name">calculate_positional_similarity(seq1: str, seq2: str) -&gt; Dict[str, Any]</span>
                    <span class="method-file">sequence_utils.py</span>
                </div>
                <div class="method-body">
                    <p><strong>Purpose:</strong> Compares nucleotides index-by-index, pads unequal sequences with trailing <code>-</code> gaps, calculates match percentages, and classifies results into interpretation categories.</p>
                </div>
            </div>

            <!-- visualization.py -->
            <h3 class="sub-heading">Module: visualization.py</h3>

            <div class="method-block">
                <div class="method-header">
                    <span class="method-name">plot_comparison_barchart(stats: Dict[str, Any]) -&gt; plt.Figure</span>
                    <span class="method-file">visualization.py</span>
                </div>
                <div class="method-body">
                    <p><strong>Purpose:</strong> Generates a high-DPI bar chart showing the frequency and percentage of Matches, Mismatches, and Gaps.</p>
                </div>
            </div>

            <div class="method-block">
                <div class="method-header">
                    <span class="method-name">plot_similarity_donut(stats: Dict[str, Any]) -&gt; plt.Figure</span>
                    <span class="method-file">visualization.py</span>
                </div>
                <div class="method-body">
                    <p><strong>Purpose:</strong> Generates a circular donut chart with a large central percentage display of overall similarity.</p>
                </div>
            </div>

            <div class="method-block">
                <div class="method-header">
                    <span class="method-name">plot_position_track(comparison_rows: List[Dict[str, Any]]) -&gt; plt.Figure</span>
                    <span class="method-file">visualization.py</span>
                </div>
                <div class="method-body">
                    <p><strong>Purpose:</strong> Generates a linear $5' \to 3'$ barcode track displaying where matches and mutations occur across the sequence length.</p>
                </div>
            </div>

            <div class="method-block">
                <div class="method-header">
                    <span class="method-name">render_html_sequence_alignment(...) -&gt; str</span>
                    <span class="method-file">visualization.py</span>
                </div>
                <div class="method-body">
                    <p><strong>Purpose:</strong> Creates custom HTML/CSS markup with green, red, and grey nucleotide boxes, alignment symbols, and position rulers.</p>
                </div>
            </div>
        </section>

        <!-- SECTION 7: Viva Voce Questions & Answers -->
        <section id="viva">
            <h2 class="section-heading">🎓 7. Comprehensive Viva Voce Questions & Answers</h2>
            <p>25 high-yield examination and oral viva questions categorized by subject area:</p>

            <!-- BioPython Category -->
            <h3 class="sub-heading">Part A: Biopython Concepts</h3>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-bio">Biopython</span> Q1: What is Biopython and what are its primary modules?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> Biopython is an open-source collection of non-commercial Python tools for computational molecular biology. Key modules include:
                    <ul style="margin-left: 20px; margin-top: 6px;">
                        <li><code>Bio.Seq</code>: Representation of biological sequences with molecular methods (transcribe, translate, reverse_complement).</li>
                        <li><code>Bio.SeqIO</code>: Standardized interface for reading and writing biological file formats (FASTA, GenBank, EMBL, FASTQ).</li>
                        <li><code>Bio.Align</code>: Sequence alignment algorithms and scoring matrices.</li>
                        <li><code>Bio.PDB</code>: Parsing and manipulating 3D macromolecular structures.</li>
                    </ul>
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-bio">Biopython</span> Q2: What is the difference between SeqIO.parse() and SeqIO.read()?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong>
                    <ul>
                        <li><code>SeqIO.parse()</code> returns an <strong>iterator</strong> yielding <code>SeqRecord</code> objects. It is designed for files that may contain <em>multiple</em> records (or large multi-FASTA datasets), preventing memory exhaustion.</li>
                        <li><code>SeqIO.read()</code> assumes the file contains <strong>exactly one</strong> record and returns a single <code>SeqRecord</code>. If the file is empty or contains more than one record, it raises a <code>ValueError</code>. In our project, we use <code>SeqIO.parse()</code> for safety.</li>
                    </ul>
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-bio">Biopython</span> Q3: What is a SeqRecord object in Biopython?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> A <code>SeqRecord</code> object encapsulates both the biological sequence (as a <code>Seq</code> object) and its associated biological metadata:
                    <ul style="margin-left: 20px; margin-top: 6px;">
                        <li><code>.seq</code>: The raw sequence string wrapped in a <code>Seq</code> instance.</li>
                        <li><code>.id</code>: The primary identifier (e.g., accession number or FASTA header title).</li>
                        <li><code>.description</code>: The full definition line from the header.</li>
                        <li><code>.annotations</code>: A dictionary of supplementary metadata.</li>
                    </ul>
                </div>
            </div>

            <!-- Algorithm Category -->
            <h3 class="sub-heading">Part B: Algorithm & Computational Methodology</h3>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-algo">Algorithm</span> Q4: Explain the mathematical formula used for calculating similarity in this project.</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong>
                    $$\text{Similarity (\%)} = \left( \frac{\text{Matches}}{\max(\text{Length}(S_1), \text{Length}(S_2))} \right) \times 100$$
                    By dividing by $\max(L_1, L_2)$, we penalize unequal sequence lengths. Any trailing nucleotides that exist in the longer sequence but not in the shorter sequence are treated as missing gaps and counted as non-matches.
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-algo">Algorithm</span> Q5: What is the Time and Space Complexity of your comparison algorithm?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong>
                    <ul>
                        <li><strong>Time Complexity:</strong> $O(N)$ where $N = \max(L_1, L_2)$. We iterate through the sequences exactly once in a single loop.</li>
                        <li><strong>Space Complexity:</strong> $O(N)$ auxiliary space to store padded sequences and the comparison dictionary rows for table rendering.</li>
                    </ul>
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-algo">Algorithm</span> Q6: What is a frameshift mutation, and how does it affect positional similarity?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> A frameshift mutation occurs when an insertion or deletion of nucleotides occurs that is not divisible by three, disrupting the triplet reading frame of codons.
                    In a positional comparison engine, a single 1-base insertion at position 1 will shift all downstream characters, causing virtually every downstream position to register as a mismatch—even if the sequence is 99% identical biologically. This demonstrates why advanced sequence alignment (Needleman-Wunsch / BLAST) uses dynamic programming gap insertion.
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-algo">Algorithm</span> Q7: How does this simple comparison differ from Needleman-Wunsch and Smith-Waterman?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong>
                    <ul>
                        <li><strong>Positional Comparison:</strong> Strictly compares index $i$ to $i$ with no gap insertion ($O(N)$ linear time).</li>
                        <li><strong>Needleman-Wunsch (Global Alignment):</strong> Dynamically inserts gaps to find the maximum possible alignment score across the entire length of both sequences ($O(N \times M)$).</li>
                        <li><strong>Smith-Waterman (Local Alignment):</strong> Identifies the highest-scoring local matching sub-region, ignoring mismatched flanking regions ($O(N \times M)$).</li>
                    </ul>
                </div>
            </div>

            <!-- Biology Category -->
            <h3 class="sub-heading">Part C: Molecular Biology & Genetics</h3>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-concept">Genetics</span> Q8: What is GC Content and why is it biologically significant?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> GC content is the percentage of nitrogenous bases in a DNA molecule that are either Guanine (G) or Cytosine (C).
                    Because G-C pairs are bound by <strong>three hydrogen bonds</strong> while A-T pairs are bound by only <strong>two</strong>, DNA with higher GC content has a higher melting temperature ($T_m$), higher thermal stability, and is frequently enriched in gene-dense genomic regions.
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-concept">Genetics</span> Q9: What does the 'N' character represent in a DNA sequence?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> Under IUPAC nucleotide nomenclature, <code>'N'</code> stands for <em>aNy nucleotide</em> (A, T, G, or C). It indicates an ambiguous or undetermined base where automated sequencing machinery (such as Illumina or Sanger base-calling) could not resolve the exact base with high confidence.
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-concept">Genetics</span> Q10: What is a Single Nucleotide Polymorphism (SNP)?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> A Single Nucleotide Polymorphism (SNP) is a variation at a single genomic nucleotide position that occurs in a significant portion of a population (typically $>1\%$). SNPs are the most common type of genetic variation among humans and serve as biological markers for disease risk and drug response.
                </div>
            </div>

            <!-- Code & Implementation Category -->
            <h3 class="sub-heading">Part D: Python & Streamlit Implementation</h3>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-code">Code</span> Q11: Why did you set matplotlib.use('Agg') in visualization.py?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> By default, Matplotlib attempts to open an interactive GUI window (such as Tkinter or Qt). In web servers and Streamlit applications, this triggers threading collisions or GUI crashes. <code>matplotlib.use('Agg')</code> forces Matplotlib to use the non-interactive Anti-Grain Geometry backend, which writes directly to memory buffers safely.
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-code">Code</span> Q12: How does Streamlit preserve state when switching between sidebar pages?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> We use Streamlit's <code>st.session_state</code> dictionary. Keys such as <code>st.session_state.last_results</code>, <code>seq1_input</code>, and <code>seq2_input</code> persist across script reruns, allowing users to view the comparison, switch to the analytics page, and export data without having to recompute.
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-code">Code</span> Q13: How do you handle non-UTF8 or corrupted FASTA files?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> In <code>sequence_utils.parse_fasta()</code>, we decode incoming bytes using <code>errors='replace'</code> to prevent decode exceptions on corrupt bytes, wrap the decoded text in <code>io.StringIO</code>, and use a <code>try-except</code> block to catch and report formatting exceptions gracefully.
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-code">Code</span> Q14: How are unit tests structured in test_checker.py?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> <code>test_checker.py</code> defines 8 modular test functions using standard Python <code>assert</code> statements:
                    <ol style="margin-left: 20px; margin-top: 6px;">
                        <li>Prompt benchmark case (12 nt, 1 mismatch = 91.67%).</li>
                        <li>Unequal sequence length gap padding.</li>
                        <li>Case-insensitivity and whitespace stripping.</li>
                        <li>Detection of invalid characters (e.g., <code>X, Y, Z, 1, 2</code>).</li>
                        <li>Empty sequence validation.</li>
                        <li>Biopython FASTA parsing from string buffers.</li>
                        <li>Matplotlib figure and HTML alignment generation.</li>
                        <li>Plain-text report formatting.</li>
                    </ol>
                </div>
            </div>

            <div class="accordion-item">
                <div class="accordion-header">
                    <span><span class="viva-badge badge-code">Code</span> Q15: How can this application be extended in the future?</span>
                    <span class="accordion-icon">+</span>
                </div>
                <div class="accordion-body">
                    <strong>Answer:</strong> Future extensions could include:
                    <ul style="margin-left: 20px; margin-top: 6px;">
                        <li>Implementing dynamic programming global alignment (Needleman-Wunsch) with customizable gap penalties.</li>
                        <li>Supporting protein amino acid sequence comparison using BLOSUM62 and PAM250 substitution matrices.</li>
                        <li>Adding 6-frame in-silico translation to show the effect of DNA mutations on amino acid sequences.</li>
                        <li>Multiple Sequence Alignment (MSA) for comparing 3 or more homologous genes simultaneously.</li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- SECTION 8: Execution & Verification -->
        <section id="run-guide">
            <h2 class="section-heading">🚀 8. Execution & Verification Guide</h2>
            <div class="doc-card">
                <h3 class="sub-heading">Clone & Run Commands</h3>
                <pre><code># 1. Clone the repository
git clone https://github.com/ayushtech874-stack/bioPython_project.git

# 2. Enter directory
cd bioPython_project

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run automated test suite
python dna_similarity_checker/test_checker.py

# 5. Launch the Streamlit Web Application
python run_app.py</code></pre>

                <h3 class="sub-heading">Expected Benchmark Output</h3>
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Parameter</th>
                            <th>Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Sequence 1</td><td><code>ATGCGTACGTAG</code></td></tr>
                        <tr><td>Sequence 2</td><td><code>ATGCGTTCGTAG</code></td></tr>
                        <tr><td>Sequence 1 Length</td><td>12 nt</td></tr>
                        <tr><td>Sequence 2 Length</td><td>12 nt</td></tr>
                        <tr><td>Matching Positions</td><td><strong>11</strong></td></tr>
                        <tr><td>Mismatching Positions</td><td><strong>1</strong> (Position 7: A &rarr; T)</td></tr>
                        <tr><td>Gaps</td><td>0</td></tr>
                        <tr><td>Similarity Percentage</td><td><strong>91.67%</strong></td></tr>
                        <tr><td>Interpretation</td><td>Very High Positional Similarity</td></tr>
                    </tbody>
                </table>
            </div>
        </section>
    </main>
</div>

<script>
    // Accordion toggle behavior
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', () => {
            const item = header.parentElement;
            item.classList.toggle('active');
        });
    });
</script>
</body>
</html>
"""

def main():
    target_path = "ProjectExplanation.html"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Successfully generated {target_path} ({len(HTML_CONTENT)} bytes)")

if __name__ == "__main__":
    main()
