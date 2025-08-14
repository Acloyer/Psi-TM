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

## v0.8.3: L_k (Pointer-Chase)

**Language Definition:** Pointer-chase through k function tables $T_1,\ldots,T_k:[m]\to[m]$ with tail predicate $b:[m]\to\{0,1\}$

**Core Results:**
- **UB:** Depth-k algorithm in $O(n)$ time, $O(\log_{2} n)$ space  
- **LB:** Depth-$(k{-}1)$ requires $\Omega\!\big(n/(k(k{-}1)\log_{2} n)\big)$ time via Budget/Fooling
- **Separation:** First combat-ready depth hierarchy result in restricted regime

**Proof Chain (ASCII Diagram):**
```
Fooling Family |F_n| = 2^{αm} 
       ↓
Ψ-Fooling Bound: T ≥ log₂|F_n|/B(k-1,n)
       ↓  
Budget: B(k-1,n) = c(k-1)log₂ n
       ↓
Size: m = Θ(n/k) 
       ↓
Result: T = Ω(n/(k(k-1)log₂ n))
```

**Integration:** Section integrated into `main.tex` via `\input{psi-tm-08-3-lk-pointer-chase}` for arXiv submission

**Artifacts:** 
- `psi-tm-08-3-lk-pointer-chase.tex` - LaTeX section for inclusion in main.tex (NOT standalone)
- `lean/Lk_LB_Skeleton.lean` - Formal statement skeleton  
- `notebooks/lk_pointer_chase.ipynb` - Empirical validation with $\log_{2} M$ trend analysis
- `paper/fig/lk_logM.png` - Generated plot showing linear $\alpha m$ bound (already present)

**Build:** 
- `make all` - Full paper compilation via main.tex (requires LaTeX, Jupyter, Lean 4)
- `make arxiv-check` - Verify arXiv submission readiness
- **Main document:** `main.tex` (all sections integrated via \input)

**arXiv Notes:** All cross-references work from main.tex context. Labels namespaced with "Lk:" prefix.

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

## v0.8.4: L_k^{phase} (Phase-Locked Access)

**Language Definition:** k-phase computation where snapshot $S_j$ accessible only via $\iota_j$ interface, enforcing strict phase-lock separation

**Core Innovation:** **Transcript Collision Lemma** - formalizes that without $\iota_k$ access, all transcripts are identical regardless of $S_k$ content

**Core Results:**
- **UB:** Depth-k algorithm in $O(n)$ time, $O(\log m)$ space using phase-sequential access
- **LB:** Depth-$(k{-}1)$ requires $\Omega\!\big(n/(k(k{-}1)\log_{2} n)\big)$ time via phase-lock constraint
- **Separation Mechanism:** Information-theoretic blindness without appropriate $\iota_j$ interface

**Phase-Lock Chain (ASCII Diagram):**
Phase Snapshots: S_1,...,S_{k-1},S_k
\u2193
Access Control: S_j only via \iota_j
\u2193
Depth k-1: Cannot access S_k (missing \iota_k)
\u2193
Transcript Collision: Identical until phase k
\u2193
Fooling Family: |F_n| = 2^{\alpha m \ell} via S_k variation
\u2193
Result: T = \Omega(n/(k(k-1)log₂ n))

**Key Lemma:** \emph{Transcript Collision Lemma} - Any depth-$(k{-}1)$ algorithm produces identical transcripts on instances differing only in $S_k$, while acceptance differs

**Integration:** Section integrated into `main.tex` via `\input{psi-tm-08-4-lkphase-phase-access}` for arXiv submission

**Artifacts:**
- `psi-tm-08-4-lkphase-phase-access.tex` - LaTeX section with phase-lock formalization
- `lean/Lkphase_Transcript_Skeleton.lean` - Formal transcript collision statement
- `notebooks/lkphase_transcript_analysis.ipynb` - Empirical phase-lock demonstration
- `fig/lkphase_transcript.png` - Transcript collision visualization

**Build:**
- `make all` - Build verification (LaTeX compilation manual)
- `make arxiv-check` - Verify arXiv submission readiness including transcript lemma
- **Main document:** `main.tex` (all sections integrated via \input)

**arXiv Notes:** All cross-references work from main.tex context. Labels namespaced with "Lkphase:" prefix. Core acceptance criterion: single lemma formalizing transcript collision mechanism.

**Figure Interpretation:**
- **Left Panel:** Phase access pattern showing interface-based restriction ($\iota_1,\ldots,\iota_{k-1}$ accessible, $\iota_k$ blocked)
- **Right Panel:** Transcript collision demonstration (identical hashes, different outcomes)
- **Core Insight:** Information-theoretic separation via computational access constraints

**Visualization Details:**
- Each data point represents a problem instance differing only in $S_k(q)$
- Transcript hashes identical across instances (horizontal clustering)
- Acceptance outcomes differ via $f(v_1,\ldots,v_k)$ despite identical transcripts
- Demonstrates phase-lock as fundamental separation primitive

## v0.8.4: L_k^{phase} (Phase-Locked Access) - Research Impact

**Methodological Innovation:** Introduces **phase-locked access** as a novel separation technique in computational complexity theory. Unlike traditional diagonalization, this method uses interface accessibility constraints to create information-theoretic barriers.

**Theoretical Contributions:**
- **Interface-Based Separation:** S_j accessible only via ι_j creates natural computational hierarchy
- **Transcript Collision Mechanism:** Formal characterization of identical transcripts with different outputs  
- **Information-Theoretic Foundation:** Bridges information theory and computational complexity

**Research Significance:**
- **New Separation Tool:** Phase-locking applicable to other computational models
- **Practical Relevance:** Natural connection to distributed computing and secure protocols
- **Theoretical Depth:** Establishes interface constraints as fundamental separation primitive

**Future Applications:**
- Quantum computational models with restricted access
- Circuit complexity with hierarchical constraints  
- Interactive proof systems with phase separation
- Secure multi-party computation protocol design

## v0.8.5: Anti-Simulation Hook

**Core Innovation:** **No-Poly-Simulation Theorem** - quantitative proof that depth k-1 cannot simulate `\iota_k` calls using polynomially-many `\iota_{k-1}` calls without violating Budget Lemma

**Attack Model:** Depth-(k-1) algorithm attempts to simulate single `\iota_k` call using s = n^\beta calls to `\iota_{k-1}`

**Core Results:**
- **No-Poly-Simulation:** Simulation requires $n^{\beta}$ budget but only $O(\log_{2} n)$ allocated; violation whenever $\displaystyle \beta \geq \frac{\log_{2}(k/(k-1))}{\log_{2} n}$
- **Failure Mode Analysis:** Exhaustive enumeration of potential bypass methods and why each is blocked
- **Quantitative Barrier:** Exponential gap between required vs. allocated simulation budget

**Anti-Simulation Chain (ASCII Diagram):**
```
Simulation Attempt: s = n^β calls to ι_{k-1}
         ↓
Budget Required: s·B(k-1,n) = n^β·c·(k-1)·log₂ n
         ↓
Budget Allocated: B(k-1,n) = c·(k-1)·log₂ n
         ↓
Violation iff: β ≥ log₂(k/(k-1)) / log₂ n
         ↓
Contradiction: Polynomial requirement vs logarithmic allocation
```

**Failure Modes Blocked:**
1. **Super-logarithmic budget:** Violates B(d,n) = O(\log n) constraint
2. **Randomized simulation:** Violates deterministic requirement  
3. **Advice mechanism:** Violates no-advice constraint
4. **Multi-pass access:** Violates one-pass constraint

**Hook Integration:** Reinforces LB proofs from v0.8.3-v0.8.4 by eliminating primary escape route for depth-(k-1) algorithms

**Quantitative Guarantee:** Even with unlimited ingenuity in payload design, fundamental budget constraints prevent simulation

**Integration:** Section integrated into `main.tex` via `\input{psi-tm-08-5-anti-simulation-hook}` for arXiv submission

**Artifacts:**
- `psi-tm-08-5-anti-simulation-hook.tex` - LaTeX section with quantitative no-simulation proof
- `lean/AntiSim_Hook_Skeleton.lean` - Formal anti-simulation statement with failure mode analysis
- `notebooks/anti_simulation_analysis.ipynb` - Empirical budget violation demonstration  
- `fig/anti_simulation_budget.png` - Budget gap visualization showing exponential barrier

**Build:**
- `make all` - Build verification (LaTeX compilation manual)
- `make arxiv-check` - Verify arXiv submission readiness including failure mode analysis
- **Main document:** `main.tex` (all sections integrated via \input)

**arXiv Notes:** All cross-references work from main.tex context. Labels namespaced with "AntiSim:" prefix. Core acceptance criterion: clear quantitative statement with dependency graph showing LB hook integration.