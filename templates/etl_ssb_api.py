# %%
"""Small SSB helper used by the cell-based SSB template."""

from __future__ import annotations

import pandas as pd
from pakkenellik.ssb import get_municipality_population


# %%
def fetch_population(
    years: list[int] | None = None,
    municipality_ids: list[str] | None = None,
) -> pd.DataFrame:
    """Fetch municipality population from SSB table 11342."""
    return get_municipality_population(
        years=years or [2024, 2025, 2026],
        municipality_ids=municipality_ids,
    )
