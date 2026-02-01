# All finance assumptions live here

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ModelConfig:
    # Reproducibility
    random_seed: int = 42

    # Simulation size
    n_sims: int = 10_000

    # Cost categories (annual means in USD)
    annual_mean: Dict[str, float] = None

    # Annual volatility (% of annual mean), e.g., 0.05 = 5%
    annual_vol_pct: Dict[str, float] = None

    # Budget definition (budget = expected_total * (1 + buffer))
    budget_buffer_pct: float = 0.03

    # Plot settings
    histogram_bins: int = 60


def default_config() -> ModelConfig:
    annual_mean = {
        "labor": 5_400_000.0,
        "materials": 2_100_000.0,
        "maintenance": 2_300_000.0,
    }
    annual_vol_pct = {
        "labor": 0.05,
        "materials": 0.10,
        "maintenance": 0.20,
    }
    return ModelConfig(
        annual_mean=annual_mean,
        annual_vol_pct=annual_vol_pct,
    )
