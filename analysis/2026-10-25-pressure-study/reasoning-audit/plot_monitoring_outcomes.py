"""Plot all final choices for completed watched/unwatched matched cells.

Inputs are derived episode metrics from extract.py. Both arms must have completed
for the same scenario, pressure level, pairing, and (the single frozen) seed.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


OUT = Path(__file__).resolve().parent
FIG = OUT / "figures"
MODES = ("unwatched", "watched")
PAIRINGS = ("W-W", "W-none", "D-D", "D-none", "A-A", "A-none")
COLORS = {"unwatched": "#D48638", "watched": "#326789"}
ONLY_COLORS = {"A only": "#30779A", "B only": "#D18A3D"}


def save(fig, name):
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / f"{name}.png", dpi=190, bbox_inches="tight")
    svg = FIG / f"{name}.svg"
    fig.savefig(svg, bbox_inches="tight")
    # Matplotlib places presentation-only trailing spaces on SVG path lines.
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def matched_episodes():
    data = pd.read_csv(OUT / "episode_metrics.csv")
    key = ["scenario", "level", "pairing"]
    assert not data.duplicated(key + ["monitoring"]).any()
    complete = data[data.status == "complete"].copy()
    cells = complete.groupby(key).monitoring.nunique()
    both = cells[cells == 2].index
    complete = complete.set_index(key).loc[both].reset_index()
    assert len(complete) == 2 * len(both)
    assert set(complete.monitoring) == set(MODES)
    assert set(complete.action_a.unique()) <= {"take", "refuse"}
    assert set(complete.action_b.unique()) <= {"take", "refuse"}
    complete["outcome"] = np.select(
        [
            (complete.action_a == "take") & (complete.action_b == "take"),
            (complete.action_a == "take") & (complete.action_b == "refuse"),
            (complete.action_a == "refuse") & (complete.action_b == "take"),
        ],
        ["Both take", "A only", "B only"],
        default="Both refuse",
    )
    return complete, len(both)


def make_table(data):
    rows = []
    for pairing in ("All pairings",) + PAIRINGS:
        subset = data if pairing == "All pairings" else data[data.pairing == pairing]
        for mode in MODES:
            arm = subset[subset.monitoring == mode]
            counts = arm.outcome.value_counts()
            row = {"pairing": pairing, "monitoring": mode, "matched_cells": len(arm)}
            for name, column in [
                ("Both take", "both_take"),
                ("A only", "a_takes_b_refuses"),
                ("B only", "b_takes_a_refuses"),
                ("Both refuse", "both_refuse"),
            ]:
                row[column] = int(counts.get(name, 0))
                row[column + "_rate"] = row[column] / len(arm)
            row["unilateral_total"] = row["a_takes_b_refuses"] + row["b_takes_a_refuses"]
            row["unilateral_rate"] = row["unilateral_total"] / len(arm)
            assert sum(row[name] for name in ("both_take", "a_takes_b_refuses", "b_takes_a_refuses", "both_refuse")) == len(arm)
            rows.append(row)
    result = pd.DataFrame(rows)
    result.to_csv(OUT / "monitoring_all_outcomes.csv", index=False)
    return result


def all_outcomes_plot(table, n):
    fig, ax = plt.subplots(figsize=(10.5, 5.7))
    categories = [
        ("Both take", "both_take"),
        ("One takes", "unilateral_total"),
        ("Both refuse", "both_refuse"),
    ]
    x = np.arange(3)
    overall = table[table.pairing == "All pairings"].set_index("monitoring")
    for offset, mode in [(-0.19, "unwatched"), (0.19, "watched")]:
        values = [100 * overall.loc[mode, column] / n for _, column in categories]
        bars = ax.bar(x + offset, values, width=0.35, color=COLORS[mode], label=mode.capitalize())
        for bar, (_, column), value in zip(bars, categories, values):
            count = int(overall.loc[mode, column])
            ax.annotate(f"{value:.1f}%\n({count:,})", (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 5), textcoords="offset points", ha="center", va="bottom", fontsize=10)
    ax.set_xticks(x, [label for label, _ in categories])
    ax.set_ylabel("Share of completed matched episodes (%)")
    ax.set_ylim(0, 78)
    ax.set_title("Watched vs unwatched: every final outcome", fontsize=17, fontweight="bold", pad=16)
    ax.legend(frameon=False, ncol=2, loc="upper left")
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.11, 0.015, f"n = {n:,} paired scenarios per arm. One takes = A only + B only; the proposed action executes only if both take.", fontsize=9, color="#4A5560")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    save(fig, "watched-unwatched-all-outcomes")


def unilateral_plot(table):
    fig, ax = plt.subplots(figsize=(11.2, 9.2))
    groups = ("All pairings",) + PAIRINGS
    labels, positions = [], []
    max_total = 0
    for group_index, pairing in enumerate(groups):
        for mode_index, mode in enumerate(MODES):
            row = table[(table.pairing == pairing) & (table.monitoring == mode)].iloc[0]
            y = 2.55 * group_index + 0.74 * mode_index
            a = 100 * row.a_takes_b_refuses_rate
            b = 100 * row.b_takes_a_refuses_rate
            ax.barh(y, a, height=0.63, color=ONLY_COLORS["A only"], label="A takes; B refuses" if group_index == mode_index == 0 else None)
            ax.barh(y, b, left=a, height=0.63, color=ONLY_COLORS["B only"], label="B takes; A refuses" if group_index == mode_index == 0 else None)
            ax.text(a + b + 0.25, y, f"{a+b:.1f}%  ({int(row.unilateral_total)}/{int(row.matched_cells)})", va="center", fontsize=9)
            labels.append(f"{pairing}  ·  {mode}")
            positions.append(y)
            max_total = max(max_total, a + b)
        if group_index < len(groups) - 1:
            ax.axhline(2.55 * group_index + 1.62, color="#DCE2E8", lw=0.8)
    ax.set_yticks(positions, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max_total + 5.8)
    ax.set_xlabel("Share of completed matched episodes (%)")
    ax.set_title("Who takes alone? Overall and by agent pairing", fontsize=17, fontweight="bold", pad=16)
    ax.legend(frameon=False, ncol=2, loc="lower right")
    ax.grid(axis="x", alpha=0.18)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.text(0.26, 0.015, "W = welfare; D = non-deception; A = authority; none = no added criterion. A always has the first named criterion.", fontsize=9, color="#4A5560")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "watched-unwatched-unilateral-detail")


def main():
    data, n = matched_episodes()
    table = make_table(data)
    assert n == 2083  # frozen completed collection
    all_outcomes_plot(table, n)
    unilateral_plot(table)
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
