# Psi-TM: File-Aware Work Order with Minimal Introspection

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Key Results](#key-results)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Research Contributions](#research-contributions)
- [Setup & Compilation](#setup--compilation)
- [arXiv Submission](#arxiv-submission)
- [Documentation](#documentation)

## 🎯 Project Overview

This repository contains a complete LaTeX project for the **Psi-TM (Psi-Turing Machine)** paper, prepared for arXiv submission. The paper presents a computational model that extends standard Turing machines with minimal introspection capabilities limited to constant depth.

### What is Psi-TM?
Psi-TM is a novel computational model that introduces **introspection depth** as a fundamental complexity parameter. Unlike traditional Turing machines, Psi-TMs can examine their own computation history through introspection functions, but with strict depth limitations that create natural computational hierarchies.

## 🏆 Key Results

### Main Theorem: Strict Hierarchy
For each $k \geq 1$, we prove $\text{Psi-TM}_k \subsetneq \text{Psi-TM}_{k+1}$

### Complexity Barrier Analysis
| Barrier | Minimum Depth | Status |
|---------|---------------|---------|
| **Relativization** | $k \geq 1$ | ✅ Proven oracle-relative |
| **Natural Proofs** | $k \geq 2$ | 🔄 Partial/conditional |
| **Proof Complexity** | $k \geq 2$ | 🔄 Partial/conditional |
| **Algebraization** | $k \geq 3$ | ❓ Open/conservative |

### Explicit Constructions
- **Languages $L_k$** that separate each level of the hierarchy
- **Information-theoretic lower bounds** through adversary arguments
- **Structural depth analysis** and pattern recognition

## 🚀 Quick Start

### Prerequisites
```bash
# Required software
- LaTeX distribution (TeX Live, MiKTeX, or similar)
- pdfLaTeX compiler (no shell-escape required)
- Python 3.7+ (for notebooks)
- Lean 4 (for formal verification)
```

### Basic Compilation
```bash
# Clone and navigate to project
git clone <repository-url>
cd Psi-TM

# Basic compilation
pdflatex main.tex

# Full compilation with bibliography
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Clean auxiliary files
make clean
```

### Verification
```bash
# Check arXiv submission readiness
make arxiv-check

# Run all builds and tests
make all
```

## 📁 Project Structure

```
Psi-TM/
├── 📄 main.tex                    # Main LaTeX document
├── 📁 paper/                      # Core content sections
│   ├── psi-tm-formal-definition.tex
│   ├── psi-tm-barrier-minimality.tex
│   ├── psi-tm-k-hierarchy.tex
│   ├── psi-tm-theoretical-results.tex
│   └── psi-tm-stoc-focs.tex
├── 📁 v0.8.3-lk-pointer-chase/    # Pointer-chase separation
├── 📁 v0.8.4-lkphase-phase-access/ # Phase-locked access
├── 📁 v0.8.5-anti-simulation-hook/ # Anti-simulation hook
├── 📁 lean/                       # Formal verification
├── 📁 notebooks/                  # Empirical analysis
├── 📁 fig/                        # Generated figures
└── 📁 scripts/                    # Build and analysis scripts
```

### Content Files (included via \input{})
- **`psi-tm-formal-definition.tex`** - Formal definitions of Psi-TM model and structural depth
- **`psi-tm-barrier-minimality.tex`** - Analysis of minimal introspection requirements for complexity barriers
- **`psi-tm-k-hierarchy.tex`** - Proof of strict hierarchy based on introspection depth
- **`psi-tm-theoretical-results.tex`** - Theoretical results and complexity analysis
- **`psi-tm-stoc-focs.tex`** - STOC/FOCS results and oracle-relative separations

## 🔬 Research Contributions

### v0.8.3: L_k (Pointer-Chase)

**Language Definition:** Pointer-chase through k function tables $T_1,\ldots,T_k:[m]\to[m]$ with tail predicate $b:[m]\to\{0,1\}$

**Core Results:**
- **Upper Bound:** Depth-k algorithm in $O(n)$ time, $O(\log_{2} n)$ space  
- **Lower Bound:** Depth-$(k{-}1)$ requires $\Omega\!\big(n/(k(k{-}1)\log_{2} n)\big)$ time via Budget/Fooling
- **Separation:** First combat-ready depth hierarchy result in restricted regime

**Proof Chain:**
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

**Artifacts:** 
- `psi-tm-08-3-lk-pointer-chase.tex` - LaTeX section
- `lean/Lk_LB_Skeleton.lean` - Formal statement skeleton  
- `notebooks/lk_pointer_chase.ipynb` - Empirical validation
- `paper/fig/lk_logM.png` - Generated plot

### v0.8.4: L_k^{phase} (Phase-Locked Access)

**Core Innovation:** **Transcript Collision Lemma** - formalizes that without $\iota_k$ access, all transcripts are identical regardless of $S_k$ content

**Core Results:**
- **Upper Bound:** Depth-k algorithm in $O(n)$ time, $O(\log m)$ space using phase-sequential access
- **Lower Bound:** Depth-$(k{-}1)$ requires $\Omega\!\big(n/(k(k{-}1)\log_{2} n)\big)$ time via phase-lock constraint
- **Separation Mechanism:** Information-theoretic blindness without appropriate $\iota_j$ interface

**Phase-Lock Chain:**
```
Phase Snapshots: S_1,...,S_{k-1},S_k
       ↓
Access Control: S_j only via ι_j
       ↓
Depth k-1: Cannot access S_k (missing ι_k)
       ↓
Transcript Collision: Identical until phase k
       ↓
Fooling Family: |F_n| = 2^{αm ℓ} via S_k variation
       ↓
Result: T = Ω(n/(k(k-1)log₂ n))
```

**Key Lemma:** *Transcript Collision Lemma* - Any depth-$(k{-}1)$ algorithm produces identical transcripts on instances differing only in $S_k$, while acceptance differs

**Artifacts:**
- `psi-tm-08-4-lkphase-phase-access.tex` - LaTeX section
- `lean/Lkphase_Transcript_Skeleton.lean` - Formal transcript collision statement
- `notebooks/lkphase_transcript_analysis.ipynb` - Empirical phase-lock demonstration
- `fig/lkphase_transcript.png` - Transcript collision visualization

### v0.8.5: Anti-Simulation Hook

**Core Innovation:** **No-Poly-Simulation Theorem** - quantitative proof that depth k-1 cannot simulate `\iota_k` calls using polynomially-many `\iota_{k-1}` calls without violating Budget Lemma

**Attack Model:** Depth-(k-1) algorithm attempts to simulate single `\iota_k` call using s = n^β calls to `\iota_{k-1}`

**Core Results:**
- **No-Poly-Simulation:** Simulation requires $n^{\beta}$ budget but only $O(\log_{2} n)$ allocated; violation whenever $\displaystyle \beta \geq \frac{\log_{2}(k/(k-1))}{\log_{2} n}$
- **Failure Mode Analysis:** Exhaustive enumeration of potential bypass methods and why each is blocked
- **Quantitative Barrier:** Exponential gap between required vs. allocated simulation budget

**Anti-Simulation Chain:**
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
1. **Super-logarithmic budget:** Violates B(d,n) = O(log n) constraint
2. **Randomized simulation:** Violates deterministic requirement  
3. **Advice mechanism:** Violates no-advice constraint
4. **Multi-pass access:** Violates one-pass constraint

**Artifacts:**
- `psi-tm-08-5-anti-simulation-hook.tex` - LaTeX section
- `lean/AntiSim_Hook_Skeleton.lean` - Formal anti-simulation statement
- `notebooks/anti_simulation_analysis.ipynb` - Empirical budget violation demonstration  
- `fig/anti_simulation_budget.png` - Budget gap visualization

## ⚙️ Setup & Compilation

### Prerequisites
- **LaTeX distribution** (TeX Live, MiKTeX, or similar)
- **pdfLaTeX compiler** (no shell-escape required)
- **Python 3.7+** (for Jupyter notebooks)
- **Lean 4** (for formal verification)

### Compilation Commands
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

### Makefile Targets
```bash
make all          # Full paper compilation
make clean        # Remove auxiliary files
make arxiv-check  # Verify arXiv submission readiness
make figures      # Generate all figures
make notebooks    # Run all Jupyter notebooks
```

### Verification Checklist
After compilation, verify:
1. ✅ No "Missing $ inserted" errors
2. ✅ All mathematical symbols render correctly
3. ✅ All cross-references work properly
4. ✅ PDF generates without errors
5. ✅ All figures are included
6. ✅ Bibliography is complete

## 📤 arXiv Submission

### Package Policy
| Status | Packages |
|--------|----------|
| ✅ **Allowed** | geometry, amsmath, amssymb, amsthm, mathtools, microtype, graphicx, hyperref, booktabs, url, enumitem, xcolor, cleveref |
| ❌ **Forbidden** | fontspec, unicode-math, polyglossia, minted, pygments, tikz externalization, shellesc, write18 |

### Encoding Requirements
- **ASCII only** - no Unicode code points
- All mathematical symbols via TeX macros (e.g., \Psi, \pi, \subsetneq, \to)
- All math wrapped in $...$ or \[...\]

### Structure Requirements
- Single preamble in main.tex only
- All content files included via \input{}
- Pure content in subfiles (no packages, macros, or document environments)

### Submission Checklist
- [ ] ASCII encoding verified
- [ ] All packages in allowed list
- [ ] Single main.tex file
- [ ] All figures included
- [ ] Bibliography complete
- [ ] Cross-references working
- [ ] No compilation errors

## 📚 Documentation

### Key Definitions

#### Psi-TM Model
A Psi-TM with introspection depth $k$ is a 7-tuple:
$$M_\Psi^k = (Q, \Sigma, \Gamma, \delta, q_0, F, \iota_k)$$

#### Structural Depth
For a string $w \in \{0,1\}^*$:
$$d(w) = \min_{T_w} \text{depth}(T_w)$$

#### Information Budget
Each introspection call returns at most $B(k,n)$ bits, where $B(k,n)$ is the information budget function.

### Content Organization

| Section | Content | File |
|---------|---------|------|
| **1. Formal Definitions** | Psi-TM model, structural depth, introspection functions | `psi-tm-formal-definition.tex` |
| **2. Complexity Barriers** | Relativization, natural proofs, proof complexity, algebraization | `psi-tm-barrier-minimality.tex` |
| **3. k-Hierarchy** | Strict separation proof, explicit language constructions | `psi-tm-k-hierarchy.tex` |
| **4. Theoretical Results** | Complexity class relationships, structural pattern analysis | `psi-tm-theoretical-results.tex` |
| **5. STOC/FOCS Results** | Oracle-relative separations, formal adversary arguments | `psi-tm-stoc-focs.tex` |

### Additional Documentation
- **`MANIFEST.md`** - Detailed file structure and purpose documentation
- **`README-STOC-FOCS.md`** - STOC/FOCS specific documentation
- **`NOTICE`** - Legal notices and licensing information

## 🎓 Research Impact

### Methodological Innovation
- **Phase-locked access** as novel separation technique
- **Interface-based separation** using computational access constraints
- **Information-theoretic foundation** bridging information theory and complexity

### Theoretical Contributions
- **Interface-Based Separation:** $S_j$ accessible only via $\iota_j$ creates natural computational hierarchy
- **Transcript Collision Mechanism:** Formal characterization of identical transcripts with different outputs  
- **Information-Theoretic Foundation:** Bridges information theory and computational complexity

### Future Applications
- Quantum computational models with restricted access
- Circuit complexity with hierarchical constraints  
- Interactive proof systems with phase separation
- Secure multi-party computation protocol design

## 📄 Citation and Attribution

**Copyright (c) 2025 Rafig Huseynzade. All Rights Reserved.**  
**Licensed under CC BY-NC-ND 4.0**

This work presents original research on computational complexity theory and the relationship between introspection depth and computational capability in formal automata theory.

## 🤝 Contact and Support

For questions about:
- **Technical content** - Review the documentation files
- **LaTeX compilation** - Check the setup instructions
- **Research collaboration** - Contact the research team
- **arXiv submission** - Follow the submission checklist

---

**Note**: This project is prepared for arXiv submission and follows all arXiv requirements for LaTeX documents, including package restrictions, encoding requirements, and structural guidelines.