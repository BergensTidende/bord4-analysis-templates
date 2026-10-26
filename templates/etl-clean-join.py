# %% [markdown]
# # Clean and join datasets
#
# Template for joining two processed datasets and checking row counts, match coverage and unmatched keys.
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
left = pd.read_csv(config.get_processed_file("etl_left.csv"))
right = pd.read_csv(config.get_processed_file("etl_right.csv"))

logger.info("Left: %s rows", len(left))
logger.info("Right: %s rows", len(right))

# %% [markdown]
# ## Prepare join keys
#

# %%
join_key = "id"

left[join_key] = left[join_key].astype(str).str.strip()
right[join_key] = right[join_key].astype(str).str.strip()

left = left.drop_duplicates(subset=[join_key]).copy()
right = right.drop_duplicates(subset=[join_key]).copy()

# %% [markdown]
# ## Join and inspect coverage
#

# %%
joined = left.merge(
    right,
    on=join_key,
    how="left",
    indicator=True,
    validate="one_to_one",
)

coverage = joined["_merge"].value_counts(dropna=False).to_frame("rows")
display(coverage)

display(joined[joined["_merge"] != "both"].head(20))

# %% [markdown]
# ## Save joined data
#

# %%
joined = joined.drop(columns=["_merge"])
output_path = config.get_processed_file("etl_joined.csv")
joined.to_csv(output_path, index=False)
logger.info("Saved joined data to %s", output_path)
