#!/usr/bin/env python3
import argparse
import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


OUT_DIR = "fig"
os.makedirs(OUT_DIR, exist_ok=True)

mpl.rcParams["mathtext.fontset"] = "stix"
mpl.rcParams["font.size"] = 12
mpl.rcParams["axes.labelsize"] = 12
mpl.rcParams["axes.titlesize"] = 14
mpl.rcParams["legend.fontsize"] = 10


def save_fig(fig: mpl.figure.Figure, filename: str, dpi: int = 300) -> None:
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    assert os.path.getsize(path) > 0, f"Empty file saved: {path}"
    print("saved:", path)


def plot_budget() -> None:
    n = 10 ** 6
    ks = [2, 3, 4, 5]
    betas = np.linspace(0.05, 1.0, 40)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for k in ks:
        ratio = (n ** betas) * ((k - 1) / k)  # logs cancel; linear on log-Y
        ax.plot(betas, ratio, label=f"k={k}")

    ax.axhline(1.0, color="k", linestyle="--", linewidth=1, label="violation threshold")

    def beta_thr(k_val: int, n_val: int) -> float:
        return np.log(k_val / (k_val - 1)) / np.log(n_val)

    for k in ks:
        b = beta_thr(k, n)
        ax.axvline(b, linestyle=":", linewidth=1)
        ax.text(
            b, 1.2,
            fr"$\beta_{{k={k}}}\approx{b:.3f}$",
            rotation=90, va="bottom", ha="right",
        )

    ax.set_yscale("log")
    ax.set_xlabel(r"$\\beta$")
    ax.set_ylabel(r"$\\frac{s\\,B(k-1,n)}{B(k,n)}$")
    ax.set_title(r"Budget violation ratio vs $\\beta$")
    ax.legend(loc="best")
    fig.tight_layout()
    save_fig(fig, "anti_simulation_budget.png")
    plt.close(fig)


def plot_modes() -> None:
    modes = ["Super-log budget", "Randomized sim", "Advice", "Multi-pass"]
    status = [1, 1, 1, 1]  # 1=blocked
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    bars = ax.bar(modes, status)
    for i, s in enumerate(status):
        ax.text(i, s + 0.02, "Blocked" if s else "Allowed", ha="center", va="bottom")
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Bypass status")
    ax.set_title("Failure mode analysis: all bypass routes blocked")
    plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
    fig.tight_layout()
    save_fig(fig, "anti_simulation_failure_modes.png")
    plt.close(fig)


def plot_budget_saved() -> None:
    n = 10 ** 6
    ks = [2, 3, 4, 5]
    betas2 = np.linspace(0.05, 1.0, 60)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for k in ks:
        ratio = (n ** betas2) * ((k - 1) / k)
        ax.plot(betas2, ratio, label=f"k={k}")
    ax.axhline(1.0, color="k", linestyle="--", linewidth=1)
    ax.set_yscale("log")
    ax.set_xlabel(r"$\\beta$")
    ax.set_ylabel(r"$\\frac{s\\,B(k-1,n)}{B(k,n)}$")
    ax.set_title(r"Budget violation ratio vs $\\beta$ (saved)")
    ax.legend(loc="best")
    fig.tight_layout()
    save_fig(fig, "anti_simulation_budget_saved.png")
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate anti-simulation figures")
    parser.add_argument(
        "--plot",
        choices=["budget", "modes", "saved", "all"],
        default="all",
        help="Which plot(s) to generate",
    )
    args = parser.parse_args(argv)

    if args.plot in ("budget", "all"):
        plot_budget()
    if args.plot in ("modes", "all"):
        plot_modes()
    if args.plot in ("saved", "all"):
        plot_budget_saved()

    # Basic existence checks for requested plots
    requested = []
    if args.plot == "budget":
        requested = ["anti_simulation_budget.png"]
    elif args.plot == "modes":
        requested = ["anti_simulation_failure_modes.png"]
    elif args.plot == "saved":
        requested = ["anti_simulation_budget_saved.png"]
    else:
        requested = [
            "anti_simulation_budget.png",
            "anti_simulation_failure_modes.png",
            "anti_simulation_budget_saved.png",
        ]

    for filename in requested:
        path = os.path.join(OUT_DIR, filename)
        if not (os.path.exists(path) and os.path.getsize(path) > 0):
            print(f"error: missing or empty file: {path}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

