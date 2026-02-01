# a single command to run everything

from __future__ import annotations

import os

from .config import default_config
from .simulate import run_simulation
from .analyze import annual_summary_metrics, variance_contribution
from .report import export_excel_report, save_distribution_plot


def main() -> None:
    cfg = default_config()

    monthly_df, annual_df, budget = run_simulation(cfg)

    summary_df = annual_summary_metrics(annual_df=annual_df, budget=budget)
    category_cols = [c for c in annual_df.columns if c not in ("sim_id", "total_annual")]
    drivers_df = variance_contribution(annual_df=annual_df, category_cols=category_cols)

    out_xlsx = os.path.join("outputs", "om_budget_risk_report.xlsx")
    out_png = os.path.join("outputs", "annual_cost_distribution.png")

    export_excel_report(
        cfg=cfg,
        summary_df=summary_df,
        drivers_df=drivers_df,
        annual_df=annual_df,
        out_path=out_xlsx,
    )

    save_distribution_plot(
        annual_df=annual_df,
        budget=budget,
        out_path=out_png,
        bins=cfg.histogram_bins,
    )

    print(f"✅ Wrote Excel report: {out_xlsx}")
    print(f"✅ Wrote chart:       {out_png}")
    print(f"Budget threshold used: ${budget:,.0f}")


if __name__ == "__main__":
    main()
