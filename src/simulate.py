# generate the simulated monthly and annual costs

from __future__ import annotations

import math
from typing import Dict, Tuple

import numpy as np
import pandas as pd

from .config import ModelConfig


def _validate_config(cfg: ModelConfig) -> None:
    if not cfg.annual_mean or not cfg.annual_vol_pct:
        raise ValueError("annual_mean and annual_vol_pct must be provided in config.")

    mean_keys = set(cfg.annual_mean.keys())
    vol_keys = set(cfg.annual_vol_pct.keys())
    if mean_keys != vol_keys:
        raise ValueError(f"annual_mean keys {mean_keys} must match annual_vol_pct keys {vol_keys}.")

    if cfg.n_sims <= 0:
        raise ValueError("n_sims must be > 0.")

    for k, v in cfg.annual_mean.items():
        if v <= 0:
            raise ValueError(f"annual_mean[{k}] must be > 0, got {v}.")

    for k, v in cfg.annual_vol_pct.items():
        if v < 0:
            raise ValueError(f"annual_vol_pct[{k}] must be >= 0, got {v}.")

    if cfg.budget_buffer_pct < 0:
        raise ValueError("budget_buffer_pct must be >= 0.")


def compute_budget(cfg: ModelConfig) -> float:
    expected_total = float(sum(cfg.annual_mean.values()))
    return expected_total * (1.0 + cfg.budget_buffer_pct)


def run_simulation(cfg: ModelConfig) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
    """
    Returns:
      monthly_df: sim_id x month rows with category costs + total_month
      annual_df: sim_id rows with annual totals (per category + total_annual)
      budget: annual budget threshold
    """
    _validate_config(cfg)
    rng = np.random.default_rng(cfg.random_seed)

    categories = list(cfg.annual_mean.keys())
    n_sims = cfg.n_sims
    months = np.arange(1, 13)

    # Convert annual mean/vol -> monthly mean/std
    monthly_mean: Dict[str, float] = {}
    monthly_std: Dict[str, float] = {}
    for c in categories:
        a_mean = float(cfg.annual_mean[c])
        a_vol = float(cfg.annual_vol_pct[c])
        a_std = a_mean * a_vol
        # Approx monthly std assuming independent monthly noise:
        m_std = a_std / math.sqrt(12.0)
        monthly_mean[c] = a_mean / 12.0
        monthly_std[c] = m_std

    # Simulate: arrays shaped (n_sims, 12)
    sim_arrays: Dict[str, np.ndarray] = {}
    for c in categories:
        arr = rng.normal(loc=monthly_mean[c], scale=monthly_std[c], size=(n_sims, 12))
        # costs cannot be negative
        arr = np.clip(arr, 0.0, None)
        sim_arrays[c] = arr

    total_month = np.zeros((n_sims, 12), dtype=float)
    for c in categories:
        total_month += sim_arrays[c]

    # Build monthly_df (tidy)
    sim_id = np.repeat(np.arange(1, n_sims + 1), 12)
    month_col = np.tile(months, n_sims)

    data = {
        "sim_id": sim_id,
        "month": month_col,
    }
    for c in categories:
        data[c] = sim_arrays[c].reshape(-1)
    data["total_month"] = total_month.reshape(-1)

    monthly_df = pd.DataFrame(data)

    # Annual aggregation
    annual_data = {"sim_id": np.arange(1, n_sims + 1)}
    total_annual = np.zeros(n_sims, dtype=float)

    for c in categories:
        annual_c = sim_arrays[c].sum(axis=1)
        annual_data[c] = annual_c
        total_annual += annual_c

    annual_data["total_annual"] = total_annual
    annual_df = pd.DataFrame(annual_data)

    budget = compute_budget(cfg)
    return monthly_df, annual_df, budget
