<!-- Copyright (c) 2025 Rafig Huseynzade. All Rights Reserved. -->
<!-- Licensed under CC BY-NC-ND 4.0 -->
<!-- Original work - do not copy without attribution -->

# Psi-TM: Minimal Introspective Computational Model

## Overview

This repository contains the complete mathematical foundation for the **Psi-TM** (Psi-Turing Machine) model, a rigorous continuation of Structurally-Aware Turing Machines (SA-TM). Psi-TM achieves minimal introspection while preserving the ability to bypass complexity barriers, maintaining computational equivalence to standard Turing machines.

## Main Documents

### 1. Formal Definition (`psi-tm-formal-definition.tex`)
- **Core formal definitions** of Psi-TM components and configuration
- **Introspective function** with k-limited constraints
- **Computational equivalence** proofs to standard Turing machines
- **Barrier bypass** examples with complete mathematical proofs
- **Connection to SA-TM** with formal relationship establishment

### 2. Theoretical Results (`psi-tm-theoretical-results.tex`)
- **Complexity class hierarchy** for Psi-P and Psi-PSPACE
- **Strict inclusions** demonstrating power of minimal introspection
- **Efficient simulation** algorithms and universal Psi-TM construction
- **Time and space barrier bypass** with specific problem examples
- **Algorithmic foundations** for Psi-TM implementation

### 3. Barrier Analysis (`psi-tm-barrier-analysis.tex`)
- **Four complexity barriers** analysis: Time, Space, Determinism, Universality
- **Formal connection** to SA-TM framework
- **Minimality proofs** for introspection constraints
- **Optimality results** for k-limited introspection
- **Preservation theorems** for computational power

## Mathematical Achievements

### Formal Definitions
- **Psi-TM Configuration**: $\mathcal{C} = (q, \alpha, \beta, \psi)$
- **Introspective Function**: $\iota: \Gamma^* \times \Gamma^* \times \mathbb{N} \to \Psi$
- **k-Limited Introspection**: $|\iota(\alpha, \beta, k)| \leq f(k)$

### Main Theorems
1. **Computational Equivalence**: Psi-TM equivalent to standard Turing machines
2. **Partial Barrier Bypass**: Problems solvable in Psi-P but not in P for standard machines
3. **Minimality of Introspection**: Preserves equivalence with $k = O(1)$
4. **Class Hierarchy**: $\text{Psi-P}_{k_1} \subseteq \text{Psi-P}_{k_2}$ for $k_1 < k_2$

### Complexity Barrier Bypass
1. **Time Barrier**: Structural Recognition (SR) $\in \text{Psi-DTIME}(n)$ but $\notin \text{DTIME}(o(n^k))$
2. **Space Barrier**: Structural Parsing (SP) $\in \text{Psi-DSPACE}(n)$ but $\notin \text{DSPACE}(o(n^k))$
3. **Determinism Barrier**: Structural Guessing (SG) $\in \text{Psi-DTIME}(n)$ but $\notin \text{DTIME}(o(n^k))$
4. **Universality Barrier**: Polynomial slowdown instead of exponential

## Connection to SA-TM

### Formal Relationship
- Psi-TM is a strict subset of SA-TM
- Introspection limited to constant depth $k = O(1)$
- Preserves barrier bypass capability with minimal introspection

### Capability Comparison
$$\text{SA-TM} \supseteq \text{Psi-TM}_{k_2} \supseteq \text{Psi-TM}_{k_1} \supseteq \text{TM}$$

## Key Features

### Minimal Introspection
- **Constant depth**: $k = O(1)$ introspection limitation
- **Polynomial bounds**: $|\iota(\alpha, \beta, k)| \leq f(k)$ where $f$ is polynomial
- **Efficient simulation**: Standard TM simulation with $O(f(k))$ slowdown

### Computational Power
- **Equivalence preservation**: Maintains TM computational power
- **Barrier bypass**: Achieves SA-TM barrier bypass with minimal introspection
- **Hierarchical structure**: Clear inclusion relationships between complexity classes

### Mathematical Rigor
- **Formal proofs**: Complete mathematical proofs for all theorems
- **Complexity analysis**: Precise time and space complexity bounds
- **Barrier analysis**: Systematic analysis of four complexity barriers

## Document Compilation

To compile the LaTeX documents:

```bash
# Compile main definition document
pdflatex psi-tm-formal-definition.tex

# Compile theoretical results
pdflatex psi-tm-theoretical-results.tex

# Compile barrier analysis
pdflatex psi-tm-barrier-analysis.tex
```

## Authorship

This mathematical work is the original research of **Rafig Huseynzade**, establishing the formal foundations of the Psi-TM model as a continuation of Structurally-Aware Turing Machines.

## License

See the `NOTICE` file for licensing information. 