# %% [markdown]
# # Publish Datawrapper chart
#
# Use publish notebooks for analysis and graphics used in the final article. Use EDA notebooks for exploration.
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

# Visualizations
import matplotlib.pyplot as plt

# %%
# Create charts
from pakkenellik.datawrapper.client import Datawrapper
from pakkenellik.integration.client import create_dw_integration, get_or_create_chart

DATAWRAPPER_API_TOKEN = os.environ["DATAWRAPPER_API_TOKEN"]
DW_FOLDER = os.environ.get("DW_FOLDER")

dw = Datawrapper(access_token=DATAWRAPPER_API_TOKEN)

# %% [markdown]
# ## Import data

# %%
df = pd.read_csv(config.get_processed_file("etl_vestland.csv"))
df["municipality_id"] = df["municipality_id"].astype(str)

# %% [markdown]
# ## Analysis for article

# %%
df["pct_ch"] = df.groupby("municipality_id", group_keys=False)[
    "population"
].pct_change()

# %%
df

# %%
# Find ten year and municipality with largest drops
df.sort_values(by="pct_ch").head(10)

# %% [markdown]
# ## Graphs for article

# %%
# Create graph for Fedje
df[df.municipality_id == "4633"].plot(x="year", y="population")

# %% [markdown]
# ## Use Datawrapper to create graph

# %%
integration_key = "fedje"
chart_id = get_or_create_chart(
    dw,
    integration_key,
    title="Befolkningsutvikling i Fedje-kommune 2001–2022",
    chart_type="d3-lines",
    folder_id=DW_FOLDER,
)

# %%
metadata = dw.chart_properties(chart_id)["metadata"]
visualize = metadata.setdefault("visualize", {})
visualize.setdefault("colorscale", {})["colors"] = [{"color": "#f0f0f0", "position": 0}]
visualize.setdefault("legend", {})["title"] = "Antall innbyggere"

dw.update_metadata(chart_id, metadata)

chart_data = df[df["municipality_id"] == "4633"][["year", "population"]]
dw.add_data(chart_id, chart_data)
dw.update_chart(chart_id)

# %% [markdown]
# ## Create integrations

# %%
# Create or update integration
create_dw_integration(dw, integration_key, chart_id)
