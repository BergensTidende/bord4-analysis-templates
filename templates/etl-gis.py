# %% [markdown]
# # Fetch geodata from WFS
#
# Example ETL for reading a WFS endpoint, saving raw GML and converting it to GeoJSON.
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
# WFS and GeoPandas
import geopandas as gpd
from owslib.wfs import WebFeatureService

# More GIS examples: https://autogis-site.readthedocs.io/en/latest/index.html

# %%
wfs_url = "https://wfs.geonorge.no/skwms1/wfs.bergrettigheter?request=GetCapabilities&service=WFS"
wfs = WebFeatureService(url=wfs_url, version="2.0.0")

logger.info("Service: %s", wfs.identification.title)
logger.info("WFS version: %s", wfs.version)
logger.info("Operations: %s", [operation.name for operation in wfs.operations])
logger.info("Layers: %s", list(wfs.contents))

# %%
layer_name = list(wfs.contents)[0]

# %%
response = wfs.getfeature(typename=layer_name)
output_path = config.get_processed_file("etl_bergrettigheter.gml")

with open(output_path, "wb") as file:
    file.write(response.read())

logger.info("Saved raw GML to %s", output_path)

# %% [markdown]
# ### Convert GML to GeoJSON
#
# GeoPandas can read many formats directly, but converting WFS GML to GeoJSON with GDAL is often more stable. If you use Postgres.app on macOS, make sure Homebrew GDAL is first in `PATH`; the bundled GDAL may not support these GML files.
#

# %%
# !ogr2ogr -f GeoJSON {config.get_processed_file("etl_bergrettigheter.geojson")} {config.get_processed_file("etl_bergrettigheter.gml")}

# %%
bergrettigheter_gdf = gpd.read_file(
    config.get_processed_file("etl_bergrettigheter.geojson")
)

logger.info("Loaded %s rows", len(bergrettigheter_gdf))
bergrettigheter_gdf.plot()

# %%
