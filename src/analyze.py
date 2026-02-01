# Turn simulated costs into decisions

from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd


def annual_summary_metrics(annual_df: pd.DataFrame, budget: float) -> pd.DataFrame:
    """
    Returns a 1-row DataFrame with finance-style metrics.
    """
    totals = annual_df["total_annual"].astype(float).to_numpy()

    prob_over = float(np.mean(totals > budget))
    overruns = totals[totals > budget] - budget
    avg_overrun_if_over = float(np.mean(overruns)) if overruns.size else 0.0
    expected_overrun = float(np.mean(np.maximum(totals - budget, 0.0)))

    p50 = float(np.percentile(totals, 50))
    p90 = float(np.percentile(totals, 90))
    p95 = float(np.percentile(totals, 95))
    p99 = float(np.percentile(totals, 99))
    mean = float(np.mean(totals))
    std = float(np.std(totals, ddof=1))

    return pd.DataFrame([{
        "budget": float(budget),
        "mean_annual_cost": mean,
        "std_annual_cost": std,
        "p50_annual_cost": p50,
        "p90_annual_cost": p90,
        "p95_annual_cost": p95,
        "p99_annual_cost": p99,
        "prob_over_budget": prob_over,
        "avg_overrun_if_over_budget": avg_overrun_if_over,
        "expected_overrun": expected_overrun,
    }])


def variance_contribution(annual_df: pd.DataFrame, category_cols: List[str]) -> pd.DataFrame:
    """
    Simple, interpretable "risk driver" view:
      variance share by category (based on simulated annual category totals).
    """
    var_by_cat: Dict[str, float] = {}
    for c in category_cols:
        var_by_cat[c] = float(annual_df[c].astype(float).var(ddof=1))

    total_var = sum(var_by_cat.values())
    rows = []
    for c in category_cols:
        share = (var_by_cat[c] / total_var) if total_var > 0 else 0.0
        rows.append({
            "category": c,
            "annual_variance": var_by_cat[c],
            "variance_share": share,
        })

    out = pd.DataFrame(rows).sort_values("variance_share", ascending=False).reset_index(drop=True)
    return out
