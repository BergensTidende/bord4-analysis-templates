# %% [markdown]
# # Extract, transform and load (ETL)
#
# * Data source:
# * Contact:
# * Update frequency:
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
# # Get data

# %%
# Get data for Norwegian municipalities from bord4-data repo
df = pd.read_csv(config.get_url("norwegian-population"))
logger.info("Fetched Norwegian population data")

# %%
df.columns

# %%
df.shape

# %% [markdown]
# # Filter

# %%
# Get all municipalities in Vestland
df_vestland = df[(df["county_id"] == "46") & (df["region_id"].str.len() == 4)].copy()

# %%
df_vestland = df_vestland[["municipality_id", "municipality", "year", "population"]]

# %% [markdown]
# ## Save Dataframe

# %%
output_path = config.get_processed_file("etl_vestland.csv")
df_vestland.to_csv(output_path, index=False)
logger.info("Saved processed data to %s", output_path)

# %%
