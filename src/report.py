# Produce Excel charts and stuff here.


from __future__ import annotations

import os
import matplotlib.pyplot as plt
import pandas as pd

from .config import ModelConfig


def save_distribution_plot(
    annual_df: pd.DataFrame,
    budget: float,
    out_path: str,
    bins: int = 60,
) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    totals = annual_df["total_annual"].astype(float)

    plt.figure()
    plt.hist(totals, bins=bins)
    plt.axvline(budget, linewidth=2)
    plt.title("Simulated Annual O&M Cost Distribution")
    plt.xlabel("Annual O&M Cost (USD)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def export_excel_report(
    cfg: ModelConfig,
    summary_df: pd.DataFrame,
    drivers_df: pd.DataFrame,
    annual_df: pd.DataFrame,
    out_path: str,
) -> str:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Build an assumptions table for transparency
    assumptions_rows = []
    for c in cfg.annual_mean.keys():
        assumptions_rows.append({
            "category": c,
            "annual_mean_usd": float(cfg.annual_mean[c]),
            "annual_vol_pct": float(cfg.annual_vol_pct[c]),
        })
    assumptions_df = pd.DataFrame(assumptions_rows)
    assumptions_meta = pd.DataFrame([{
        "n_sims": cfg.n_sims,
        "random_seed": cfg.random_seed,
        "budget_buffer_pct": cfg.budget_buffer_pct,
    }])

    # Write workbook
    with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        drivers_df.to_excel(writer, sheet_name="Risk Drivers", index=False)
        assumptions_df.to_excel(writer, sheet_name="Assumptions", index=False, startrow=0)
        assumptions_meta.to_excel(writer, sheet_name="Assumptions", index=False, startrow=len(assumptions_df) + 3)
        # Keep annual output manageable but still inspectable:
        annual_df.to_excel(writer, sheet_name="Annual Sims", index=False)

        # Light formatting (finance-friendly)
        workbook = writer.book

        money_fmt = workbook.add_format({"num_format": "$#,##0"})
        pct_fmt = workbook.add_format({"num_format": "0.0%"})
        # dec_fmt = workbook.add_format({"num_format": "0.00"})

        # Summary formatting
        ws = writer.sheets["Summary"]
        # Apply column formats by header name
        for col_idx, col_name in enumerate(summary_df.columns):
            if "pct" in col_name or "prob_" in col_name or "share" in col_name:
                ws.set_column(col_idx, col_idx, 22, pct_fmt)
            elif "cost" in col_name or "budget" in col_name or "overrun" in col_name:
                ws.set_column(col_idx, col_idx, 26, money_fmt)
            else:
                ws.set_column(col_idx, col_idx, 22)

        # Risk Drivers formatting
        ws = writer.sheets["Risk Drivers"]
        ws.set_column(0, 0, 18)  # category
        ws.set_column(1, 1, 22, money_fmt)  # variance
        ws.set_column(2, 2, 18, pct_fmt)  # share

        # Assumptions formatting
        ws = writer.sheets["Assumptions"]
        ws.set_column(0, 0, 18)
        ws.set_column(1, 1, 22, money_fmt)
        ws.set_column(2, 2, 18, pct_fmt)

        # Annual sims formatting
        ws = writer.sheets["Annual Sims"]
        # sim_id then money columns
        ws.set_column(0, 0, 10)
        for i in range(1, len(annual_df.columns)):
            ws.set_column(i, i, 20, money_fmt)

    return out_path
