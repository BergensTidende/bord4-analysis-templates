# %% [markdown]
# # Update Datawrapper chart
#
# Minimal template for pushing a processed dataset to an existing Datawrapper chart.
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
import pandas as pd

pd.options.display.max_columns = 50
pd.options.display.max_rows = 30

# %%
from pakkenellik.datawrapper.client import Datawrapper

# %%
DATAWRAPPER_API_TOKEN = os.environ["DATAWRAPPER_API_TOKEN"]
DW_FOLDER = os.environ.get("DW_FOLDER")

dw = Datawrapper(access_token=DATAWRAPPER_API_TOKEN)

# %%
chart_id = "CHART_ID"
data_path = config.get_processed_file("etl_vestland.csv")
chart_data = pd.read_csv(data_path)

dw.add_data(chart_id, chart_data)
dw.update_chart(chart_id)
