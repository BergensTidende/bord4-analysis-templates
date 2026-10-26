# %% [markdown]
# # EDA SSB
#
# Show how to fetch population data from SSB and calculate rates/ranks.
#

# %%
# Interactive Python config, environment and logging

import logging
import os
import sys
from pathlib import Path

import pakkenellik.config as conf
from dotenv import load_dotenv
from pakkenellik.log import logger

# Interactive editors can run with either the project root or the notebooks folder as cwd.
PROJECT_DIR = Path.cwd().resolve()
if PROJECT_DIR.name in {"templates", "notebooks"}:
    PROJECT_DIR = PROJECT_DIR.parent

project_path = str(PROJECT_DIR)
if project_path not in sys.path:
    sys.path.insert(0, project_path)

try:
    ipython = get_ipython()
except NameError:
    ipython = None

if ipython:
    if "autoreload" not in ipython.extension_manager.loaded:
        ipython.run_line_magic("load_ext", "autoreload")
    ipython.run_line_magic("autoreload", "2")

load_dotenv(PROJECT_DIR / ".env")

config = conf.Config(project_path)
logger.setLevel(logging.INFO)

# %%
# Data manipulation
import numpy as np
import pandas as pd

pd.options.display.max_columns = 50
pd.options.display.max_rows = 30

from pakkenellik.ssb import add_rank, add_rate, get_municipality_population

# %%
municipality_ids = None

# %% [markdown]
# Use `pakkenellik.ssb` directly for population, rates and ranks.
#

# %%
df = get_municipality_population(
    years=[2024, 2025, 2026],
    municipality_ids=municipality_ids,
)

# %%
df.head()

# %%
df.shape

# %%
df["eksempel_hendelser"] = 100
df = add_rate(
    df,
    numerator_col="eksempel_hendelser",
    denominator_col="folketall",
    per=1000,
    output_col="eksempel_per_1000",
)
df = add_rank(
    df,
    value_col="eksempel_per_1000",
    group_col="år",
    ascending=False,
    output_col="eksempel_rank",
)

# %%
