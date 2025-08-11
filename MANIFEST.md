# Psi-TM LaTeX Project Manifest

## Project Overview
This is a LaTeX project for the Psi-TM (Psi-Turing Machine) paper, prepared for arXiv submission. The paper presents a computational model that extends standard Turing machines with minimal introspection capabilities.

## File Structure

### Main Document
- **main.tex** - Main LaTeX document with all packages, theorem environments, and content inclusion

### Content Files (included via \input{})
- **psi-tm-formal-definition.tex** - Formal definitions of Psi-TM model and structural depth
- **psi-tm-barrier-minimality.tex** - Analysis of minimal introspection requirements for complexity barriers
- **psi-tm-k-hierarchy.tex** - Proof of strict hierarchy based on introspection depth
- **psi-tm-theoretical-results.tex** - Theoretical results and complexity analysis
- **psi-tm-stoc-focs.tex** - STOC/FOCS results and oracle-relative separations

## Key Features

### arXiv Compliance
- Single preamble in main.tex only
- ASCII-only content with TeX symbols (no Unicode)
- Standard LaTeX packages compatible with arXiv
- No shell-escape or external dependencies

### Mathematical Content
- Complete formalization of Psi-TM model
- Proof of strict hierarchy: Psi-TM_k \subsetneq Psi-TM_{k+1}
- Analysis of complexity barrier bypass requirements
- Information-theoretic lower bounds via adversary arguments

### Structure
- All theorem environments defined in main.tex
- Global macros for consistent notation
- Proper cross-referencing and bibliography
- Professional academic formatting

## Compilation
To compile the document:
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Target
This paper is prepared for arXiv submission and follows arXiv's LaTeX requirements for computational complexity theory papers. 