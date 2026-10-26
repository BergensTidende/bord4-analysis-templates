# %% [markdown]
# # Quick data check
#
# First-pass EDA for a processed dataset: dimensions, column types, missing values, duplicates and simple distributions.
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

# %% [markdown]
# ## Load data
#

# %%
data_path = config.get_processed_file("etl_dataset.csv")
df = pd.read_csv(data_path)
logger.info("Loaded %s rows and %s columns", len(df), len(df.columns))

df.head()

# %% [markdown]
# ## Structure
#

# %%
display(df.shape)
display(df.dtypes.to_frame("dtype"))
df.info()

# %% [markdown]
# ## Missing values and duplicates
#

# %%
missing = (
    df.isna()
    .sum()
    .to_frame("missing")
    .assign(missing_pct=lambda x: x["missing"] / len(df))
    .sort_values("missing", ascending=False)
)

display(missing)
display({"duplicate_rows": df.duplicated().sum()})

# %% [markdown]
# ## Numeric summary
#

# %%
df.describe(include="number").T

# %% [markdown]
# ## Categorical summary
#

# %%
categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns

for column in categorical_cols[:10]:
    display(df[column].value_counts(dropna=False).head(20).to_frame("count"))

# %% [markdown]
# ## Date range
#

# %%
date_columns = [
    column
    for column in df.columns
    if "date" in column.lower() or "dato" in column.lower()
]

for column in date_columns:
    dates = pd.to_datetime(df[column], errors="coerce")
    display(
        pd.DataFrame(
            {
                "column": [column],
                "min": [dates.min()],
                "max": [dates.max()],
                "missing": [dates.isna().sum()],
            }
        )
    )
