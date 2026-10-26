# %% [markdown]
# # Read Excel file
#
# Import one worksheet from an Excel workbook, clean column names and save a processed CSV.
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
# ## Read workbook
#

# %%
source_path = PROJECT_DIR / "data" / "source" / "example.xlsx"
sheet_name = 0

df = pd.read_excel(source_path, sheet_name=sheet_name)
logger.info("Read %s rows from %s", len(df), source_path)

df.head()

# %% [markdown]
# ## Clean columns
#

# %%
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
    .str.replace(r"[^0-9a-zA-Z_]+", "", regex=True)
)

df.head()

# %% [markdown]
# ## Save processed data
#

# %%
output_path = config.get_processed_file("etl_excel.csv")
df.to_csv(output_path, index=False)
logger.info("Saved processed data to %s", output_path)
