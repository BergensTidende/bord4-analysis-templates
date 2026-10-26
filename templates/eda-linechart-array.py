# %% [markdown]
# # Exploratory data analysis (EDA)
#
# Use this notebook to inspect processed data and look for story leads.
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
# Visualization and analysis

# %matplotlib inline

import math

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

pd.options.display.max_columns = 50
pd.options.display.max_rows = 30

# %% [markdown]
# # Get data

# %%
df = pd.read_csv(config.get_processed_file("etl_vestland.csv"))
df["municipality_id"] = df["municipality_id"].astype(str)

# %%
graphs_per_row = 3
municipalities = df["municipality_id"].unique()
rows = math.ceil(len(municipalities) / graphs_per_row)

df = df.sort_values(by=["municipality", "year"])

with plt.style.context("fivethirtyeight"):
    fig, axes = plt.subplots(
        rows, graphs_per_row, figsize=(20, 4 * rows), squeeze=False
    )
    plt.subplots_adjust(hspace=0.4)

    for index, municipality_id in enumerate(municipalities):
        df_data = df[df["municipality_id"] == municipality_id]
        ax = axes[index // graphs_per_row, index % graphs_per_row]
        ax.set_title(df_data["municipality"].iloc[0])
        df_data.plot(ax=ax, x="year", y="population", legend=False)

    for index in range(len(municipalities), rows * graphs_per_row):
        axes[index // graphs_per_row, index % graphs_per_row].axis("off")

# %%
