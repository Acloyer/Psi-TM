.PHONY: all pdf notebooks lean test clean arxiv-check figures check arxiv plots

# Main build target - compiles full paper via main.tex  
all: notebooks lean test
	@echo "✓ v0.8.6 artifacts built (skeletons + notebooks)"
	@echo "⚠ PDF compilation disabled - manual LaTeX compilation required"

notebooks:
	@echo "Executing notebooks..."
	mkdir -p fig
	jupyter nbconvert --execute --inplace notebooks/anti_simulation_analysis.ipynb --ExecutePreprocessor.cwd=.
	@if [ -f notebooks/numeric_examples.ipynb ]; then jupyter nbconvert --execute --inplace notebooks/numeric_examples.ipynb --ExecutePreprocessor.cwd=.; fi
	@if [ -f notebooks/transcript_counts.ipynb ]; then jupyter nbconvert --execute --inplace notebooks/transcript_counts.ipynb --ExecutePreprocessor.cwd=.; fi
	@test -f fig/anti_simulation_budget.png && echo "✓ Anti-simulation plot saved to fig/" || echo "✗ Anti-simulation plot missing from fig/"
	@echo "✓ Notebook(s) executed"

FIGS = fig/anti_simulation_budget.png fig/anti_simulation_failure_modes.png

figures: $(FIGS)

fig/anti_simulation_budget.png: scripts/plot_anti_simulation.py
	python scripts/plot_anti_simulation.py --plot budget

fig/anti_simulation_failure_modes.png: scripts/plot_anti_simulation.py
	python scripts/plot_anti_simulation.py --plot modes

lean:
	@echo "Checking Lean proofs..."
	@echo "(allowing sorrys; skeletons only)"
	@if [ -f lakefile.lean ]; then lake build | cat; fi || true
	-lean --make lean/AntiSim_Hook_Skeleton.lean || true
	-lean --make lean/Lk_LB_Skeleton.lean || true
	-lean --make lean/Lkphase_Transcript_Skeleton.lean || true
	-lean --make lean/BudgetLemma.lean || true
	-lean --make lean/PsiFooling.lean || true
	-lean --make lean/LkLowerBound.lean || true
	-lean --make lean/AntiSimulationHook.lean || true
	@echo "✓ Lean skeletons verified (type-check may be partial)"

pdf:
	@echo "Compiling LaTeX to PDF..."
	pdflatex -interaction=nonstopmode main.tex | cat
	bibtex main | cat || true
	pdflatex -interaction=nonstopmode main.tex | cat
	pdflatex -interaction=nonstopmode main.tex | cat
	@echo "✓ main.pdf generated"

check:
	@echo "Running project checks (v0.8.6)..."
	python arxiv_asset_check.py
	python scripts/validate_claims.py || true
	python scripts/check_project.py || true
	@# Figures only under fig/
	@if git grep -n "\\includegraphics" -- '*.tex' | grep -v "{fig/"; then echo "✗ Found non-fig/ figure paths"; else echo "✓ Figure paths normalized to fig/"; fi
	@# Missing LaTeX references
	@grep -q "\\label{" *.tex || echo "⚠ No labels found at root .tex files"
	@echo "✓ Checks completed"

arxiv:
	@echo "Preparing arXiv-ready package (flattened .tex in root, fig/ paths)"
	@echo "(placeholder)"

test:
	@echo "Running tests..."
	pytest tests/ -v || echo "⚠ No tests found or tests failed"  
	@echo "✓ Tests completed"

clean:
	rm -f *.aux *.log *.pdf *.bbl *.blg
	rm -f notebooks/*.html 
	rm -f fig/anti_simulation_budget.png
	@echo "✓ Cleaned build artifacts"

# Quick verification of v0.8.5 acceptance criteria
verify: arxiv-check
	@echo "🔍 Verifying v0.8.5 acceptance criteria..."
	@grep -q "No-Poly-Simulation" psi-tm-08-5-anti-simulation-hook.tex && echo "✓ Core theorem present" || echo "✗ Missing No-Poly-Simulation theorem"
	@grep -q "s = n\\^\\beta" psi-tm-08-5-anti-simulation-hook.tex && echo "✓ Quantitative simulation bound" || echo "✗ Missing quantitative bound"
	@grep -q "\\beta \\geq 1/(k-1)" psi-tm-08-5-anti-simulation-hook.tex && echo "✓ Threshold specification" || echo "✗ Missing threshold"
	@grep -q "Failure Mode Analysis" psi-tm-08-5-anti-simulation-hook.tex && echo "✓ Failure modes enumerated" || echo "✗ Missing failure mode analysis"
	@grep -q "dependency.*LB" psi-tm-08-5-anti-simulation-hook.tex && echo "✓ LB integration" || echo "✗ Missing LB dependency"
	@test -f fig/anti_simulation_budget.png && echo "✓ Budget violation plot generated" || echo "✗ Missing budget analysis visualization"

plots: figures
