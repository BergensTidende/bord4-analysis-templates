# %% [markdown]
# # Mapping road data from NVDB
#
# Inspect processed NVDB road-slide data on a map.
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
import geopandas as gpd
import pandas as pd

pd.options.display.max_columns = 50
pd.options.display.max_rows = 30

# %%
df = pd.read_csv(config.get_processed_file("etl_e16.csv"), low_memory=False)

# %%
geometry = gpd.GeoSeries.from_wkt(df["geometri"])
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:5973")

# %%
gdf.head(100).explore(
    column="volum_av_skredmasser_paa_veg",
    cmap="tab10",
    style_kwds={"weight": 10, "opacity": 0.8},
    tooltip=[
        "skred_dato",
        "skred_klokkeslett",
        "type_skred",
        "volum_av_skredmasser_paa_veg",
    ],
    tiles="CartoDB Positron",
)

# %%
