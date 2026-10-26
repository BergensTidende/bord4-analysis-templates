# %% [markdown]
# # Manual dataset
#
# Use this when the dataset is small enough to type or paste directly into a notebook.
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
# ## Enter data
#

# %%
rows = [
    {"name": "Example A", "value": 10, "date": "2024-01-01"},
    {"name": "Example B", "value": 20, "date": "2024-01-02"},
]

df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"])

df

# %% [markdown]
# ## Validate
#

# %%
required_columns = ["name", "value", "date"]
missing_columns = set(required_columns) - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing columns: {sorted(missing_columns)}")

if df[required_columns].isna().any().any():
    raise ValueError("Required columns contain missing values")

df.describe(include="all")

# %% [markdown]
# ## Save processed data
#

# %%
output_path = config.get_processed_file("etl_manual_data.csv")
df.to_csv(output_path, index=False)
logger.info("Saved manual dataset to %s", output_path)
