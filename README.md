# Psi-TM: File-Aware Work Order with Minimal Introspection

## Project Overview

This repository contains a complete LaTeX project for the Psi-TM (Psi-Turing Machine) paper, prepared for arXiv submission. The paper presents a computational model that extends standard Turing machines with minimal introspection capabilities limited to constant depth.

## Key Results

### Main Theorem: Strict Hierarchy
For each $k \geq 1$, we prove $\text{Psi-TM}_k \subsetneq \text{Psi-TM}_{k+1}$

### Complexity Barrier Analysis
- **Relativization**: requires $k \geq 1$ (proven oracle-relative)
- **Natural Proofs**: requires $k \geq 2$ (partial/conditional)
- **Proof Complexity**: requires $k \geq 2$ (partial/conditional)
- **Algebraization**: requires $k \geq 3$ (open/conservative)

### Explicit Constructions
- Languages $L_k$ that separate each level of the hierarchy
- Information-theoretic lower bounds through adversary arguments
- Structural depth analysis and pattern recognition

## Project Structure

### Main Document
- **main.tex** - Complete LaTeX document with all packages, theorem environments, and content inclusion

### Content Files (included via \input{})
- **psi-tm-formal-definition.tex** - Formal definitions of Psi-TM model and structural depth
- **psi-tm-barrier-minimality.tex** - Analysis of minimal introspection requirements for complexity barriers
- **psi-tm-k-hierarchy.tex** - Proof of strict hierarchy based on introspection depth
- **psi-tm-theoretical-results.tex** - Theoretical results and complexity analysis
- **psi-tm-stoc-focs.tex** - STOC/FOCS results and oracle-relative separations

### Documentation
- **MANIFEST.md** - Detailed file structure and purpose documentation
- **README.md** - This file with setup and usage instructions

## arXiv Submission Requirements

### Package Policy
- **Allowed**: geometry, amsmath, amssymb, amsthm, mathtools, microtype, graphicx, hyperref, booktabs, url, enumitem, xcolor, cleveref
- **Forbidden**: fontspec, unicode-math, polyglossia, minted, pygments, tikz externalization, shellesc, write18

### Encoding Requirements
- ASCII only - no Unicode code points
- All mathematical symbols via TeX macros (e.g., \Psi, \pi, \subsetneq, \to)
- All math wrapped in $...$ or \[...\]

### Structure Requirements
- Single preamble in main.tex only
- All content files included via \input{}
- Pure content in subfiles (no packages, macros, or document environments)

## Setup Instructions

### Prerequisites
- LaTeX distribution (TeX Live, MiKTeX, or similar)
- pdfLaTeX compiler (no shell-escape required)

### Compilation
```bash
# Basic compilation
pdflatex main.tex

# For bibliography (if using BibTeX)
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Clean auxiliary files
rm *.aux *.log *.out *.toc *.bbl *.blg
```

### Verification
After compilation, verify:
1. No "Missing $ inserted" errors
2. All mathematical symbols render correctly
3. All cross-references work properly
4. PDF generates without errors

## Content Organization

### Section 1: Formal Definitions
- Psi-TM model definition
- Structural depth concepts
- Introspection functions and selectors

### Section 2: Complexity Barriers
- Relativization barrier analysis
- Natural proofs barrier requirements
- Proof complexity considerations
- Algebraization barrier status

### Section 3: k-Hierarchy
- Strict separation proof
- Explicit language constructions
- Information-theoretic lower bounds

### Section 4: Theoretical Results
- Complexity class relationships
- Connection to classical classes
- Structural pattern analysis

### Section 5: STOC/FOCS Results
- Oracle-relative separations
- Formal adversary arguments
- Conservative barrier statements

## Key Definitions

### Psi-TM Model
A Psi-TM with introspection depth $k$ is a 7-tuple:
$$M_\Psi^k = (Q, \Sigma, \Gamma, \delta, q_0, F, \iota_k)$$

### Structural Depth
For a string $w \in \{0,1\}^*$:
$$d(w) = \min_{T_w} \text{depth}(T_w)$$

### Information Budget
Each introspection call returns at most $B(k,n)$ bits, where $B(k,n)$ is the information budget function.

## Citation and Attribution

**Copyright (c) 2025 Rafig Huseynzade. All Rights Reserved.**
**Licensed under CC BY-NC-ND 4.0**

This work presents original research on computational complexity theory and the relationship between introspection depth and computational capability in formal automata theory.

## Contact and Support

For questions about the technical content or LaTeX compilation, please refer to the documentation or contact the research team.

---

**Note**: This project is prepared for arXiv submission and follows all arXiv requirements for LaTeX documents, including package restrictions, encoding requirements, and structural guidelines.