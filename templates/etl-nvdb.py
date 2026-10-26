# %% [markdown]
# # Usage of NVDB data
#
# https://www.vegvesen.no/nvdb/apidokumentasjon
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

from datetime import datetime

# %%
# NVDB API and GeoPandas
import geopandas as gpd
import nvdbapiv3
import pandas as pd
from pakkenellik.dataframe.clean_column_headers import clean_column_headers
from pakkenellik.dataframe.datetime import (
    add_month_name,
    add_week_day,
    add_week_day_name,
    add_ymd,
)
from pakkenellik.regions import add_municipality_info

# %%
ras_data = nvdbapiv3.nvdbFagdata(445)
df = pd.DataFrame(ras_data.to_records())
df = clean_column_headers(df)
df.head()

# %%
df.columns

# %%
df["skred_dato"] = pd.to_datetime(df["skred_dato"], format="%Y-%m-%d")
df = add_ymd(df, "skred_dato")
df = add_month_name(df, "skred_dato")
df = add_week_day(df, "skred_dato")
df = add_week_day_name(df, "skred_dato", nynorsk=True)
df = add_municipality_info(df, municipality_col="kommune")

# %%
geometry = gpd.GeoSeries.from_wkt(df["geometri"])
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# %%
timestamp = datetime.now().strftime("%Y%m%d-%H%M")
output_path = config.get_processed_file(f"etl_e16_{timestamp}.geojson")
e16_gdf = gdf[(gdf["vegkategori"] == "E") & (gdf["vegnummer"] == 16)]

with open(output_path, "w") as file:
    file.write(e16_gdf[["skred_dato", "geometry"]].to_json(default=str))

logger.info("Saved E16 GeoJSON to %s", output_path)

# %%
df.to_csv(config.get_processed_file("etl_e16.csv"), index=False)

# %%
