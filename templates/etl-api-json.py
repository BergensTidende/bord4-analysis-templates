# %% [markdown]
# # Fetch JSON from API
#
# Generic ETL template for JSON APIs, including request parameters, pagination placeholder and processed CSV output.
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

# %%
import requests

# %% [markdown]
# ## Fetch data
#

# %%
base_url = "https://example.com/api/items"
params = {
    "page": 1,
    "per_page": 100,
}
headers = {
    "Accept": "application/json",
}

response = requests.get(base_url, params=params, headers=headers, timeout=30)
response.raise_for_status()

data = response.json()

# %% [markdown]
# ## Normalize JSON
#

# %%
records = data.get("items", data if isinstance(data, list) else [])
df = pd.json_normalize(records)
logger.info("Fetched %s rows", len(df))

df.head()

# %% [markdown]
# ## Optional pagination
#

# %%
dfs = []
page = 1

while True:
    params["page"] = page
    response = requests.get(base_url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    page_data = response.json()
    records = page_data.get("items", [])

    if not records:
        break

    dfs.append(pd.json_normalize(records))
    logger.info("Fetched page %s with %s rows", page, len(records))
    page += 1

df_all = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
df_all.head()

# %% [markdown]
# ## Save processed data
#

# %%
output_path = config.get_processed_file("etl_api_json.csv")
df_all.to_csv(output_path, index=False)
logger.info("Saved processed data to %s", output_path)
